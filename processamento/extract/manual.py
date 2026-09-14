"""Extrator para tabelas compiladas à mão (dados/manuais/*.csv).

Serve para dados que só existem em relatórios (tarifa de eletricidade, projetos de
armazenamento). Não há download: o arquivo é lido, validado e copiado para
dados/brutos/ com a data, para manter a mesma rastreabilidade das demais séries.

Colunas obrigatórias: iso3, ano, valor, fonte, link, data_acesso.
Colunas livres adicionais são mantidas (ex.: projeto, mw, mwh, status, observacao).
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

OBRIGATORIAS = ["iso3", "ano", "valor", "fonte", "link", "data_acesso"]


def fetch(serie: dict, raiz: Path) -> tuple[Path, pd.DataFrame]:
    caminho = raiz / serie["arquivo"]
    if not caminho.exists():
        raise FileNotFoundError(f"{serie['id']}: crie {serie['arquivo']} com as colunas {OBRIGATORIAS}")

    df = pd.read_csv(caminho)
    faltando = [c for c in OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise KeyError(f"{serie['id']}: faltam colunas {faltando} em {serie['arquivo']}")

    vazios = df[OBRIGATORIAS].isna().any(axis=1)
    if vazios.any():
        raise ValueError(f"{serie['id']}: {int(vazios.sum())} linha(s) sem fonte/link/data em {serie['arquivo']}")

    df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype("Int64")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.dropna(subset=["ano"])
    if "pais" not in df.columns:
        df.insert(1, "pais", df["iso3"])
    df = df.sort_values(["iso3", "ano"]).reset_index(drop=True)
    return caminho, df


def save_raw(caminho: Path, destino: Path) -> None:
    shutil.copyfile(caminho, destino)
