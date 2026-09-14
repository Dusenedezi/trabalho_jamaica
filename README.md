# AM1 — Jamaica / energia solar e armazenamento

Pipeline reprodutível para a Atividade Monitorada 1 (Economias Emergentes, FGV EAESP), replicado do
projeto Japão/tecnologia com três mudanças: país, comparadores, nomes e referência de convergência
vivem em `config/series.yaml` (nada fixo no código); um extrator genérico de CSV por URL cobre
IRENA/Ember; um extrator "manual" trata tabelas que só existem em relatórios locais.

## Estrutura

```
config/series.yaml          catálogo: país, comparadores, nomes e uma entrada por série
processamento/
  run_all.py                baixa tudo, salva bruto + tidy, gera fontes.csv e log_extracao.csv
  transform.py              derivados e figuras (lê o país e os comparadores do catálogo)
  verificar.py              resumo por série, sinalizações e conferência contra os brutos (verificacao.txt)
  gerar_tabelas.py          tabelas e fatos-chave em Markdown (01_...06_*.md e fontes.md em dados/processados/)
  extract/                  worldbank.py, undp.py, csv_url.py, manual.py
dados/manuais/              CSVs compilados à mão (tarifa, projetos de armazenamento)
dados/brutos/               payloads originais com data no nome (não editar)
dados/processados/          CSVs tidy + tabela de fontes + derivados
figuras/                    PNGs para o PDF
uso_de_ia_AM1.md            registro de uso de IA (vira PDF na entrega)
```

## Como rodar

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python processamento/run_all.py
python processamento/verificar.py
python processamento/transform.py
python processamento/gerar_tabelas.py
```

## Estado do catálogo (sessão Claude Code de 2026-09-14)

1. **IRENA (`solar_capacidade`)**: a IRENA não oferece URL de download direto em CSV (o IRENASTAT
   só responde CSV por POST e o irena.org bloqueia acesso automatizado). Usa-se a republicação do
   Our World in Data (`installed-solar-pv-capacity.csv`, em GW, convertida para MW pelo campo
   `fator: 1000`), conferida contra a API do IRENASTAT: valores iguais à soma PV on-grid + off-grid
   e CSP nula nos sete países. Detalhes no campo `ajuste` do catálogo.
2. **Ember (`solar_geracao_share`, `renovaveis_geracao_share`)**: em julho de 2026 o Ember trocou o
   formato do arquivo anual (`release_generation_yearly_global.csv`: uma linha por área, ano e
   fonte, métricas em colunas). Mapeamento e filtros do catálogo já refletem o novo cabeçalho.
3. **Tabelas manuais** em `dados/manuais/`: preenchidas com fontes oficiais (MSETT, OUR, IRP 2022,
   GPE) e imprensa especializada onde o documento da JPS não pôde ser lido (jpsco.com bloqueia
   acesso automatizado). Toda linha traz `fonte`, `link` e `data_acesso`; o extrator recusa o
   arquivo se faltar algum. Pendências listadas em `uso_de_ia_AM1.md`.
4. **Quinta dimensão**: decisão de 2026-09-14: o PDF usa `energia_importada` (ponte direta com a
   tese solar; Jamaica até 2022, Barbados sem dado). `divida_publica` e `wgi_rule_of_law` ficam no
   catálogo como apoio (dívida no WDI muito irregular entre comparadores; WGI completo, sem 1997,
   1999 e 2001). Alternativa para a dívida (FMI WEO, `GGXWDG_NGDP`) deixada como bloco comentado
   no catálogo, não ativada.
5. **Agregado LCN**: existe na API do Banco Mundial, mas não no HDR, no HCI, no WGI, no OWID nem no
   Ember; as figuras e tabelas ignoram automaticamente comparadores ausentes.
6. **Período**: `periodo.fim: 2025` (decisão de 2026-09-14) vale para todas as fontes; o extrator
   `csv_url` também aplica o recorte. O Banco Mundial devolve 2025 só onde já existe.
7. **Tarifa em US$**: a série auxiliar `cambio_jmd_usd` (WDI, `PA.NUS.FCRF`) converte a tabela
   manual de J$/kWh para US$/kWh em `transform.py` (`tarifa_eletricidade_usd.csv`, com a residencial
   em US$ e a média do sistema recalculada para conferir o valor publicado pelo MSETT).
8. **Armazenamento**: a composição do HESS de Hunts Bay segue a OUR (21 MW de baterias + 3,5 MW de
   flywheel); a do IRP 2022 fica registrada como divergente na coluna `observacao`.

## Correspondência com o enunciado

| Exigência | Onde está |
|---|---|
| Definição, unidade, período, instituição, link, código, data de acesso, ajustes | `dados/processados/fontes.csv` (gerada) + colunas de proveniência nas tabelas manuais |
| Dados brutos e processados | `dados/brutos/`, `dados/processados/` |
| Código de processamento | `processamento/` |
| Verificação (lacunas, escala, conferência contra brutos) | `dados/processados/verificacao.txt` (gerado por `verificar.py`) |
| Tabelas prontas para o texto | `dados/processados/01_*.md` a `06_*.md`, `fontes.md` (gerados por `gerar_tabelas.py`) |
| Registro de uso de IA | `uso_de_ia_AM1.md` → PDF |

Na entrega, renomear a pasta para `sobrenome_jamaica_AM1` e compactar.
