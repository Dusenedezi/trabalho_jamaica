"""Transformações e figuras — roda depois de run_all.py.

Nada de país fixo aqui: pais, comparadores, nomes e referência de convergência
vêm de config/series.yaml. Cada figura corresponde a um indicador do PDF.

Uso:  python processamento/transform.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from matplotlib.ticker import MaxNLocator

RAIZ = Path(__file__).resolve().parents[1]
PROC = RAIZ / "dados" / "processados"
FIG = RAIZ / "figuras"

CFG = yaml.safe_load((RAIZ / "config" / "series.yaml").open(encoding="utf-8"))
PAIS = CFG["pais"]
COMP = CFG["comparadores"]
NOMES = CFG["nomes"]
REF = CFG.get("referencia_convergencia", COMP[0])
COR_PAIS, COR_OUTROS = "#c0392b", "#7f8c8d"

plt.rcParams.update({"figure.dpi": 150, "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False})


def ler(sid: str) -> pd.DataFrame:
    return pd.read_csv(PROC / f"{sid}.csv")


def wide(df: pd.DataFrame) -> pd.DataFrame:
    w = df.pivot(index="ano", columns="iso3", values="valor")
    w.columns.name = None
    return w


def existe(sid: str) -> bool:
    return (PROC / f"{sid}.csv").exists()


def ultimo_ano_comum(w: pd.DataFrame) -> int:
    return int(w.dropna().index.max())


def salvar(fig, nome: str) -> None:
    fig.tight_layout()
    fig.savefig(FIG / nome, bbox_inches="tight")   # inclui a legenda externa no recorte
    plt.close(fig)


def linhas(w: pd.DataFrame, cols: list[str], ax, destaque: str = PAIS,
           legenda_fora: bool = True) -> None:
    """Plota as colunas em cinza e o país em vermelho, por cima.

    legenda_fora=True põe a legenda à direita do gráfico para não cobrir as linhas
    (ajuste só de renderização, 2026-09-14); o painel duplo de fig_setor usa False.
    """
    for c in cols:
        if c not in w.columns or c == destaque:
            continue
        ax.plot(w.index, w[c], color=COR_OUTROS, lw=1, alpha=0.8, label=NOMES.get(c, c))
    if destaque in w.columns:
        ax.plot(w.index, w[destaque], color=COR_PAIS, lw=2, label=NOMES.get(destaque, destaque))
    if legenda_fora:
        ax.legend(fontsize=7, frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    else:
        ax.legend(fontsize=7, frameon=False)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))


# ------------------------------------------------------------ transformações

def razao_vs_referencia(sid: str, ref: str = REF) -> pd.DataFrame:
    w = wide(ler(sid))
    out = (w.div(w[ref], axis=0) * 100).drop(columns=ref)
    out.to_csv(PROC / f"{sid}_pct_{ref.lower()}.csv")
    return out


def indice_base(sid: str, ano_base: int | None = None) -> pd.DataFrame:
    w = wide(ler(sid))
    ano_base = ano_base or int(w.dropna().index.min())
    out = w.div(w.loc[ano_base]) * 100
    out.to_csv(PROC / f"{sid}_indice_{ano_base}.csv")
    return out


def por_habitante(sid: str, fator: float, sufixo: str) -> pd.DataFrame:
    num, pop = wide(ler(sid)), wide(ler("populacao"))
    out = (num / pop * fator).dropna(how="all")
    out.to_csv(PROC / f"{sid}_{sufixo}.csv")
    return out


# -------------------------------------------------------------------- figuras

def fig_idh() -> None:
    w = wide(ler("idh"))
    fig, ax = plt.subplots(figsize=(6, 3.4))
    linhas(w, [PAIS] + [c for c in COMP if c in w.columns], ax)
    ax.set_ylabel("IDH")
    ax.set_title(f"Índice de Desenvolvimento Humano, {w.index.min()}–{w.index.max()}")
    salvar(fig, "fig_idh.png")


def fig_convergencia() -> None:
    r = razao_vs_referencia("pib_pc_ppp")
    fig, ax = plt.subplots(figsize=(6, 3.4))
    linhas(r, [PAIS] + [c for c in COMP if c in r.columns], ax)
    ax.axhline(100, color="gray", lw=0.8, ls="--")
    ax.set_ylabel(f"PIB per capita PPP\n({NOMES[REF]} = 100)")   # duas linhas: rótulo longo cortava no topo
    ax.set_title(f"Convergência: {NOMES[PAIS]} em relação a {NOMES[REF]}")
    salvar(fig, "fig_convergencia.png")


def fig_produtividade() -> None:
    w = wide(ler("pib_por_ocupado"))
    ano = ultimo_ano_comum(w)
    s = w.loc[ano].rename(NOMES).sort_values()
    cores = [COR_PAIS if n == NOMES[PAIS] else COR_OUTROS for n in s.index]
    fig, ax = plt.subplots(figsize=(6, 3.4))
    s.plot.barh(ax=ax, color=cores)
    ax.set_xlabel(f"PIB por pessoa ocupada, US$ PPP constantes de 2021 ({ano})")
    ax.set_ylabel("")
    ax.set_title("Produtividade do trabalho")
    salvar(fig, "fig_produtividade.png")
    indice_base("pib_por_ocupado")


def tabela_capital_humano() -> pd.DataFrame:
    w = wide(ler("hci"))
    ano = int(w.index.max())
    t = w.loc[ano].dropna().rename(NOMES).sort_values(ascending=False).to_frame(f"HCI_{ano}")
    t.index.name = "pais"
    t.to_csv(PROC / "tabela_hci.csv")
    return t


def fig_quinta_dimensao() -> None:
    """Uma linha por candidato disponível; o PDF usa o que o aluno escolher."""
    for sid, rotulo in [("energia_importada", "Importações líquidas de energia, % do uso"),
                        ("divida_publica", "Dívida do governo central, % do PIB"),
                        ("wgi_rule_of_law", "Rule of Law (escore WGI)")]:
        if not existe(sid):
            continue
        w = wide(ler(sid))
        fig, ax = plt.subplots(figsize=(6, 3.4))
        linhas(w, [PAIS] + [c for c in COMP if c in w.columns], ax)
        ax.set_ylabel(rotulo)
        ax.set_title(f"{rotulo}, {w.index.min()}–{w.index.max()}")
        salvar(fig, f"fig_{sid}.png")


def fig_setor() -> None:
    """Esquerda: capacidade solar instalada; direita: participação do solar e das renováveis."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
    if existe("solar_capacidade"):
        w = wide(ler("solar_capacidade"))
        linhas(w, [PAIS] + [c for c in COMP if c in w.columns], a1, legenda_fora=False)
        a1.set_title("Capacidade solar instalada (MW)")
        por_habitante("solar_capacidade", 1e6, "kw_por_mil_hab")  # MW × 1e3 kW × 1e3 hab. / população
    if existe("solar_geracao_share"):
        s = wide(ler("solar_geracao_share"))[PAIS]
        a2.plot(s.index, s, color=COR_PAIS, lw=2, label="Solar")
    if existe("renovaveis_geracao_share"):
        r = wide(ler("renovaveis_geracao_share"))[PAIS]
        a2.plot(r.index, r, color=COR_OUTROS, lw=1.5, label="Renováveis (total)")
    a2.set_title(f"{NOMES[PAIS]}: participação na geração elétrica (%)")
    a2.legend(fontsize=7, frameon=False)
    a2.xaxis.set_major_locator(MaxNLocator(integer=True))
    salvar(fig, "fig_setor.png")


