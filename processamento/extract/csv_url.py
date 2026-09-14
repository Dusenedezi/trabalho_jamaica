"""Extrator genérico para CSVs públicos acessíveis por URL (IRENA, Ember, OWID...).

A entrada do catálogo declara:
  url_csv      URL de download direto do arquivo
  mapeamento   {pais: <coluna>, ano: <coluna>, valor: <coluna>}
  tipo_pais    'iso3' (coluna já traz o código) ou 'nome' (converte por nomes_fonte)
  filtros      {coluna: valor} aplicados antes do recorte (ex.: Variable = Solar)
  nomes_fonte  opcional, {nome na fonte: iso3} quando tipo_pais = 'nome'
  fator        opcional, multiplica o valor (ex.: 1000 para converter GW em MW)

O período do catálogo (periodo.inicio/fim) é aplicado ao recorte, como no
extrator do Banco Mundial. O arquivo é salvo íntegro em dados/brutos/; o
recorte vira o tidy padrão.
"""
from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import requests


def fetch(serie: dict, countries: list[str], start: int | None = None,
          end: int | None = None) -> tuple[str, pd.DataFrame]:
    url = serie.get("url_csv", "")
    if not url or url.startswith("COLE_AQUI"):
        raise ValueError(f"url_csv não preenchida para {serie['id']}")

    resp = requests.get(url, timeout=180)
    resp.raise_for_status()
    texto = resp.content.decode("utf-8-sig", errors="replace")
    raw = pd.read_csv(io.StringIO(texto), low_memory=False)

    m = serie["mapeamento"]
    faltando = [c for c in m.values() if c not in raw.columns]
    if faltando:
        raise KeyError(f"{serie['id']}: colunas {faltando} não existem; colunas disponíveis: {list(raw.columns)[:20]}")

    df = raw
    for col, val in (serie.get("filtros") or {}).items():
        if col not in df.columns:
            raise KeyError(f"{serie['id']}: coluna de filtro '{col}' não existe")
        df = df[df[col].astype(str) == str(val)]
    if df.empty:
        raise ValueError(f"{serie['id']}: nenhum registro após os filtros {serie.get('filtros')}")

    df = df.rename(columns={m["pais"]: "iso3", m["ano"]: "ano", m["valor"]: "valor"})[["iso3", "ano", "valor"]]

    if serie.get("tipo_pais", "iso3") == "nome":
        conv = serie.get("nomes_fonte") or {}
        df["iso3"] = df["iso3"].map(conv)

    df = df[df["iso3"].isin(countries)].copy()
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype("Int64")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.dropna(subset=["ano", "valor"])
    if start is not None:
        df = df[df["ano"] >= start]
    if end is not None:
        df = df[df["ano"] <= end]

    fator = float(serie.get("fator", 1) or 1)
    if fator != 1:
        df["valor"] = df["valor"] * fator

    df["pais"] = df["iso3"]
    df = df[["iso3", "pais", "ano", "valor"]].sort_values(["iso3", "ano"]).reset_index(drop=True)
    if df.empty:
        raise ValueError(f"{serie['id']}: nenhum país do grupo encontrado após o recorte")
    return texto, df


def save_raw(texto: str, path: Path) -> None:
    path.write_text(texto, encoding="utf-8")
