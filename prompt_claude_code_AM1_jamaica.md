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
