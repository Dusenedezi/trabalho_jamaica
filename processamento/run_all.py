"""Extração automatizada — executa todo o catálogo de config/series.yaml.

Para cada série:
  dados/brutos/<id>_<AAAAMMDD>.<json|csv>   payload original (ou cópia datada do CSV manual)
  dados/processados/<id>.csv                 formato tidy: iso3, pais, ano, valor (+ colunas extras nas manuais)
E ao final:
  dados/processados/fontes.csv               tabela de fontes exigida pelo enunciado
  dados/processados/log_extracao.csv         registro de sucesso/erro por série

Uso:  python processamento/run_all.py [--somente id1,id2]
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).parent))
from extract import csv_url, manual, undp, worldbank  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
CONFIG = RAIZ / "config" / "series.yaml"
BRUTOS = RAIZ / "dados" / "brutos"
PROC = RAIZ / "dados" / "processados"


def carregar_config() -> dict:
    with CONFIG.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def extrair(serie: dict, cfg: dict, hoje: str) -> pd.DataFrame:
    paises = [cfg["pais"]] + cfg["comparadores"]
    ini, fim = cfg["periodo"]["inicio"], cfg["periodo"]["fim"]
    sid, fonte = serie["id"], serie["fonte"]

    if fonte == "worldbank":
        payload, df = worldbank.fetch(serie["codigo"], paises, ini, fim, serie.get("source_id", 2))
        worldbank.save_raw(payload, BRUTOS / f"{sid}_{hoje}.json")

    elif fonte == "undp":
        texto, df = undp.fetch(serie["url_arquivo"], serie["codigo"], paises)
        undp.save_raw(texto, BRUTOS / f"{sid}_{hoje}.csv")

    elif fonte == "csv_url":
        texto, df = csv_url.fetch(serie, paises, ini, fim)
        csv_url.save_raw(texto, BRUTOS / f"{sid}_{hoje}.csv")

    elif fonte == "manual":
        caminho, df = manual.fetch(serie, RAIZ)
        manual.save_raw(caminho, BRUTOS / f"{sid}_{hoje}.csv")

    else:
        raise ValueError(f"Fonte desconhecida: {fonte}")

    # nome legível a partir do catálogo (a fonte pode trazer só o iso3)
    df["pais"] = df["iso3"].map(cfg.get("nomes", {})).fillna(df["pais"])
    df.to_csv(PROC / f"{sid}.csv", index=False)
    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--somente", help="ids separados por vírgula", default=None)
    args = parser.parse_args()

    cfg = carregar_config()
    hoje = dt.date.today().strftime("%Y%m%d")
    filtro = set(args.somente.split(",")) if args.somente else None

    fontes, log = [], []
    for serie in cfg["series"]:
        sid = serie["id"]
        if filtro and sid not in filtro:
            continue
        try:
            df = extrair(serie, cfg, hoje)
            anos = f"{df['ano'].min()}–{df['ano'].max()}" if len(df) else "—"
            status, erro = "ok", ""
            print(f"[ok]   {sid:<26} {len(df):>5} obs  {anos}")
        except Exception as exc:  # noqa: BLE001
            anos, status, erro = "—", "erro", str(exc)
            print(f"[ERRO] {sid:<26} {exc}")

        log.append({"id": sid, "status": status, "erro": erro, "data": hoje})
        if status == "ok":
            data_acesso = dt.date.today().isoformat()
            if serie["fonte"] == "manual":   # nas manuais a data está em cada linha
                data_acesso = "ver coluna data_acesso do arquivo"
            fontes.append({
                "id": sid,
                "bloco": serie["bloco"],
                "dimensao": serie["dimensao"],
                "definicao": serie["definicao"],
                "unidade": serie["unidade"],
                "periodo_utilizado": anos,
                "instituicao": serie["instituicao"],
                "link": serie["link"],
                "codigo_serie": serie.get("codigo", "—"),
                "data_acesso": data_acesso,
                "ajustes": serie.get("ajuste", "Nenhum"),
            })

    pd.DataFrame(fontes).to_csv(PROC / "fontes.csv", index=False)
    pd.DataFrame(log).to_csv(PROC / "log_extracao.csv", index=False)
    print(f"\nTabela de fontes: {PROC / 'fontes.csv'}")


if __name__ == "__main__":
    main()
