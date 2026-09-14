"""Verificação dos CSVs processados — roda depois de run_all.py.

Para cada série do catálogo: observações, primeiro e último ano, número de
países, valor do país no último ano, faixa de valores; sinaliza duplicatas,
comparadores ausentes, lacunas, valores fora de escala. Ao final, sorteia três
valores e confere contra os arquivos de dados/brutos/ (seed fixo).

Uso:  python processamento/verificar.py   (saída também em dados/processados/verificacao.txt)
"""
from __future__ import annotations

import glob
import io
import json
import random
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[1]
PROC, BRUTOS = RAIZ / "dados" / "processados", RAIZ / "dados" / "brutos"
CFG = yaml.safe_load((RAIZ / "config" / "series.yaml").open(encoding="utf-8"))
PAIS = CFG["pais"]
PAISES = [PAIS] + CFG["comparadores"]
SAIDA: list[str] = []


def out(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    SAIDA.append(s)


def valor_bruto(serie: dict, iso3: str, ano: int, bruto: Path):
    """Relê o arquivo bruto com a mesma regra do extrator e devolve o valor."""
    f = serie["fonte"]
    if f == "worldbank":
        recs = json.load(open(bruto, encoding="utf-8"))
        hit = [r for r in recs if r["countryiso3code"] == iso3 and int(r["date"]) == ano]
        return hit[0]["value"] if hit else None
    if f == "undp":
        raw = pd.read_csv(bruto, encoding="utf-8", encoding_errors="replace")
        col = f"{serie['codigo']}_{ano}"
        return float(raw.loc[raw["iso3"] == iso3, col].iloc[0])
    if f == "csv_url":
        raw = pd.read_csv(bruto, low_memory=False)
        m = serie["mapeamento"]
        sub = raw
        for c, v in (serie.get("filtros") or {}).items():
            sub = sub[sub[c].astype(str) == str(v)]
        sub = sub[(sub[m["pais"]] == iso3) & (pd.to_numeric(sub[m["ano"]], errors="coerce") == ano)]
        if sub.empty:
            return None
        return float(sub[m["valor"]].iloc[0]) * float(serie.get("fator", 1) or 1)
    if f == "manual":
        raw = pd.read_csv(bruto)
        sub = raw[(raw["iso3"] == iso3) & (raw["ano"] == ano)]
        return float(sub["valor"].iloc[0]) if len(sub) else None
    return None


def main() -> None:
    rows, flags = [], []
    for s in CFG["series"]:
        sid = s["id"]
        arq = PROC / f"{sid}.csv"
        if not arq.exists():
            flags.append(f"{sid}: CSV processado ausente (ver log_extracao.csv)")
            continue
        df = pd.read_csv(arq)
        p = df[df.iso3 == PAIS].sort_values("ano")
        ult = p.iloc[-1] if len(p) else None
        rows.append({
            "id": sid, "obs": len(df), "ano_ini": int(df.ano.min()), "ano_fim": int(df.ano.max()),
            "paises": df.iso3.nunique(),
            f"{PAIS}_ult_ano": int(ult.ano) if ult is not None else None,
            f"{PAIS}_ult_valor": float(ult.valor) if ult is not None and pd.notna(ult.valor) else None,
            "min": float(df.valor.min()), "max": float(df.valor.max()), "unidade": s["unidade"],
        })
        if s["fonte"] == "manual":
            continue  # tabelas manuais: uma linha por registro, sem painel país-ano
        if df.duplicated(["iso3", "ano"]).any():
            flags.append(f"{sid}: DUPLICATAS (iso3, ano)")
        falt = sorted(set(PAISES) - set(df.iso3))
        if falt:
            flags.append(f"{sid}: comparadores ausentes {falt}")
        for iso, g in df.groupby("iso3"):
            anos = sorted(g.ano)
            esperado = set(range(anos[0], anos[-1] + 1))
            miss = sorted(esperado - set(anos))
            if miss and sid != "hci":
                txt = ", ".join(map(str, miss)) if len(miss) <= 8 else f"{len(miss)} anos"
                flags.append(f"{sid}: {iso} cobre {anos[0]}–{anos[-1]} sem {txt}")
            if anos[-1] < int(df.ano.max()) - 1:
                flags.append(f"{sid}: {iso} termina em {anos[-1]} (série vai até {int(df.ano.max())})")
        if df.valor.isna().any():
            flags.append(f"{sid}: valores NaN")
        u = s["unidade"]
        if "Índice 0" in u and (df.valor.min() < 0 or df.valor.max() > 1):
            flags.append(f"{sid}: fora de 0–1")
        if "2,5" in u and df.valor.abs().max() > 2.5:
            flags.append(f"{sid}: |valor| > 2,5")
        if u.startswith("% da geração") and (df.valor.min() < 0 or df.valor.max() > 100):
            flags.append(f"{sid}: fora de 0–100%")
        if sid == "energia_importada" and df.valor.min() < 0:
            neg = sorted(df[df.valor < 0].iso3.unique())
            flags.append(f"{sid}: valores negativos (exportadores líquidos de energia) em {neg}")
        if (df.valor < 0).any() and sid not in ("wgi_rule_of_law", "energia_importada"):
            flags.append(f"{sid}: valores negativos")

    tab = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    out("=== RESUMO POR SÉRIE ===")
    out(tab.to_string(index=False, float_format=lambda x: f"{x:,.4f}"))
    out("\n=== SINALIZAÇÕES ===")
    out("\n".join(flags) if flags else "nenhuma")

    out("\n=== CONFERÊNCIA ALEATÓRIA CONTRA OS BRUTOS (seed 20260914) ===")
    rng = random.Random(20260914)
    candidatos = [s for s in CFG["series"] if s["id"] != "populacao" and (PROC / f"{s['id']}.csv").exists()]
    for s in rng.sample(candidatos, 3):
        sid = s["id"]
        df = pd.read_csv(PROC / f"{sid}.csv")
        r = df.iloc[rng.randrange(len(df))]
        bruto = Path(sorted(glob.glob(str(BRUTOS / f"{sid}_*.*")))[-1])
        rv = valor_bruto(s, r.iso3, int(r.ano), bruto)
        ok = rv is not None and abs(float(r.valor) - float(rv)) < 1e-6
        out(f"{sid:<26} {r.iso3} {int(r.ano)}: processado={float(r.valor)!r:<22} bruto={rv!r:<22} arquivo={bruto.name}  -> {'OK' if ok else 'DIVERGE'}")

    out("\n=== fontes.csv ===")
    f = pd.read_csv(PROC / "fontes.csv")
    out(f[["id", "periodo_utilizado", "codigo_serie", "data_acesso"]].to_string(index=False))
    out("\n=== log_extracao.csv ===")
    out(pd.read_csv(PROC / "log_extracao.csv").to_string(index=False))
    (PROC / "verificacao.txt").write_text("\n".join(SAIDA) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
