# Fatos-chave (calculados a partir dos CSVs)

> Gerado por `processamento/gerar_tabelas.py` em 2026-09-14 a partir de `dados/processados/` (acesso às fontes em 2026-09-14). Números em formato pt-BR. Traço (—) = sem dado. Comparadores ausentes em uma fonte simplesmente não aparecem.


Cada frase pode ser conferida no CSV citado. Interpretação e contexto ficam para o relatório.

## País

- **Convergência (`pib_pc_ppp_pct_dom.csv`)**: o PIB per capita PPP de Jamaica era 121,2% do de República Dominicana em 1990, atingiu o máximo de 127,3% em 1991 e chegou a 46,3% em 2025. Demais países em 2025 (República Dominicana = 100): Trinidad e Tobago 129,2%; Barbados 90,2%; Costa Rica 115,9%; Panamá 152,9%; Colômbia 76,5%; América Latina e Caribe 82,7%.
- **Nível (`pib_pc_ppp.csv`)**: Jamaica US$ 8.880 (1990) → US$ 11.358 (2025), variação de 27,9% no período; República Dominicana 234,9%. Em 2025, Jamaica é 8º de 8 países.
- **Produtividade (2025, `pib_por_ocupado.csv`)**: Panamá 81.808; Trinidad e Tobago 68.867; Costa Rica 64.823; República Dominicana 54.043; Barbados 44.125; América Latina e Caribe 43.303; Colômbia 40.369; Jamaica 20.659 US$ PPP por pessoa ocupada. Jamaica em 8º de 8, com 25,3% do nível de Panamá e 38,2% do de República Dominicana.
- **IDH (`idh.csv`)**: Jamaica 0,662 (1990) → 0,720 (2023), 7º de 7 em 2023. Maior: Panamá 0,839; menor: Jamaica 0,720.
- **Capital humano (HCI 2020, `hci.csv`)**: Costa Rica 0,629; Colômbia 0,604; Trinidad e Tobago 0,603; Jamaica 0,535; República Dominicana 0,503; Panamá 0,502. Jamaica em 4º de 6. Anos disponíveis: 2010, 2017, 2018, 2020.
- **Importações líquidas de energia (2022, `energia_importada.csv`)**: Jamaica 112,6% do uso de energia (em 1990: 96,0%). Demais em 2022: República Dominicana 94,4%; Trinidad e Tobago -75,5%; Costa Rica 53,1%; Panamá 171,2%; Colômbia -139,1%; América Latina e Caribe -2,8%. Valores negativos = exportadores líquidos; acima de 100% ocorre quando há reexportação ou variação de estoques (definição do WDI).
- **Dívida do governo central (`divida_publica.csv`)**: Jamaica 97,9% do PIB em 2020 (máximo da série: 232,8% em 1991; em 1990: 138,7%). Comparadores com cobertura irregular no WDI (ver `verificacao.txt`).
- **Rule of Law (2024, `wgi_rule_of_law.csv`)**: Jamaica -0,08 (3º de 7; em 1996: -0,17). Maior: Barbados 0,73; menor: Colômbia -0,56.
- **População (`populacao.csv`)**: 2,84 milhões em 2025; máximo de 2,84 milhões em 2023 (-0,1% desde o máximo).

## Setor: energia solar e armazenamento

- **Capacidade solar instalada (`solar_capacidade.csv`)**: Jamaica 116,6 MW em 2025 (4º de 7); 6,5 MW em 2015; primeiro registro positivo em 2001. Em 2025: República Dominicana 2.083,1; Colômbia 1.726,2; Panamá 973,4; Jamaica 116,6; Trinidad e Tobago 96,6; Costa Rica 82,6; Barbados 69,3 MW.
- **Capacidade solar por habitante (2025, `solar_capacidade_kw_por_mil_hab.csv`)**: Barbados 245,36; Panamá 212,93; República Dominicana 180,81; Trinidad e Tobago 70,64; Jamaica 41,09; Colômbia 32,31; Costa Rica 16,04 kW por 1.000 hab. Jamaica em 5º de 7.
- **Solar na geração elétrica (`solar_geracao_share.csv`)**: Jamaica 3,05% em 2024 (máximo 3,05% em 2024; passa de 1% em 2018). Em 2024: Barbados 9,01%; Panamá 7,37%; República Dominicana 6,45%; Colômbia 3,85%; Jamaica 3,05%; Costa Rica 0,82%; Trinidad e Tobago 0,10%.
- **Renováveis na geração elétrica (`renovaveis_geracao_share.csv`)**: Jamaica 12,6% em 2024 (máximo 14,6% em 2018; em 2000: 4,6%). Em 2024: Costa Rica 99,9%; Panamá 68,0%; Colômbia 61,3%; República Dominicana 18,9%; Jamaica 12,6%; Barbados 9,0%; Trinidad e Tobago 0,1%.
- **Tarifa média de eletricidade (`tarifa_eletricidade.csv`, tabela manual)**: US$ 0,27/kWh em 2015 → US$ 0,32/kWh em 2025; máximo US$ 0,36/kWh em 2022. Segmento: média do sistema (todas as classes). Fonte de cada linha na própria tabela.
- **Tarifa residencial em US$ (`tarifa_eletricidade_usd.csv`, câmbio PA.NUS.FCRF)**: US$ 0,367/kWh em 2025 (máximo US$ 0,410 em 2022; em 2015: US$ 0,275). Média do sistema recalculada em 2025: US$ 0,325, contra US$ 0,32 publicado pelo MSETT.
- **Armazenamento em baterias (`armazenamento_projetos.csv`, tabela manual)**: 4 registros: Hunts Bay Hybrid Energy Storage System (HESS) — 24,5 MW / 16,6 MWh, operacional (comissionado em 2019-12) (2019); IRP 2022 – BESS do plano preferido, 1ª fase (2024–2027) — 264,0 MW / 528,0 MWh, planejado (plano integrado de recursos, não contratado) (2022); JPS – BESS em três ou mais locais (licitação EPC junto com 115 MW solar e 12 MW eólica) — — MW / 171,5 MWh, em contratação (EPC licitado em 2023-12; operação prevista do 4T2026 ao 3T2027) (2026); GPE – 2ª rodada de leilão: 220 MW renováveis + 110 MW / 220 MWh de BESS (co-localizado) — 110,0 MW / 220,0 MWh, em licitação (RFI lançado em 2026-03-19; leilão previsto para o 3T2026) (2026).
