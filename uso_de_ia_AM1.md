# Registro de uso de IA — AM1 (Jamaica / energia solar e armazenamento)

**Ferramenta:** Claude (Anthropic), modelo Claude Fable 5.1 — chat do claude.ai e Claude Code.
**Data de início:** 2026-09-14

## Sessões

### Sessão 1 — 2026-09-14 (chat): replicação do pipeline para a Jamaica
- Prompt: enunciados da AM1 e do projeto final; pedido de pipeline de extração para Jamaica / solar e armazenamento.
- Resposta: repositório `jamaica_AM1/` com catálogo generalizado (país, comparadores e nomes no YAML), extratores worldbank/undp/csv_url/manual, run_all.py, transform.py e prompt para o Claude Code.

> Colar aqui os prompts e respostas completos da sessão de chat, em ordem cronológica. As interações do Claude Code estão transcritas no Anexo, ao final deste arquivo.

### Sessão 2 — 2026-09-14 (Claude Code): completar, executar e verificar o pipeline

**Prompt:** o arquivo `prompt_claude_code_AM1_jamaica.md` (sete tarefas: ambiente, catálogo, tabelas manuais, extração, verificação, figuras e derivados, relatório final; transcrito no Anexo A). O agente não redesenhou o pipeline: completou o catálogo consultando as fontes reais, preencheu as tabelas manuais com documentos públicos, rodou e verificou tudo.

#### O que rodou

1. **Ambiente.** Pasta já descompactada (idêntica ao `jamaica_AM1.zip`); venv com Python 3.14.3, pandas 3.0.5, requests 2.34.2, PyYAML 6.0.3, matplotlib 3.11.2 (só `requirements.txt`; nenhum pacote extra no projeto).
2. **Consulta às fontes (não de memória).** Metadados dos indicadores na API do Banco Mundial (`/v2/indicator/<codigo>?format=json&source=...`): todos os códigos confirmados, inclusive `HD.HCI.OVRL` na fonte 63 e `GOV_WGI_RL.EST` na fonte 3 (o antigo `RL.EST` não existe mais nessa fonte). Página de downloads do HDR: o arquivo continua `HDR25_Composite_indices_complete_time_series.csv` (2 MB, maio de 2025). Página e arquivos do Ember: o formato mudou em julho de 2026 (ver alterações). Metadados do grapher do OWID e API PxWeb do IRENASTAT (tabela `Country_ELECCAP_2026_H1`): usados para conferir a série de capacidade solar. API SDMX 2.1 do FMI (`api.imf.org`): testada para a alternativa de dívida.
3. **Extração** (`run_all.py`): 13 de 13 séries com status `ok` em `log_extracao.csv`; brutos datados em `dados/brutos/` (12 arquivos, ~35 MB, dos quais 2 × 16 MB do Ember).
4. **Verificação** (`verificar.py`, saída em `dados/processados/verificacao.txt`): sem duplicatas país-ano, sem NaN, valores nas faixas esperadas; três valores sorteados (seed 20260914) conferidos contra os brutos: `wgi_rule_of_law` TTO 2013, `renovaveis_geracao_share` DOM 2013, `solar_capacidade` TTO 2023 — todos idênticos.
5. **Figuras e derivados** (`transform.py`): sete PNGs em `figuras/`, derivados e tabelas em `dados/processados/`. Cada PNG foi aberto e conferido.
6. **Tabelas em Markdown** (`gerar_tabelas.py`, adaptado do projeto Japão): `01_painel_ultimo_ano_comum.md`, `02_series_por_pais_anos_selecionados.md`, `03_jam_marcos_temporais.md`, `04_derivados.md`, `05_fatos_chave.md`, `06_tabelas_manuais.md` e `fontes.md`, todos em `dados/processados/`.
7. **Git**: `git init` e commit inicial `822dd96` (sem `.venv/` nem `__pycache__/`).

#### O que alterou (arquivo, motivo)

