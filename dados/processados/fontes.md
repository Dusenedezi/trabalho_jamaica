# Tabela de fontes (versão legível de `fontes.csv`)

> Gerada automaticamente por `run_all.py` a partir de `config/series.yaml`; este .md é só uma reformatação. Campos exigidos pelo enunciado: definição, unidade, período, instituição, link, código, data de acesso e ajustes.

## `idh` — Índice de Desenvolvimento Humano (média geométrica dos índices de saúde, educação e renda)

| Campo | Valor |
|---|---|
| Bloco | pais |
| Dimensão | Nível de renda ou desenvolvimento |
| Definição | Índice de Desenvolvimento Humano (média geométrica dos índices de saúde, educação e renda) |
| Unidade | Índice 0–1 |
| Período utilizado | 1990–2023 |
| Instituição | UNDP – Human Development Report Data Center |
| Link | https://hdr.undp.org/data-center/documentation-and-downloads |
| Código da série | hdi |
| Data de acesso | 2026-09-14 |
| Ajustes | Filtro para os países do grupo de comparação (o agregado LCN não existe nesta fonte); colunas hdi_AAAA em formato longo |

## `pib_pc_ppp` — PIB per capita em paridade de poder de compra

| Campo | Valor |
|---|---|
| Bloco | pais |
| Dimensão | Crescimento ou convergência |
| Definição | PIB per capita em paridade de poder de compra |
| Unidade | US$ internacionais constantes de 2021 |
| Período utilizado | 1990–2025 |
| Instituição | Banco Mundial – World Development Indicators |
| Link | https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD |
| Código da série | NY.GDP.PCAP.PP.KD |
| Data de acesso | 2026-09-14 |
| Ajustes | Razão país/referência (x100) calculada em transform.py; referência definida em referencia_convergencia |

## `pib_por_ocupado` — PIB por pessoa ocupada (produtividade do trabalho)

| Campo | Valor |
|---|---|
| Bloco | pais |
| Dimensão | Produtividade ou transformação estrutural |
| Definição | PIB por pessoa ocupada (produtividade do trabalho) |
| Unidade | US$ internacionais constantes de 2021 (PPP) |
| Período utilizado | 1991–2025 |
| Instituição | Banco Mundial – WDI (origem: ILO, modelagem ILOSTAT) |
| Link | https://data.worldbank.org/indicator/SL.GDP.PCAP.EM.KD |
| Código da série | SL.GDP.PCAP.EM.KD |
| Data de acesso | 2026-09-14 |
| Ajustes | Barras: último ano com dado para todos os países; índice base = primeiro ano comum |

## `hci` — Human Capital Index: produtividade esperada aos 18 anos relativa ao benchmark de saúde e educação completas

| Campo | Valor |
|---|---|
| Bloco | pais |
| Dimensão | Capital humano, pobreza, desigualdade ou qualidade de vida |
| Definição | Human Capital Index: produtividade esperada aos 18 anos relativa ao benchmark de saúde e educação completas |
| Unidade | Índice 0–1 |
| Período utilizado | 2010–2020 |
| Instituição | Banco Mundial – Human Capital Index |
| Link | https://data.worldbank.org/indicator/HD.HCI.OVRL |
| Código da série | HD.HCI.OVRL |
| Data de acesso | 2026-09-14 |
| Ajustes | Nenhum; tabela com o ano mais recente. Só quatro anos (2010, 2017, 2018, 2020), não é série anual; Barbados e o agregado LCN não existem nesta fonte |

## `energia_importada` — Importações líquidas de energia como % do uso de energia

