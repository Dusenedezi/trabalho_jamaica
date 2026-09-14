"""Extrator para o CSV de séries temporais dos índices compostos do HDR (UNDP).

O arquivo é largo: uma linha por país, colunas como hdi_1990 ... hdi_2023.
Atenção: o arquivo também traz colunas hdi_rank_AAAA, hdi_f_AAAA e hdi_m_AAAA
(ranking e IDH por sexo); por isso a seleção usa o padrão exato <indicador>_AAAA.
A função converte para formato longo (iso3, ano, valor) para o indicador
pedido (ex.: 'hdi', 'le', 'eys', 'mys', 'gnipc').
"""
from __future__ import annotations

import io
import re
from pathlib import Path

import pandas as pd
import requests


def fetch(url_arquivo: str, indicador: str, countries: list[str]) -> tuple[str, pd.DataFrame]:
    resp = requests.get(url_arquivo, timeout=120)
    resp.raise_for_status()
    texto = resp.content.decode("utf-8", errors="replace")
    raw = pd.read_csv(io.StringIO(texto))

    # Somente <indicador>_<4 dígitos>; exclui hdi_rank_2023, hdi_f_1990, hdi_m_1990 etc.
    padrao = re.compile(rf"^{re.escape(indicador)}_\d{{4}}$")
    cols = [c for c in raw.columns if padrao.match(c)]
    if not cols:
        raise ValueError(f"Indicador '{indicador}' não encontrado no arquivo do HDR")

    sub = raw[raw["iso3"].isin(countries)][["iso3", "country"] + cols]
    df = sub.melt(id_vars=["iso3", "country"], var_name="ano", value_name="valor")
    df["ano"] = df["ano"].str.replace(f"{indicador}_", "", regex=False).astype(int)
    df = (df.rename(columns={"country": "pais"})
            .dropna(subset=["valor"])
            .sort_values(["iso3", "ano"])
            .reset_index(drop=True))
    return texto, df


def save_raw(texto: str, path: Path) -> None:
    path.write_text(texto, encoding="utf-8")