| Arquivo | Alteração | Motivo |
|---|---|---|
| `config/series.yaml` — `solar_capacidade` | `url_csv` = grapher do OWID (`installed-solar-pv-capacity.csv`), `mapeamento {Code, Year, Solar}`, `fator: 1000`, `instituicao` registra que é republicação da IRENA, `ajuste` documenta a conferência | A IRENA não oferece URL de download direto em CSV: o IRENASTAT (PxWeb) só devolve CSV por POST e o irena.org bloqueia acesso automatizado (HTTP 403). O OWID publica em GW; conferido na API do IRENASTAT que os valores coincidem com a soma PV on-grid + off-grid (diferença ≤ 0,01 MW; única exceção Costa Rica 2012, 0,9 MW) e que a CSP é nula nos sete países, logo "solar total" = fotovoltaica |
| `config/series.yaml` — `solar_geracao_share`, `renovaveis_geracao_share` | `url_csv` = `release_generation_yearly_global.csv`; `mapeamento` e `filtros` refeitos (`Electricity source` = Solar / Renewables; valor em `Share of generation (%)`) | O Ember trocou o formato em julho de 2026: uma linha por área, ano e fonte, métricas em colunas; as colunas Category/Subcategory/Variable/Unit/Value não existem mais. O arquivo "Europe only" (`_lower`) não tem os países do grupo |
| `config/series.yaml` — `hci`, `energia_importada`, `divida_publica`, `wgi_rule_of_law` | Campo `ajuste` passou a registrar a cobertura efetiva e as lacunas conferidas | Exigência de documentar lacunas; a dívida no WDI é insuficiente para comparação |
| `config/series.yaml` — bloco comentado `divida_bruta_weo` | Entrada pronta (não ativada) para `GGXWDG_NGDP` do FMI WEO via API SDMX 2.1, usando o extrator `csv_url` | Alternativa pedida no prompt; não implementada sem autorização |
| `config/series.yaml` — `tarifa_eletricidade`, `armazenamento_projetos` | `instituicao`, `link`, `definicao` e `ajuste` descrevem o que as tabelas manuais contêm (fontes, unidades, `valor` = MWh) | Coerência entre `fontes.csv` e o conteúdo real das tabelas |
| `processamento/extract/csv_url.py` | Campo opcional `fator` (multiplica o valor) e aplicação de `periodo.inicio/fim` do catálogo | Converter GW→MW de forma declarada; o recorte de período passou a valer para todas as fontes |
| `processamento/run_all.py` | Passa `ini, fim` para `csv_url.fetch` | Idem |
| `processamento/transform.py` | Legenda das figuras de linha à direita do gráfico (`legenda_fora`), `bbox_inches="tight"` ao salvar, rótulo do eixo y da convergência em duas linhas | Só renderização: a legenda cobria linhas em `fig_energia_importada`, `fig_wgi_rule_of_law` e `fig_idh`; o rótulo longo cortava no topo |
| `processamento/verificar.py` (novo) | Resumo por série, sinalizações e conferência aleatória contra os brutos | Tarefa 5 do prompt; gera `dados/processados/verificacao.txt` |
| `processamento/gerar_tabelas.py` (novo) | Adaptação do script do projeto Japão: país, comparadores, nomes e referência lidos do catálogo; fallback quando nenhum ano é comum a todos os países (dívida) | Tarefa 6 do prompt |
| `dados/manuais/tarifa_eletricidade.csv` | 11 linhas (2015–2025), tarifa média da JPS em US$/kWh como publicada pelo MSETT (Jamaica Energy Statistics, tabela "JPS Rate Charges", dados da JPS), valor original em J$/kWh, coluna extra com a tarifa residencial (Rate 10); 2015 do IRP 2018 | Documentos da JPS (jpsco.com) inacessíveis por bloqueio anti-bot (Incapsula); o MSETT publica a série oficial com fonte JPS |
| `dados/manuais/armazenamento_projetos.csv` | 4 linhas: HESS de Hunts Bay (OUR, 24,5 MW / 16,6 MWh, dez. 2019), BESS da 1ª fase do IRP 2022 (264 MW / 528 MWh, plano), BESS de 171,5 MWh da JPS (licitação EPC 2023, imprensa especializada), 2ª rodada da GPE (110 MW / 220 MWh, RFI mar. 2026) | Tarefa 3; cada linha com fonte, link e data de acesso |
| `README.md` | Seção "Antes da primeira execução" substituída por "Estado do catálogo"; novos scripts na estrutura e no "Como rodar" | Instruções anteriores ficaram obsoletas |
| `uso_de_ia_AM1.md` | Esta seção | Exigência da atividade |