| Campo | Valor |
|---|---|
| Bloco | pais |
| Dimensão | Estabilidade macroeconômica, inserção internacional ou qualidade institucional |
| Definição | Importações líquidas de energia como % do uso de energia |
| Unidade | % |
| Período utilizado | 1990–2023 |
| Instituição | Banco Mundial – WDI (origem: IEA) |
| Link | https://data.worldbank.org/indicator/EG.IMP.CONS.ZS |
| Código da série | EG.IMP.CONS.ZS |
| Data de acesso | 2026-09-14 |
| Ajustes | Quinta dimensão escolhida para o PDF (decisão de 2026-09-14). Nenhum ajuste. Cobertura conferida em 2026-09-14: Jamaica 1990–2022 (sem 2005–2007); Barbados sem dado; República Dominicana só 2012–2022; demais 1990–2022/2023. Valores negativos = exportadores líquidos de energia (Colômbia, Trinidad e Tobago, agregado LCN) |

## `divida_publica` — Dívida do governo central, total

| Campo | Valor |
|---|---|
| Bloco | pais |
| Dimensão | Estabilidade macroeconômica, inserção internacional ou qualidade institucional |
| Definição | Dívida do governo central, total |
| Unidade | % do PIB |
| Período utilizado | 1990–2024 |
| Instituição | Banco Mundial – WDI (origem: FMI GFS) |
| Link | https://data.worldbank.org/indicator/GC.DOD.TOTL.GD.ZS |
| Código da série | GC.DOD.TOTL.GD.ZS |
| Data de acesso | 2026-09-14 |
| Ajustes | Nenhum. Cobertura no WDI conferida em 2026-09-14 e insuficiente para comparação: Jamaica 1990–2020 (sem 2018); Colômbia 1998–2024 com lacunas; Barbados 2005–2016; Costa Rica 1996–2001; República Dominicana 1996–1999; Trinidad e Tobago 2006–2007; Panamá sem dado; LCN 2019–2021. Alternativa proposta (não ativada): dívida bruta do governo geral do FMI WEO, GGXWDG_NGDP, ver bloco comentado abaixo |

## `wgi_rule_of_law` — Rule of Law (estimativa)

| Campo | Valor |
|---|---|
| Bloco | pais |
| Dimensão | Estabilidade macroeconômica, inserção internacional ou qualidade institucional |
| Definição | Rule of Law (estimativa) |
| Unidade | Escore padronizado, aprox. −2,5 a 2,5 |
| Período utilizado | 1996–2024 |
| Instituição | Banco Mundial – Worldwide Governance Indicators |
| Link | https://www.worldbank.org/en/publication/worldwide-governance-indicators |
| Código da série | GOV_WGI_RL.EST |
| Data de acesso | 2026-09-14 |
| Ajustes | Nenhum. Código atual da API (fonte 3) é GOV_WGI_RL.EST; o antigo RL.EST não existe mais na fonte 3 (só na fonte 57, WDI Database Archives). Sem dado em 1997, 1999 e 2001 (indicador bienal até 2002). O agregado LCN não existe no WGI |

## `solar_capacidade` — Capacidade instalada de geração solar (fotovoltaica; on-grid e off-grid)

| Campo | Valor |
|---|---|
| Bloco | setor |
| Dimensão | Setor – tamanho e trajetória (capacidade solar instalada) |
| Definição | Capacidade instalada de geração solar (fotovoltaica; on-grid e off-grid) |
| Unidade | MW |
| Período utilizado | 2000–2025 |
| Instituição | IRENA – Renewable Energy Statistics 2026 (republicação: Our World in Data, grapher 'installed-solar-pv-capacity', processado a partir de IRENA_Statistics_Extract_2026.xlsx; atualização do OWID em 2026-07-28) |
| Link | https://ourworldindata.org/grapher/installed-solar-pv-capacity |
| Código da série | OWID solar__total_gw (IRENA: Solar energy, on-grid + off-grid) |
| Data de acesso | 2026-09-14 |
| Ajustes | Arquivo do OWID em GW, convertido para MW (x1.000, campo fator). A série do OWID é 'solar total' (fotovoltaica + solar térmica de concentração, CSP); na API do IRENASTAT (tabela Country_ELECCAP_2026_H1, consulta em 2026-09-14) a CSP é nula nos sete países e os valores do OWID coincidem com a soma PV on-grid + off-grid da IRENA em todos os anos (diferença máxima 0,01 MW; única exceção Costa Rica 2012: 2,27 vs 1,36 MW). Recorte ao período do catálogo (2025 é o último ano da fonte). Capacidade por habitante (kW/1.000 hab.) calculada em transform.py com SP.POP.TOTL |

