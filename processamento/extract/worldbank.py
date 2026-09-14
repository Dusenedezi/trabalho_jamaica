"""Extrator para a API v2 do Banco Mundial (WDI: source=2; WGI: source=3).

Documentação: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests

BASE = "https://api.worldbank.org/v2"


def fetch(indicator: str, countries: list[str], start: int, end: int,
          source_id: int = 2) -> tuple[list[dict], pd.DataFrame]:
    """Retorna (payload bruto, DataFrame tidy) para um indicador."""
    url = f"{BASE}/country/{';'.join(countries)}/indicator/{indicator}"
    params = {
        "format": "json",
        "per_page": 20000,
        "date": f"{start}:{end}",
        "source": source_id,
    }
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    payload = resp.json()

    if len(payload) < 2 or payload[1] is None:
        raise RuntimeError(f"Sem dados para {indicator}: {payload[0]}")

    registros = payload[1]
    df = pd.DataFrame(
        {
            "iso3": r["countryiso3code"],
            "pais": r["country"]["value"],
            "ano": int(r["date"]),
            "valor": r["value"],
        }
        for r in registros
    )
    df = df.dropna(subset=["valor"]).sort_values(["iso3", "ano"]).reset_index(drop=True)
    return registros, df


def save_raw(payload: list[dict], path: Path) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