Nada em `dados/brutos/` foi editado; nenhum valor foi imputado, interpolado ou inventado.

#### Lacunas e cautelas registradas

- Agregado LCN só existe no Banco Mundial (WDI; não no WGI); ausente no HDR, HCI, OWID e Ember. Barbados não tem `energia_importada` nem `hci`. WGI sem 1997, 1999 e 2001. `energia_importada` da Jamaica sem 2005–2007.
- `divida_publica` (WDI): Jamaica 1990–2020 sem 2018; comparadores muito irregulares (Panamá sem dado; Trinidad e Tobago só 2006–2007; República Dominicana 1996–1999). A alternativa do FMI WEO (`GGXWDG_NGDP`) foi testada: sete países com dados anuais (Jamaica 1999–2024 observados, ano fiscal), projeções até 2031 a excluir; bloco pronto no catálogo, não ativado.
- `solar_capacidade` vem da republicação do OWID, não da IRENA diretamente (motivo e conferência no catálogo).
- `tarifa_eletricidade`: US$ arredondado a 2 casas pela própria fonte. HESS com composição divergente entre fontes (OUR na inauguração: 21 MW baterias + 3,5 MW flywheel; IRP 2022: 20 MW + 4,5 MW).

O relatório final entregue no chat ao fim desta sessão está transcrito no Anexo B; a tabela de períodos e últimos valores foi atualizada na Sessão 3, depois da mudança do período para 2025.

### Sessão 3 — 2026-09-14 (Claude Code): decisões do aluno aplicadas

**Prompt (transcrito no Anexo C):** usar `energia_importada` como quinta dimensão; adotar a OUR para a composição do HESS; converter a tarifa com `PA.NUS.FCRF`; `periodo.fim` = 2025; montar um docx com as interações de IA; organizar as pastas e subpastas no padrão do projeto anterior, sem commit nem push.

#### O que alterou (arquivo, motivo)

| Arquivo | Alteração | Motivo |
|---|---|---|
| `config/series.yaml` | `periodo.fim: 2025`; comentário registrando `energia_importada` como quinta dimensão do PDF (a dívida e o WGI seguem no catálogo como apoio); nova série auxiliar `cambio_jmd_usd` (WDI `PA.NUS.FCRF`, moeda local por US$, média do período); `ajuste` da tarifa descreve a conversão; nota sobre Costa Rica 2025 em `renovaveis_geracao_share` | Decisões do aluno; a conversão de moeda passa a ser feita no código, com a série de câmbio no catálogo e em `fontes.csv` |
| `dados/manuais/armazenamento_projetos.csv` | Colunas novas `mw_baterias` = 21 e `mw_flywheel` = 3,5 na linha do HESS; `observacao` registra que a composição adotada é a da OUR (discurso do Diretor-Geral na inauguração, 2019-12-11) e que a do IRP 2022 (20 + 4,5 MW) é divergente e não foi usada | Decisão do aluno |
| `processamento/transform.py` | Função `tarifa_em_dolar()` gera `tarifa_eletricidade_usd.csv`: J$/kWh ÷ câmbio médio anual, com a residencial em US$ e a média do sistema recalculada para conferir o US$ publicado pelo MSETT | Decisão do aluno; sem alterar a tabela manual |
| `processamento/gerar_tabelas.py` | Tabela da tarifa em US$ em `04_derivados.md` e fato-chave em `05_fatos_chave.md` | Idem |
| `README.md` | Itens 4, 6, 7 e 8 do "Estado do catálogo" com as decisões | Documentação |
| `.gitattributes` (novo) | `* text=auto`, PNG/docx/PDF binários | Evitar avisos LF/CRLF entre sistemas ao montar o repositório |
| `uso_de_ia_AM1.md` e `uso_de_ia_AM1.docx` | Esta seção, o Anexo com as interações e a versão docx gerada a partir do Markdown (python-docx, fora do projeto) | Pedido do aluno |
| `../jamaica_AM1_insumos_relatorio/` (fora do repositório) | Cópia organizada dos insumos para o relatório, no mesmo padrão da pasta `japao_AM1_insumos_relatorio/`: guias, catálogo e fontes, dados processados, figuras, tabelas, verificação e código | Pedido do aluno ("conforme sempre fizemos"); nada foi commitado nem enviado |

#### O que rodou