## `solar_geracao_share` — Participação da energia solar na geração elétrica

| Campo | Valor |
|---|---|
| Bloco | setor |
| Dimensão | Setor – participação do solar na geração elétrica |
| Definição | Participação da energia solar na geração elétrica |
| Unidade | % da geração |
| Período utilizado | 2000–2025 |
| Instituição | Ember – Yearly Electricity Data (arquivo 'Yearly electricity data – Global (CSV)', versão de 2026-09-08; atualizado mensalmente) |
| Link | https://ember-energy.org/data/yearly-electricity-data/ |
| Código da série | Electricity source = Solar; coluna 'Share of generation (%)' |
| Data de acesso | 2026-09-14 |
| Ajustes | Em julho de 2026 o Ember mudou o formato: o arquivo anual passou a ter uma linha por área, ano e fonte ('Electricity source'), com as métricas em colunas; as colunas Category/Subcategory/Variable/Unit/Value do formato longo antigo não existem mais. Filtro 'Electricity source' = Solar; valor lido de 'Share of generation (%)'. O agregado 'Latin America and Caribbean' não tem código ISO no arquivo e fica de fora (LCN ausente). Recorte ao período do catálogo; 2025 só existe para Colômbia, Costa Rica e República Dominicana (dado preliminar) |

## `renovaveis_geracao_share` — Participação das renováveis na geração elétrica

| Campo | Valor |
|---|---|
| Bloco | setor |
| Dimensão | Setor – participação das renováveis na geração elétrica |
| Definição | Participação das renováveis na geração elétrica |
| Unidade | % da geração |
| Período utilizado | 2000–2025 |
| Instituição | Ember – Yearly Electricity Data (arquivo 'Yearly electricity data – Global (CSV)', versão de 2026-09-08; atualizado mensalmente) |
| Link | https://ember-energy.org/data/yearly-electricity-data/ |
| Código da série | Electricity source = Renewables (agregado: hidro, eólica, solar, bioenergia e outras renováveis); coluna 'Share of generation (%)' |
| Data de acesso | 2026-09-14 |
| Ajustes | Mesmo arquivo da série anterior, outro filtro ('Electricity source' = Renewables, linha agregada). Recorte ao período do catálogo. Atenção: Costa Rica 2025 = 109,9% porque o Ember registra 'Other fossil' negativo (-1,15 TWh) nesse ano preliminar; valor mantido como na fonte e sinalizado em verificacao.txt |

## `tarifa_eletricidade` — Tarifa média de eletricidade da JPS, todas as classes (inclui as parcelas fuel e non-fuel); tarifa residencial (Rate 10) em coluna adicional, em J$/kWh

