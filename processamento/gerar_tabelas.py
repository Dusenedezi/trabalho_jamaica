"""Gera tabelas e fatos-chave em Markdown a partir dos CSVs de dados/processados/.

Somente leitura dos dados: nada é recalculado fora do que já está nos CSVs (e, por
trás deles, em dados/brutos/). País, comparadores, nomes e referência de
convergência vêm de config/series.yaml — nada fixo no código. Formatação pt-BR
(vírgula decimal, ponto de milhar) apenas nos .md; os CSVs continuam no formato
de máquina.

Adaptado do gerar_tabelas.py do projeto Japão (2026-09-12), que tinha país,
comparadores e nomes como constantes.

Uso:  python processamento/gerar_tabelas.py [--proc PASTA] [--out PASTA] [--fontes PASTA]
      (padrão: tudo em dados/processados/)
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load((RAIZ / "config" / "series.yaml").open(encoding="utf-8"))
PAIS, COMP, NOMES = CFG["pais"], CFG["comparadores"], CFG["nomes"]
REF = CFG.get("referencia_convergencia", COMP[0])
ORDEM = [PAIS] + COMP
ANOS = [1990, 1995, 2000, 2005, 2010, 2015, 2020]
CATALOGO = {s["id"]: s for s in CFG["series"]}
NOME_PAIS = NOMES.get(PAIS, PAIS)

# id -> (rótulo curto, casas decimais, fator aplicado ao valor do CSV, unidade exibida ou None = a do catálogo)
FORMATO = {
    "idh": ("IDH", 3, 1, None),
    "pib_pc_ppp": ("PIB per capita PPP", 0, 1, None),
    "pib_por_ocupado": ("PIB por pessoa ocupada", 0, 1, None),
    "hci": ("Human Capital Index", 3, 1, None),
    "energia_importada": ("Importações líquidas de energia", 1, 1, None),
    "divida_publica": ("Dívida do governo central", 1, 1, None),
    "wgi_rule_of_law": ("WGI Rule of Law", 2, 1, None),
    "solar_capacidade": ("Capacidade solar instalada", 1, 1, None),
    "solar_geracao_share": ("Solar na geração elétrica", 2, 1, None),
    "renovaveis_geracao_share": ("Renováveis na geração elétrica", 1, 1, None),
    "populacao": ("População", 2, 1e-6, "milhões de pessoas (valor ÷ 1e6)"),
}

ap = argparse.ArgumentParser()
ap.add_argument("--proc", default=str(RAIZ / "dados" / "processados"))
ap.add_argument("--out", default=str(RAIZ / "dados" / "processados"))
ap.add_argument("--fontes", default=str(RAIZ / "dados" / "processados"))
A = ap.parse_args()
PROC, OUT, FON = Path(A.proc), Path(A.out), Path(A.fontes)
OUT.mkdir(parents=True, exist_ok=True)

DATA_ACESSO = "?"
if (FON / "fontes.csv").exists():
    _f = pd.read_csv(FON / "fontes.csv")
    _d = [d for d in _f["data_acesso"].astype(str) if d[:4].isdigit()]
    DATA_ACESSO = max(_d) if _d else "?"
CAB = (f"> Gerado por `processamento/gerar_tabelas.py` em {dt.date.today().isoformat()} a partir de "
       f"`dados/processados/` (acesso às fontes em {DATA_ACESSO}). Números em formato pt-BR. "
       "Traço (—) = sem dado. Comparadores ausentes em uma fonte simplesmente não aparecem.\n\n")


def br(x, nd=1):
    """Formata número no padrão brasileiro."""
    if x is None or pd.isna(x):
        return "—"
    return f"{x:,.{nd}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def md(df, index_name=""):
    """DataFrame (já em strings) -> tabela Markdown."""
    header = [index_name] + [str(c) for c in df.columns]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for idx, row in df.iterrows():
        lines.append("| " + " | ".join([str(idx)] + [str(v) for v in row]) + " |")
    return "\n".join(lines)


def fmt(df, nd):
    return df.apply(lambda col: col.map(lambda v: br(v, nd)))


def existe(sid):
    return (PROC / f"{sid}.csv").exists()


def unidade(sid):
    return FORMATO[sid][3] or CATALOGO[sid]["unidade"]


def wide(sid):
    d = pd.read_csv(PROC / f"{sid}.csv")
    w = d.pivot(index="ano", columns="iso3", values="valor") * FORMATO[sid][2]
    w.columns.name = None
    return w[[c for c in ORDEM if c in w.columns]]


def ult_comum(w):
    """Último ano com dado para todos os países presentes na série.

    Se nenhum ano tem dado para todos (caso da dívida no WDI), usa o último ano com
    dado para o país; os demais aparecem como traço.
    """
    full = w.dropna()
    if len(full):
        return int(full.index.max())
    return int(w[PAIS].dropna().index.max())


def rank_pais(v):
    """Posição do país (1 = maior valor) entre os países com dado."""
    v = v.dropna()
    return int(v.rank(ascending=False)[PAIS]), len(v)


def nomes(df):
    df = df.copy()
    df.columns = [NOMES.get(c, c) for c in df.columns]
    return df


def anos_sel(w, ult):
    return [a for a in ANOS if a in w.index and a < ult] + [ult]


def nome(c):
    return NOMES.get(c, c)


SERIES = [sid for sid in FORMATO if existe(sid)]

# ---------------------------------------------------------------- 01 painel
rows = []
for sid in SERIES:
    rot, nd, _, _ = FORMATO[sid]
    w = wide(sid)
    ano = ult_comum(w)
    v = w.loc[ano]
    r = {"Indicador": f"{rot} ({unidade(sid)})", "Ano": ano}
    r.update({nome(c): (br(v[c], nd) if c in v.index else "—") for c in ORDEM})
    k, n = rank_pais(v)
    r[f"{NOME_PAIS} (1 = maior valor)"] = f"{k}º de {n}"
    rows.append(r)
t = pd.DataFrame(rows).set_index("Indicador")
(OUT / "01_painel_ultimo_ano_comum.md").write_text(
    "# Painel: todos os indicadores no último ano com dado para os países presentes\n\n" + CAB
    + "\"Último ano comum\" = último ano com dado para todos os países que a fonte cobre (mesmo critério de "
    "`transform.py`, função `ultimo_ano_comum`); por isso o ano varia entre indicadores. Quando nenhum ano tem "
    f"dado para todos os países (dívida no WDI), usa-se o último ano com dado para {NOME_PAIS}. A posição é só ordem "
    "de grandeza: em dívida e importações de energia, valor maior não é \"melhor\".\n\n"
    + md(t, "Indicador") + "\n", encoding="utf-8")

# ------------------------------------------------ 02 séries por país, anos selecionados
txt = "# Séries por país em anos selecionados\n\n" + CAB
for sid in SERIES:
    rot, nd, _, _ = FORMATO[sid]
    w = wide(sid)
    ult = ult_comum(w)
    anos = list(w.index) if sid == "hci" else anos_sel(w, ult)
    sub = nomes(w.loc[anos])
    cobertura = "; ".join(
        f"{nome(c)} {int(w[c].dropna().index.min())}–{int(w[c].dropna().index.max())}" for c in w.columns)
    txt += f"## {rot} ({unidade(sid)}) — `{sid}.csv`\n\n" + md(fmt(sub, nd), "Ano") + "\n\n"
    txt += "Cobertura por país (primeiro–último ano com dado): " + cobertura + ".\n\n"
(OUT / "02_series_por_pais_anos_selecionados.md").write_text(txt, encoding="utf-8")

# ----------------------------------------------------------- 03 país: marcos
rows = []
for sid in SERIES:
    rot, nd, _, _ = FORMATO[sid]
    s = wide(sid)[PAIS].dropna()
    r = {"Indicador": f"{rot} ({unidade(sid)})"}
    for a in ANOS:
        r[str(a)] = br(s.loc[a], nd) if a in s.index else "—"
    last = int(s.index.max())
    r["Último disponível"] = f"{br(s.loc[last], nd)} ({last})"
    rows.append(r)
(OUT / f"03_{PAIS.lower()}_marcos_temporais.md").write_text(
    f"# {NOME_PAIS}: valores em anos-marco\n\n" + CAB
    + md(pd.DataFrame(rows).set_index("Indicador"), "Indicador") + "\n", encoding="utf-8")


# ---------------------------------------------------------------- 04 derivados
def sel(df):
    ult = int(df.dropna(how="all").index.max())
    return df.loc[[a for a in ANOS if a in df.index and a < ult] + [ult]]


def ler_derivado(padrao):
    arqs = sorted(glob.glob(str(PROC / padrao)))
    if not arqs:
        return None, None
    d = pd.read_csv(arqs[-1], index_col=0)
    d = d[[c for c in ORDEM if c in d.columns]].dropna(axis=1, how="all")
    return d, Path(arqs[-1]).name


txt = "# Derivados calculados em `transform.py`\n\n" + CAB
pct, pct_nome = ler_derivado(f"pib_pc_ppp_pct_{REF.lower()}.csv")
if pct is not None:
    txt += (f"## PIB per capita PPP como % de {nome(REF)} (`{pct_nome}`)\n\n"
            f"Fórmula: valor do país ÷ valor de {nome(REF)} × 100, ano a ano "
            "(US$ internacionais constantes de 2021).\n\n" + md(fmt(nomes(sel(pct)), 1), "Ano") + "\n\n")
idx, idx_nome = ler_derivado("pib_por_ocupado_indice_*.csv")
if idx is not None:
    base = idx_nome.split("_")[-1].replace(".csv", "")
    txt += (f"## PIB por pessoa ocupada, índice {base} = 100 (`{idx_nome}`)\n\n"
            f"Fórmula: valor do ano ÷ valor de {base} × 100. Série em US$ PPP constantes de 2021, "
            "portanto o índice mede variação real.\n\n" + md(fmt(nomes(sel(idx)), 1), "Ano") + "\n\n")
kw, kw_nome = ler_derivado("solar_capacidade_kw_por_mil_hab.csv")
if kw is not None:
    txt += (f"## Capacidade solar por habitante, kW por 1.000 habitantes (`{kw_nome}`)\n\n"
            "Fórmula: capacidade (MW) ÷ população (SP.POP.TOTL) × 1.000.000.\n\n"
            + md(fmt(nomes(sel(kw)), 2), "Ano") + "\n\n")
if (PROC / "tabela_hci.csv").exists():
    hci_t = pd.read_csv(PROC / "tabela_hci.csv", index_col=0)
    txt += "## Human Capital Index, ano mais recente (`tabela_hci.csv`)\n\n" + md(fmt(hci_t, 3), "País") + "\n\n"
if (PROC / "tarifa_eletricidade_usd.csv").exists():
    tu = pd.read_csv(PROC / "tarifa_eletricidade_usd.csv", index_col=0)
    ROTULOS = {"media_sistema_usd_publicado": "Média do sistema, US$/kWh (publicado)",
               "media_sistema_jmd": "Média do sistema, J$/kWh",
               "residencial_jmd": "Residencial, J$/kWh",
               "cambio_jmd_por_usd": "Câmbio, J$ por US$ (PA.NUS.FCRF)",
               "media_sistema_usd_calc": "Média do sistema, US$/kWh (calculado)",
               "residencial_usd_calc": "Residencial, US$/kWh (calculado)"}
    txt += ("## Tarifa de eletricidade em US$ com o câmbio do WDI (`tarifa_eletricidade_usd.csv`)\n\n"
            "Fórmula: J$/kWh ÷ câmbio médio anual (PA.NUS.FCRF, série `cambio_jmd_usd`). A média do sistema "
            "recalculada serve para conferir o US$ publicado pelo MSETT (arredondado a 2 casas); 2015 não tem "
            "valor em J$ na fonte.\n\n" + md(fmt(tu.rename(columns=ROTULOS), 3), "Ano") + "\n")
(OUT / "04_derivados.md").write_text(txt, encoding="utf-8")

# -------------------------------------------------------------- 05 fatos-chave
F = ["# Fatos-chave (calculados a partir dos CSVs)\n", CAB,
     "Cada frase pode ser conferida no CSV citado. Interpretação e contexto ficam para o relatório.\n", "## País\n"]

if pct is not None and PAIS in pct.columns:
    jp = pct[PAIS].dropna()
    f0, pk, ul = int(jp.index.min()), int(jp.idxmax()), int(jp.index.max())
    outros = "; ".join(f"{nome(c)} {br(pct.loc[ul, c], 1)}%" for c in pct.columns
                       if c != PAIS and pd.notna(pct.loc[ul, c]))
    F.append(f"- **Convergência (`{pct_nome}`)**: o PIB per capita PPP de {NOME_PAIS} era {br(jp.loc[f0], 1)}% do de "
             f"{nome(REF)} em {f0}, atingiu o máximo de {br(jp.loc[pk], 1)}% em {pk} e chegou a {br(jp.loc[ul], 1)}% em {ul}. "
             f"Demais países em {ul} ({nome(REF)} = 100): {outros}.")

if "pib_pc_ppp" in SERIES:
    w = wide("pib_pc_ppp")
    s = w[PAIS].dropna()
    f0, ul = int(s.index.min()), int(s.index.max())

    def var(c):
        return br((w.loc[ul, c] / w.loc[f0, c] - 1) * 100, 1)

    uc = ult_comum(w)
    k, n = rank_pais(w.loc[uc])
    F.append(f"- **Nível (`pib_pc_ppp.csv`)**: {NOME_PAIS} US$ {br(s.loc[f0], 0)} ({f0}) → US$ {br(s.loc[ul], 0)} ({ul}), "
             f"variação de {var(PAIS)}% no período; {nome(REF)} {var(REF)}%. Em {uc}, {NOME_PAIS} é {k}º de {n} países.")

if "pib_por_ocupado" in SERIES:
    p = wide("pib_por_ocupado")
    up = ult_comum(p)
    v = p.loc[up].sort_values(ascending=False)
    k, n = rank_pais(v)
    top = v.index[0]
    F.append(f"- **Produtividade ({up}, `pib_por_ocupado.csv`)**: "
             + "; ".join(f"{nome(c)} {br(v[c], 0)}" for c in v.index)
             + f" US$ PPP por pessoa ocupada. {NOME_PAIS} em {k}º de {n}, com {br(v[PAIS] / v[top] * 100, 1)}% do nível de "
             f"{nome(top)} e {br(v[PAIS] / v[REF] * 100, 1)}% do de {nome(REF)}.")

if "idh" in SERIES:
    h = wide("idh")
    s = h[PAIS].dropna()
    f0, uh = int(s.index.min()), ult_comum(h)
    vh = h.loc[uh]
    k, n = rank_pais(vh)
    F.append(f"- **IDH (`idh.csv`)**: {NOME_PAIS} {br(s.loc[f0], 3)} ({f0}) → {br(vh[PAIS], 3)} ({uh}), {k}º de {n} em {uh}. "
             f"Maior: {nome(vh.idxmax())} {br(vh.max(), 3)}; menor: {nome(vh.idxmin())} {br(vh.min(), 3)}.")

if "hci" in SERIES:
    c = wide("hci")
    uc = int(c.index.max())
    vc = c.loc[uc].dropna().sort_values(ascending=False)
    k, n = rank_pais(vc)
    F.append(f"- **Capital humano (HCI {uc}, `hci.csv`)**: " + "; ".join(f"{nome(x)} {br(vc[x], 3)}" for x in vc.index)
             + f". {NOME_PAIS} em {k}º de {n}. Anos disponíveis: {', '.join(str(a) for a in c.index)}.")

if "energia_importada" in SERIES:
    e = wide("energia_importada")
    s = e[PAIS].dropna()
    ul = int(s.index.max())
    outros = "; ".join(f"{nome(x)} {br(e.loc[ul, x], 1)}%" for x in e.columns if x != PAIS and pd.notna(e.loc[ul, x]))
    F.append(f"- **Importações líquidas de energia ({ul}, `energia_importada.csv`)**: {NOME_PAIS} {br(s.loc[ul], 1)}% do uso de "
             f"energia (em {int(s.index.min())}: {br(s.iloc[0], 1)}%). Demais em {ul}: {outros}. Valores negativos = "
             "exportadores líquidos; acima de 100% ocorre quando há reexportação ou variação de estoques (definição do WDI).")

if "divida_publica" in SERIES:
    d = wide("divida_publica")
    s = d[PAIS].dropna()
    ul, pk = int(s.index.max()), int(s.idxmax())
    F.append(f"- **Dívida do governo central (`divida_publica.csv`)**: {NOME_PAIS} {br(s.loc[ul], 1)}% do PIB em {ul} "
             f"(máximo da série: {br(s.loc[pk], 1)}% em {pk}; em {int(s.index.min())}: {br(s.iloc[0], 1)}%). "
             "Comparadores com cobertura irregular no WDI (ver `verificacao.txt`).")

if "wgi_rule_of_law" in SERIES:
    g = wide("wgi_rule_of_law")
    ug = ult_comum(g)
    vg = g.loc[ug]
    k, n = rank_pais(vg)
    F.append(f"- **Rule of Law ({ug}, `wgi_rule_of_law.csv`)**: {NOME_PAIS} {br(vg[PAIS], 2)} ({k}º de {n}; em "
             f"{int(g.index.min())}: {br(g[PAIS].dropna().iloc[0], 2)}). Maior: {nome(vg.idxmax())} {br(vg.max(), 2)}; "
             f"menor: {nome(vg.idxmin())} {br(vg.min(), 2)}.")

if "populacao" in SERIES:
    po = wide("populacao")[PAIS].dropna()
    pko, upo = int(po.idxmax()), int(po.index.max())
    F.append(f"- **População (`populacao.csv`)**: {br(po.loc[upo], 2)} milhões em {upo}; máximo de {br(po.loc[pko], 2)} "
             f"milhões em {pko} ({br((po.loc[upo] / po.loc[pko] - 1) * 100, 1)}% desde o máximo).")

F.append("\n## Setor: energia solar e armazenamento\n")

if "solar_capacidade" in SERIES:
    sc = wide("solar_capacidade")
    s = sc[PAIS].dropna()
    ul = int(s.index.max())
    nz = s[s > 0]
    f1 = int(nz.index.min()) if len(nz) else None
    a2015 = br(s.loc[2015], 1) if 2015 in s.index else "—"
    v = sc.loc[ul]
    k, n = rank_pais(v)
    F.append(f"- **Capacidade solar instalada (`solar_capacidade.csv`)**: {NOME_PAIS} {br(s.loc[ul], 1)} MW em {ul} "
             f"({k}º de {n}); {a2015} MW em 2015; primeiro registro positivo em {f1}. Em {ul}: "
             + "; ".join(f"{nome(x)} {br(v[x], 1)}" for x in v.sort_values(ascending=False).index) + " MW.")
    if kw is not None and PAIS in kw.columns:
        vk = kw.loc[ul].dropna().sort_values(ascending=False)
        kk, nk = rank_pais(vk)
        F.append(f"- **Capacidade solar por habitante ({ul}, `{kw_nome}`)**: "
                 + "; ".join(f"{nome(x)} {br(vk[x], 2)}" for x in vk.index)
                 + f" kW por 1.000 hab. {NOME_PAIS} em {kk}º de {nk}.")

if "solar_geracao_share" in SERIES:
    ss = wide("solar_geracao_share")
    s = ss[PAIS].dropna()
    ul = int(s.index.max())
    um = s[s >= 1]
    f1 = int(um.index.min()) if len(um) else None
    v = ss.loc[ul].dropna().sort_values(ascending=False)
    F.append(f"- **Solar na geração elétrica (`solar_geracao_share.csv`)**: {NOME_PAIS} {br(s.loc[ul], 2)}% em {ul} "
             f"(máximo {br(s.max(), 2)}% em {int(s.idxmax())}; passa de 1% em {f1}). Em {ul}: "
             + "; ".join(f"{nome(x)} {br(v[x], 2)}%" for x in v.index) + ".")

if "renovaveis_geracao_share" in SERIES:
    rs = wide("renovaveis_geracao_share")
    s = rs[PAIS].dropna()
    ul = int(s.index.max())
    v = rs.loc[ul].dropna().sort_values(ascending=False)
    F.append(f"- **Renováveis na geração elétrica (`renovaveis_geracao_share.csv`)**: {NOME_PAIS} {br(s.loc[ul], 1)}% em {ul} "
             f"(máximo {br(s.max(), 1)}% em {int(s.idxmax())}; em {int(s.index.min())}: {br(s.iloc[0], 1)}%). Em {ul}: "
             + "; ".join(f"{nome(x)} {br(v[x], 1)}%" for x in v.index) + ".")

if existe("tarifa_eletricidade"):
    tf = pd.read_csv(PROC / "tarifa_eletricidade.csv").sort_values("ano")
    a0, a1 = tf.iloc[0], tf.iloc[-1]
    mx = tf.loc[tf["valor"].idxmax()]
    F.append(f"- **Tarifa média de eletricidade (`tarifa_eletricidade.csv`, tabela manual)**: US$ {br(a0['valor'], 2)}/kWh em "
             f"{int(a0['ano'])} → US$ {br(a1['valor'], 2)}/kWh em {int(a1['ano'])}; máximo US$ {br(mx['valor'], 2)}/kWh em "
             f"{int(mx['ano'])}. Segmento: {a1['segmento']}. Fonte de cada linha na própria tabela.")

if (PROC / "tarifa_eletricidade_usd.csv").exists():
    tu = pd.read_csv(PROC / "tarifa_eletricidade_usd.csv", index_col=0)
    r = tu["residencial_usd_calc"].dropna()
    if len(r):
        ul, pk = int(r.index.max()), int(r.idxmax())
        F.append(f"- **Tarifa residencial em US$ (`tarifa_eletricidade_usd.csv`, câmbio PA.NUS.FCRF)**: US$ {br(r.loc[ul], 3)}/kWh "
                 f"em {ul} (máximo US$ {br(r.loc[pk], 3)} em {pk}; em {int(r.index.min())}: US$ {br(r.iloc[0], 3)}). "
                 f"Média do sistema recalculada em {ul}: US$ {br(tu.loc[ul, 'media_sistema_usd_calc'], 3)}, contra "
                 f"US$ {br(tu.loc[ul, 'media_sistema_usd_publicado'], 2)} publicado pelo MSETT.")

if existe("armazenamento_projetos"):
    ar = pd.read_csv(PROC / "armazenamento_projetos.csv").sort_values("ano")
    itens = "; ".join(f"{r['projeto']} — {br(r['mw'], 1) if pd.notna(r['mw']) else '—'} MW / {br(r['mwh'], 1)} MWh, "
                      f"{r['status']} ({int(r['ano'])})" for _, r in ar.iterrows())
    F.append(f"- **Armazenamento em baterias (`armazenamento_projetos.csv`, tabela manual)**: {len(ar)} registros: {itens}.")

(OUT / "05_fatos_chave.md").write_text("\n".join(F) + "\n", encoding="utf-8")

# ------------------------------------------------------- 06 tabelas manuais legíveis
txt = "# Tabelas manuais (tarifa e armazenamento)\n\n" + CAB
if existe("tarifa_eletricidade"):
    tf = pd.read_csv(PROC / "tarifa_eletricidade.csv").sort_values("ano")
    t = pd.DataFrame({
        "Ano": tf["ano"].astype(int),
        "US$/kWh": tf["valor"].map(lambda v: br(v, 2)),
        "Valor original": [f"{br(v, 2)} {m}" for v, m in zip(tf["valor_original"], tf["moeda_original"])],
        "Residencial (J$/kWh)": tf["residencial_jmd_por_kwh"].map(lambda v: br(v, 2)),
        "Fonte": tf["fonte"], "Link": tf["link"], "Acesso": tf["data_acesso"],
    }).set_index("Ano")
    txt += "## Tarifa média de eletricidade (`tarifa_eletricidade.csv`)\n\n" + md(t, "Ano") + "\n\n"
    txt += "Observações por linha (coluna `observacao` do CSV):\n\n" + "\n".join(
        f"- {int(a)}: {o}" for a, o in zip(tf["ano"], tf["observacao"])) + "\n\n"
if existe("armazenamento_projetos"):
    ar = pd.read_csv(PROC / "armazenamento_projetos.csv").sort_values("ano")
    t = pd.DataFrame({
        "Projeto": ar["projeto"], "Ano": ar["ano"].astype(int),
        "MW": ar["mw"].map(lambda v: br(v, 1)), "MWh": ar["mwh"].map(lambda v: br(v, 1)),
        "Operador": ar["operador"], "Status": ar["status"], "Fonte": ar["fonte"], "Link": ar["link"],
        "Acesso": ar["data_acesso"],
    }).set_index("Projeto")
    txt += "## Projetos de armazenamento (`armazenamento_projetos.csv`)\n\n" + md(t, "Projeto") + "\n\n"
    txt += "Observações por linha:\n\n" + "\n".join(
        f"- {p}: {o}" for p, o in zip(ar["projeto"], ar["observacao"])) + "\n"
(OUT / "06_tabelas_manuais.md").write_text(txt, encoding="utf-8")

# ------------------------------------------------------- fontes.md (legível)
if (FON / "fontes.csv").exists():
    f = pd.read_csv(FON / "fontes.csv")
    txt = ("# Tabela de fontes (versão legível de `fontes.csv`)\n\n"
           "> Gerada automaticamente por `run_all.py` a partir de `config/series.yaml`; este .md é só uma reformatação. "
           "Campos exigidos pelo enunciado: definição, unidade, período, instituição, link, código, data de acesso e ajustes.\n\n")
    CAMPOS = [("bloco", "Bloco"), ("dimensao", "Dimensão"), ("definicao", "Definição"), ("unidade", "Unidade"),
              ("periodo_utilizado", "Período utilizado"), ("instituicao", "Instituição"), ("link", "Link"),
              ("codigo_serie", "Código da série"), ("data_acesso", "Data de acesso"), ("ajustes", "Ajustes")]
    for _, r in f.iterrows():
        txt += f"## `{r['id']}` — {r['definicao']}\n\n| Campo | Valor |\n|---|---|\n"
        for k, lab in CAMPOS:
            txt += f"| {lab} | {r[k]} |\n"
        txt += "\n"
    (FON / "fontes.md").write_text(txt, encoding="utf-8")

print("ok:", sorted(x.name for x in OUT.glob("0*.md")), "+ fontes.md")