`run_all.py` (14 de 14 séries `ok`, incluindo `cambio_jmd_usd`), `verificar.py`, `transform.py` e `gerar_tabelas.py`. Conferência aleatória contra os brutos (seed 20260914): `wgi_rule_of_law` JAM 2014, `armazenamento_projetos` JAM 2026 e `renovaveis_geracao_share` PAN 2018 — todos idênticos.

#### Séries: período usado e último valor da Jamaica (período do catálogo até 2025)

| id | Período usado | Último valor da Jamaica |
|---|---|---|
| `idh` | 1990–2023 | 0,720 (2023), 7º de 7 |
| `pib_pc_ppp` | 1990–2025 | US$ 11.358 (2025), 8º de 8; 46,3% da República Dominicana |
| `pib_por_ocupado` | 1991–2025 | US$ 20.659 (2025), 8º de 8 |
| `hci` | 2010–2020 (2010, 2017, 2018, 2020) | 0,535 (2020), 4º de 6 |
| `energia_importada` (quinta dimensão) | 1990–2023 (Jamaica até 2022) | 112,6% do uso de energia (2022) |
| `divida_publica` (apoio) | 1990–2024 (Jamaica até 2020) | 97,9% do PIB (2020) |
| `wgi_rule_of_law` (apoio) | 1996–2024 | −0,08 (2024), 3º de 7 |
| `solar_capacidade` | 2000–2025 | 116,6 MW (2025), 4º de 7; 41,1 kW por 1.000 hab. (5º de 7) |
| `solar_geracao_share` | 2000–2025 (Jamaica até 2024) | 3,05% da geração (2024) |
| `renovaveis_geracao_share` | 2000–2025 (Jamaica até 2024) | 12,6% da geração (2024) |
| `tarifa_eletricidade` (manual) | 2015–2025 | US$ 0,32/kWh publicado (2025, preliminar); residencial calculada US$ 0,367/kWh (2025); máximo em 2022 (US$ 0,36 publicado; residencial US$ 0,410) |
| `armazenamento_projetos` (manual) | 2019–2026 | 4 registros; único operacional: HESS 24,5 MW (21 MW baterias + 3,5 MW flywheel) / 16,6 MWh |
| `populacao` (auxiliar) | 1960–2025 | 2,84 milhões (2025) |
| `cambio_jmd_usd` (auxiliar) | 1960–2025 | 159,10 J$ por US$ (2025) |

#### Novas sinalizações

- Costa Rica 2025: renováveis = 109,9% da geração porque o Ember registra "Other fossil" negativo (−1,15 TWh) nesse ano preliminar; valor mantido como na fonte, anotado no catálogo e em `verificacao.txt`.
- 2025 do Ember só existe para Colômbia, Costa Rica e República Dominicana; a Jamaica termina em 2024 nas participações e em 2025 na capacidade (igual a 2024).

#### Pendências restantes

1. Confirmar no site da JPS os MW do BESS de 171,5 MWh e confirmar na GPE se a 2ª rodada passou de 220 MW + 110 MW/220 MWh para 300 MW + 150 MW (anúncio de maio de 2026).
2. Colar neste arquivo a transcrição da Sessão 1 (chat do claude.ai), que o Claude Code não tem.
3. Conversão deste arquivo em PDF na entrega; renomear a pasta para `sobrenome_jamaica_AM1` e compactar sem `.venv/`. O commit das alterações e a inicialização do git passaram a ser feitos manualmente pelo aluno (ver Sessão 4).

### Sessão 4 — 2026-09-14 (Claude Code): diagnóstico do erro de git e reinício da inicialização

**Prompt:** entender o erro do repositório git associado ao projeto e desfazer toda a inicialização feita pelo agente, para o aluno refazê-la manualmente sem misturar nada.