| Campo | Valor |
|---|---|
| Bloco | setor |
| Dimensão | Setor – característica relevante para investimento (custo da eletricidade) |
| Definição | Tarifa média de eletricidade da JPS, todas as classes (inclui as parcelas fuel e non-fuel); tarifa residencial (Rate 10) em coluna adicional, em J$/kWh |
| Unidade | US$ por kWh |
| Período utilizado | 2015–2025 |
| Instituição | MSETT (Ministry of Energy, Transport and Telecommunications da Jamaica) – Energy Division, 'Jamaica Energy Statistics', tabela 'JPS Rate Charges' (dados da JPS); 2015 do IRP 2018 (MSET). OUR usada como conferência |
| Link | https://www.mset.gov.jm/documents/jamaica-energy-statistics/ |
| Código da série | — |
| Data de acesso | ver coluna data_acesso do arquivo |
| Ajustes | Transcrito das edições 2019–2025 de Jamaica Energy Statistics (MSETT), com edição, página, link e data de acesso em cada linha. US$/kWh como publicado pela fonte (conversão feita pelo MSETT, arredondada a 2 casas); valor original em J$/kWh (edições até 2024 publicam em J¢/kWh, dividido por 100). 2025 é preliminar. 2015 vem do IRP 2018 (p. 14). Conversão própria em transform.py (tarifa_eletricidade_usd.csv): J$/kWh dividido pelo câmbio médio anual do WDI (PA.NUS.FCRF, série auxiliar cambio_jmd_usd), gerando a residencial em US$/kWh e a média do sistema recalculada para conferir o US$ publicado. Documentos da JPS (jpsco.com) inacessíveis em 2026-09-14 (bloqueio anti-bot); a Determinação 2019-2024 da OUR (p. 482) confirma a ordem de grandeza (J$34/kWh em 2018-19) |

## `armazenamento_projetos` — Projetos de armazenamento em baterias (BESS) na Jamaica: nome, capacidade (MW/MWh), ano, status (operacional, em contratação, em licitação, planejado)

| Campo | Valor |
|---|---|
| Bloco | setor |
| Dimensão | Setor – armazenamento (projetos e capacidade) |
| Definição | Projetos de armazenamento em baterias (BESS) na Jamaica: nome, capacidade (MW/MWh), ano, status (operacional, em contratação, em licitação, planejado) |
| Unidade | MW e MWh (valor = MWh) |
| Período utilizado | 2019–2026 |
| Instituição | OUR (Determinação JPS Annual Review 2023), MSET (IRP 2022), GPE (Generation Procurement Entity); JPS via imprensa especializada (pv magazine, Gleaner) e JIS como apoio |
| Link | https://our.org.jm/wp-content/uploads/2023/08/JPS-2023-Annual-Tariff-Review-Determination-Notice.pdf |
| Código da série | — |
| Data de acesso | ver coluna data_acesso do arquivo |
| Ajustes | Tabela compilada; valor = MWh, potência na coluna mw; ano = comissionamento (operacional), operação prevista (contratação/licitação) ou ano do documento (plano). Cada linha traz fonte, link e data de acesso. O documento original da JPS sobre o BESS de 171,5 MWh não pôde ser lido (jpsco.com bloqueia acesso automatizado) e foi substituído por imprensa especializada. Não há série estatística internacional para armazenamento por país |

## `populacao` — População total

| Campo | Valor |
|---|---|
| Bloco | auxiliar |
| Dimensão | Auxiliar – normalização |
| Definição | População total |
| Unidade | Pessoas |
| Período utilizado | 1960–2025 |
| Instituição | Banco Mundial – WDI |
| Link | https://data.worldbank.org/indicator/SP.POP.TOTL |
| Código da série | SP.POP.TOTL |
| Data de acesso | 2026-09-14 |
| Ajustes | Usada apenas como denominador |

## `cambio_jmd_usd` — Taxa de câmbio oficial, média do período (moeda local por US$); para a Jamaica, J$ por US$

| Campo | Valor |
|---|---|
| Bloco | auxiliar |
| Dimensão | Auxiliar – conversão de moeda |
| Definição | Taxa de câmbio oficial, média do período (moeda local por US$); para a Jamaica, J$ por US$ |
| Unidade | Moeda local por US$ |
| Período utilizado | 1960–2025 |
| Instituição | Banco Mundial – WDI (origem: FMI, International Financial Statistics) |
| Link | https://data.worldbank.org/indicator/PA.NUS.FCRF |
| Código da série | PA.NUS.FCRF |
| Data de acesso | 2026-09-14 |
| Ajustes | Usada apenas para converter a tarifa manual (J$/kWh) em US$/kWh em transform.py (tarifa_eletricidade_usd.csv). Baixada para todo o grupo, mas só a linha da Jamaica é usada |