def tabelas_manuais() -> None:
    """Copia as tabelas manuais para versões prontas de leitura (uma linha por registro)."""
    for sid in ["tarifa_eletricidade", "armazenamento_projetos"]:
        if existe(sid):
            ler(sid).to_csv(PROC / f"tabela_{sid}.csv", index=False)


def tarifa_em_dolar() -> pd.DataFrame | None:
    """Converte a tarifa manual (J$/kWh) em US$/kWh com o câmbio médio anual do WDI (PA.NUS.FCRF).

    Saída: tarifa_eletricidade_usd.csv — média do sistema publicada em US$, valores em J$,
    câmbio, média recalculada (conferência do valor publicado) e residencial em US$.
    Decisão de 2026-09-14; só roda se as duas séries existirem.
    """
    if not (existe("tarifa_eletricidade") and existe("cambio_jmd_usd")):
        return None
    t = ler("tarifa_eletricidade")
    t = t[t["iso3"] == PAIS].set_index("ano").sort_index()
    fx = wide(ler("cambio_jmd_usd"))[PAIS]
    out = pd.DataFrame({
        "media_sistema_usd_publicado": t["valor"],
        "media_sistema_jmd": t["valor_original"].where(t["moeda_original"] == "JMD/kWh"),
        "residencial_jmd": t["residencial_jmd_por_kwh"],
        "cambio_jmd_por_usd": fx.reindex(t.index),
    })
    out["media_sistema_usd_calc"] = out["media_sistema_jmd"] / out["cambio_jmd_por_usd"]
    out["residencial_usd_calc"] = out["residencial_jmd"] / out["cambio_jmd_por_usd"]
    out.to_csv(PROC / "tarifa_eletricidade_usd.csv")
    return out


def main() -> None:
    fig_idh()
    fig_convergencia()
    fig_produtividade()
    tabela_capital_humano()
    fig_quinta_dimensao()
    fig_setor()
    tabelas_manuais()
    tarifa_em_dolar()
    print(f"Figuras em {FIG}")


if __name__ == "__main__":
    main()