**Diagnóstico (só leitura):** o repositório local tinha dois commits (`822dd96`, do agente, e `aef4626`, "commit inicial", do aluno) e o remoto `origin` (github.com/Dusenedezi/trabalho_jamaica) tinha um "Initial commit" (`9e39ab0`) criado pelo próprio GitHub, só com o arquivo LICENSE. As duas histórias não têm ancestral comum, o que faz o `git push` ser rejeitado e o `git pull` recusar ("refusing to merge unrelated histories"). Nenhuma pasta acima do projeto é repositório; `.venv/` e `__pycache__/` estavam corretamente ignorados; `git fsck` sem erros; 73 arquivos rastreados e árvore de trabalho limpa. Configuração do sistema: `core.autocrlf=true` e `init.defaultbranch=master` (por isso o primeiro `git init` do agente usou `-b main`). Detalhe de fim de linha: `dados/brutos/idh_20260914.csv` é detectado como binário pelo git, mas a regra `*.csv text` o forçaria a conversão; foi acrescentada a regra `dados/brutos/** -text` ao `.gitattributes`, para que os brutos sejam guardados byte a byte.

**O que fez:** backup completo do `.git` em `../jamaica_AM1_git_backup_20260914.zip` (267 entradas, 5 MB) e remoção da pasta `.git` local. Os arquivos do projeto ficaram intactos (a árvore de trabalho era igual ao último commit). O remoto no GitHub não foi tocado. `uso_de_ia_AM1.docx` regerado a partir deste arquivo.

## Verificação dos resultados
- [ ] Cada série conferida no portal da fonte
- [ ] Códigos e URLs confirmados
- [ ] Tabelas manuais: cada linha com fonte, link e data de acesso, valores conferidos no documento original
- [ ] Derivados recomputados manualmente para um ano

## Anexo — transcrição das interações com o Claude Code

### Anexo A — Prompt inicial da Sessão 2 (arquivo `prompt_claude_code_AM1_jamaica.md`)

Mensagem do aluno no Claude Code: "Leia, e execute o que está sendo pedido neste arquivo. Em caso de dúvida, me questione sobre como prosseguir."

```
# Contexto

Estou fazendo a Atividade Monitorada 1 da disciplina Economias Emergentes e Desenvolvimento Econômico (FGV EAESP): diagnóstico inicial da **Jamaica** e do setor de **energia solar e armazenamento**, etapa inicial de um memo de investimento. Já tenho um repositório em `jamaica_AM1.zip` (mesma pasta deste prompt), replicado de um projeto anterior que funcionou. Seu trabalho é completar, executar e verificar o pipeline — não redesenhá-lo.

Regras da atividade:
- Toda série precisa de definição, unidade, período usado, instituição, link direto, código, data de acesso e ajustes. Isso está modelado em `config/series.yaml` e vira `dados/processados/fontes.csv`.
- **Nunca edite `dados/brutos/`.** Nunca invente dados. Quando um dado não existir, registre a lacuna.
- Serei sabatinado oralmente sobre fontes, processamento e leitura; prefira soluções simples e explicáveis.
- Ao final, acrescente em `uso_de_ia_AM1.md` uma seção "Sessão Claude Code" com o que fez, alterou e por quê.

# Tarefas, em ordem

1. **Ambiente.** Descompacte, leia `README.md` e `config/series.yaml` inteiros, crie venv e instale `requirements.txt`.

2. **Completar o catálogo consultando as fontes reais (não de memória):**
   - `solar_capacidade` (IRENA): encontre a URL de download direto, em CSV, da capacidade instalada por país e tecnologia (IRENASTAT ou o arquivo de extração da IRENA). Preencha `url_csv`, `mapeamento` e `filtros` (tecnologia = solar fotovoltaica; observe se há colunas de tipo on-grid/off-grid). Se só houver nomes de país, use `tipo_pais: nome` e `nomes_fonte`. Se a IRENA não oferecer CSV direto, use o grapher do Our World in Data (`installed-solar-pv-capacity.csv`), que republica IRENA, e registre no campo `instituicao` que é republicação.
   - `solar_geracao_share` e `renovaveis_geracao_share` (Ember): localize a URL atual do arquivo anual em formato longo, confira o cabeçalho e ajuste `mapeamento` e `filtros` se os nomes mudaram.
   - Confirme os códigos WDI/WGI em `https://api.worldbank.org/v2/indicator/<codigo>?format=json` (WGI: `source=3`; HCI: `source=63`). Confirme o nome atual do arquivo do HDR.
   - Verifique a cobertura de `energia_importada` e `divida_publica` para a Jamaica; se a dívida no WDI for insuficiente, proponha a série `GGXWDG_NGDP` do FMI WEO como alternativa e diga como acessá-la (não implemente sem me avisar).

3. **Tabelas manuais.** Não invente valores. Para `dados/manuais/tarifa_eletricidade.csv` e `armazenamento_projetos.csv`, busque os documentos públicos da OUR (regulador), da JPS (concessionária) e do plano integrado de recursos do governo jamaicano; preencha apenas o que conseguir ler e citar com link direto e data. O que não encontrar, deixe fora e liste no relatório final para eu completar.

4. **Extração.** Rode `python processamento/run_all.py` até `log_extracao.csv` ficar sem erros nas séries que têm fonte preenchida. Séries que dependem de mim podem ficar com erro, desde que listadas.

5. **Verificação.** Para cada série: observações, primeiro e último ano, número de países, valor da Jamaica no último ano. Sinalize lacunas, valores fora de escala e comparadores ausentes. Confira três valores sorteados contra os brutos.

6. **Figuras e derivados.** Rode `python processamento/transform.py`, abra cada PNG e corrija só renderização. Adapte o `gerar_tabelas.py` do projeto anterior (se eu o incluir na pasta) para ler país, comparadores e nomes de `config/series.yaml` em vez de constantes, e gere as tabelas em Markdown.

7. **Relatório final:** o que rodou; o que alterou (arquivo, motivo); tabela id / período / último valor da Jamaica; pendências minhas, em especial linhas das tabelas manuais e a decisão sobre a quinta dimensão.

# Restrições

- Sem pacotes além de `requirements.txt` salvo necessidade real e justificada.
- Não altere a estrutura de pastas nem os nomes dos arquivos de saída.
- Não faça commit de `.venv/` nem de `__pycache__/`. Ao final, `git init` com um commit inicial.
```

### Anexo B — Resposta final do Claude Code na Sessão 2 (transcrição integral)

Pipeline completo: 13 de 13 séries extraídas sem erro, verificadas contra os brutos, 7 figuras e 7 tabelas em Markdown geradas, `git init` com commit inicial `822dd96` (68 arquivos, sem `.venv/` nem `__pycache__/`). A seção "Sessão Claude Code" está em [uso_de_ia_AM1.md](uso_de_ia_AM1.md), com a tabela de alterações completa.

#### O que mudou e por quê

- **[config/series.yaml](config/series.yaml)**: `solar_capacidade` usa o grapher do OWID, que republica a IRENA, porque a IRENA não oferece CSV por GET. O IRENASTAT só responde por POST e o irena.org devolve 403 a scripts. Conferi na API do IRENASTAT que os valores do OWID batem com PV on-grid + off-grid em todos os anos e que a CSP é nula nos sete países. O arquivo vem em GW e é convertido para MW pelo campo novo `fator: 1000`.
- **Ember**: o formato mudou em julho de 2026. A URL atual é `release_generation_yearly_global.csv`, uma linha por área, ano e fonte, métricas em colunas. Mapeamento e filtros foram refeitos. O arquivo "lower" é só Europa.
- **Banco Mundial e HDR**: todos os códigos confirmados na API, WGI é `GOV_WGI_RL.EST` na fonte 3, HCI na fonte 63. O arquivo do HDR continua `HDR25_Composite_indices_complete_time_series.csv`.
- **[csv_url.py](processamento/extract/csv_url.py) e [run_all.py](processamento/run_all.py)**: campo opcional `fator` e recorte pelo `periodo` do catálogo, que antes só valia para o Banco Mundial.
- **[transform.py](processamento/transform.py)**: só renderização. Legenda à direita do gráfico porque cobria linhas em três figuras, recorte `bbox_inches="tight"`, rótulo da convergência em duas linhas.
- **Novos**: [verificar.py](processamento/verificar.py) gera [verificacao.txt](dados/processados/verificacao.txt). [gerar_tabelas.py](processamento/gerar_tabelas.py) foi adaptado do projeto Japão e lê país, comparadores e nomes do catálogo, com saída em `dados/processados/01_*.md` a `06_*.md` e `fontes.md`.
- **Tabelas manuais**: [tarifa_eletricidade.csv](dados/manuais/tarifa_eletricidade.csv) tem 11 linhas, 2015 a 2025, tarifa média da JPS em US$/kWh como publicada nas "Jamaica Energy Statistics" do MSETT, com valor original em J$/kWh e coluna extra da tarifa residencial. [armazenamento_projetos.csv](dados/manuais/armazenamento_projetos.csv) tem 4 linhas com fonte, link e data em cada uma. O site da JPS bloqueia acesso automatizado, por isso a OUR, o IRP 2022, a GPE e o MSETT foram as fontes primárias.
- **README** atualizado com o estado do catálogo e os scripts novos.

#### Séries, período e último valor da Jamaica

| id | Período | Último valor da Jamaica |
|---|---|---|
| idh | 1990–2023 | 0,720 em 2023, 7º de 7 |
| pib_pc_ppp | 1990–2024 | US$ 11.340 em 2024, 46,8% da Rep. Dominicana |
| pib_por_ocupado | 1991–2024 | US$ 20.741 em 2024, 8º de 8 |
| hci | 2010–2020 | 0,535 em 2020, 4º de 6 |
| energia_importada | 1990–2023 | 112,6% do uso em 2022 |
| divida_publica | 1990–2024 | 97,9% do PIB em 2020 |
| wgi_rule_of_law | 1996–2024 | −0,08 em 2024, 3º de 7 |
| solar_capacidade | 2000–2024 | 116,6 MW em 2024, 4º de 7 |
| solar_geracao_share | 2000–2024 | 3,05% em 2024 |
| renovaveis_geracao_share | 2000–2024 | 12,6% em 2024 |
| tarifa_eletricidade | 2015–2025 | US$ 0,32/kWh em 2025, preliminar |
| armazenamento_projetos | 2019–2026 | HESS 24,5 MW / 16,6 MWh operacional |
| populacao | 1960–2024 | 2,84 milhões em 2024 |

Verificação: sem duplicatas nem NaN, três valores sorteados idênticos aos brutos. Lacunas registradas no catálogo e em `verificacao.txt`: LCN só existe no Banco Mundial, Barbados sem energia importada nem HCI, WGI sem 1997, 1999 e 2001, dívida no WDI muito irregular entre comparadores.

#### Pendências suas

1. **Quinta dimensão.** Recomendo `energia_importada`: é a ponte direta com a tese solar e cobre a Jamaica até 2022 com todos os comparadores exceto Barbados. `wgi_rule_of_law` é a série mais completa. A dívida no WDI é insuficiente para comparar. A alternativa `GGXWDG_NGDP` do FMI WEO funciona por GET na API SDMX 2.1, sem extrator novo, e está como bloco comentado no catálogo. Não ativei sem sua autorização.
2. **Armazenamento.** Confirmar no site da JPS os MW do BESS de 171,5 MWh e o cronograma. Confirmar na GPE se a segunda rodada passou de 220 MW mais 110 MW/220 MWh para 300 MW mais 150 MW, como o ministro anunciou em maio de 2026. Escolher qual composição do HESS citar, já que a OUR diz 21 MW mais 3,5 MW e o IRP diz 20 MW mais 4,5 MW.
3. **Tarifa.** A residencial está em J$/kWh. Converter para US$ exige adicionar `PA.NUS.FCRF` ao catálogo. O valor de 2015 vem do IRP 2018, não do MSETT.
4. **Período.** OWID e Ember já têm 2025 para parte do grupo. Decidir se `periodo.fim` sobe para 2025.
5. **Entrega.** Colar os prompts e respostas completos em `uso_de_ia_AM1.md`, converter em PDF, renomear a pasta para `sobrenome_jamaica_AM1` e compactar sem `.venv/`.

### Anexo C — Mensagem do aluno na Sessão 3 (transcrição integral)

> Vamos usar energia_importada como quinta dimensão. Sobre o marmazenamento, vamos usar a OUR. Sobrte tarifa, vamos usar PA.NUS.FCRF. Vamos usar periodo.fim de 2025. Consegue montar um docx com as interações de IA?
> Também, vamos organizar todas as pastas e sub pastas para montar um repositório do git. Preciso de sua ajuda para isso, mas faça conforme sempre fizemos. Organize, mas não dê commit e nem push.

### Anexo D — Resposta final do Claude Code na Sessão 3

O conteúdo da resposta final é o mesmo da seção "Sessão 3" acima (alterações, execução, tabela atualizada, sinalizações e pendências), acrescido do mapa da pasta `jamaica_AM1_insumos_relatorio/` descrito em seu `00_LEIA-ME.md`.
