# Tabelas manuais (tarifa e armazenamento)

> Gerado por `processamento/gerar_tabelas.py` em 2026-09-14 a partir de `dados/processados/` (acesso às fontes em 2026-09-14). Números em formato pt-BR. Traço (—) = sem dado. Comparadores ausentes em uma fonte simplesmente não aparecem.

## Tarifa média de eletricidade (`tarifa_eletricidade.csv`)

| Ano | US$/kWh | Valor original | Residencial (J$/kWh) | Fonte | Link | Acesso |
|---|---|---|---|---|---|---|
| 2015 | 0,27 | 0,27 USD/kWh | 32,22 | MSET – 2018 Jamaica Integrated Resource Plan (aprovado em fev. 2020), p. 14 | https://www.mset.gov.jm/wp-content/uploads/2020/03/2018-Jamaica-Integrated-Resource-Feb-21-2020.pdf | 2026-09-14 |
| 2016 | 0,22 | 26,94 JMD/kWh | 30,44 | MSETT – Jamaica Energy Statistics 2020, tabela 'Average Rate Charge (JA¢/kWh)' (fonte: JPS e IPPs), p. 16 | https://www.mset.gov.jm/wp-content/uploads/2020/06/JAMAICA-ENERGY-STATISTICS-2020.pdf | 2026-09-14 |
| 2017 | 0,25 | 32,65 JMD/kWh | 36,77 | MSETT – Jamaica Energy Statistics 2020, tabela 'Average Rate Charge (JA¢/kWh)' (fonte: JPS e IPPs), p. 16 | https://www.mset.gov.jm/wp-content/uploads/2020/06/JAMAICA-ENERGY-STATISTICS-2020.pdf | 2026-09-14 |
| 2018 | 0,28 | 35,76 JMD/kWh | 40,00 | MSETT – Jamaica Energy Statistics 2020, tabela 'Average Rate Charge (JA¢/kWh)' (fonte: JPS e IPPs), p. 16 | https://www.mset.gov.jm/wp-content/uploads/2020/06/JAMAICA-ENERGY-STATISTICS-2020.pdf | 2026-09-14 |
| 2019 | 0,27 | 35,69 JMD/kWh | 40,06 | MSETT – Jamaica Energy Statistics 2023 (rev. ago. 2024), tabela 'Trends in JPS Rate Charges (Jamaican Cents/kWh)' (fonte: JPS), p. 18 | https://www.mset.gov.jm/wp-content/uploads/2021/07/JAMAICA-ENERGY-STATISTICS-2023-Revised-August-2024.pdf | 2026-09-14 |
| 2020 | 0,28 | 39,93 JMD/kWh | 44,04 | MSETT – Jamaica Energy Statistics 2024 (jul. 2025), tabela 'Trends in JPS Rate Charges (Jamaican Cents/kWh)' (fonte: JPS), p. 18 | https://www.mset.gov.jm/wp-content/uploads/2021/07/JAMAICA-ENERGY-STATISTICS-2024.pdf | 2026-09-14 |
| 2021 | 0,31 | 46,57 JMD/kWh | 52,04 | MSETT – Jamaica Energy Statistics 2025 (jul. 2026), tabela 'JPS Rate Charges (Jamaican Dollars/kWh)' (fonte: JPS), p. 18 | https://www.mset.gov.jm/wp-content/uploads/2021/07/JAMAICA-ENERGY-STATISTICS-2025.pdf | 2026-09-14 |
| 2022 | 0,36 | 55,79 JMD/kWh | 62,92 | MSETT – Jamaica Energy Statistics 2025 (jul. 2026), tabela 'JPS Rate Charges (Jamaican Dollars/kWh)' (fonte: JPS), p. 18 | https://www.mset.gov.jm/wp-content/uploads/2021/07/JAMAICA-ENERGY-STATISTICS-2025.pdf | 2026-09-14 |
| 2023 | 0,31 | 47,73 JMD/kWh | 55,14 | MSETT – Jamaica Energy Statistics 2025 (jul. 2026), tabela 'JPS Rate Charges (Jamaican Dollars/kWh)' (fonte: JPS), p. 18 | https://www.mset.gov.jm/wp-content/uploads/2021/07/JAMAICA-ENERGY-STATISTICS-2025.pdf | 2026-09-14 |
| 2024 | 0,32 | 49,88 JMD/kWh | 56,95 | MSETT – Jamaica Energy Statistics 2025 (jul. 2026), tabela 'JPS Rate Charges (Jamaican Dollars/kWh)' (fonte: JPS), p. 18 | https://www.mset.gov.jm/wp-content/uploads/2021/07/JAMAICA-ENERGY-STATISTICS-2025.pdf | 2026-09-14 |
| 2025 | 0,32 | 51,67 JMD/kWh | 58,35 | MSETT – Jamaica Energy Statistics 2025 (jul. 2026), tabela 'JPS Rate Charges (Jamaican Dollars/kWh)' (fonte: JPS), p. 18 | https://www.mset.gov.jm/wp-content/uploads/2021/07/JAMAICA-ENERGY-STATISTICS-2025.pdf | 2026-09-14 |

Observações por linha (coluna `observacao` do CSV):

- 2015: Texto do IRP: 'Jamaica's average electricity tariff of US$0.27 per kWh in 2015'. A média em J$ não consta da edição 2019 de Jamaica Energy Statistics (só tarifas por classe, p. 16); residencial (Rate 10) = 3.222 J¢/kWh nessa edição (https://www.mset.gov.jm/wp-content/uploads/2020/06/Jamaica-Energy-Statistics-2019.pdf).
- 2016: Publicado em J¢/kWh (2.693,77) e US¢/kWh (22, inteiro); J$/kWh = J¢/100. Residencial (Rate 10) = 3.044,26 J¢/kWh.
- 2017: Publicado em J¢/kWh (3.265,09) e US¢/kWh (25); J$/kWh = J¢/100. Residencial (Rate 10) = 3.676,78 J¢/kWh.
- 2018: Publicado em J¢/kWh (3.576,45) e US¢/kWh (28); J$/kWh = J¢/100. Residencial (Rate 10) = 3.999,85 J¢/kWh. Conferência: a OUR (Determinação 2019-2024, p. 482) cita tarifa média de J$34/kWh em 2018-19.
- 2019: Publicado em J¢/kWh (3.569) e US¢/kWh (27); J$/kWh = J¢/100. A edição 2020 trazia 3.569,24 (2019p). Residencial (Rate 10) = 4.006 J¢/kWh.
- 2020: Publicado em J¢/kWh (3.993) e US¢/kWh (28); J$/kWh = J¢/100. A edição 2020 trazia 3.992,73 (2020p). Residencial (Rate 10) = 4.404 J¢/kWh.
- 2021: Publicado em J$/kWh e US$/kWh (2 casas). Mesmo valor na edição 2024 (4.657 J¢/kWh; 31 US¢). Residencial (Rate 10) = 52,04 J$/kWh.
- 2022: Publicado em J$/kWh e US$/kWh (2 casas). Mesmo valor na edição 2024 (5.579 J¢/kWh; 36 US¢). Pico associado ao preço dos combustíveis em 2022 (OUR, Determinação 2023, p. 85: fuel charge máximo de 24,711 US¢/kWh em set. 2022). Residencial (Rate 10) = 62,92 J$/kWh.
- 2023: Publicado em J$/kWh e US$/kWh (2 casas). Mesmo valor na edição 2024 (4.773 J¢/kWh; 31 US¢). Residencial (Rate 10) = 55,14 J$/kWh.
- 2024: Publicado em J$/kWh e US$/kWh (2 casas). A edição 2024 trazia o mesmo valor como preliminar (4.988 J¢/kWh; 32 US¢). Residencial (Rate 10) = 56,95 J$/kWh.
- 2025: Preliminar (2025p). Publicado em J$/kWh e US$/kWh (2 casas). Residencial (Rate 10) = 58,35 J$/kWh.

## Projetos de armazenamento (`armazenamento_projetos.csv`)

| Projeto | Ano | MW | MWh | Operador | Status | Fonte | Link | Acesso |
|---|---|---|---|---|---|---|---|---|
| Hunts Bay Hybrid Energy Storage System (HESS) | 2019 | 24,5 | 16,6 | JPS | operacional (comissionado em 2019-12) | OUR – JPS Annual Review 2023: Determination Notice, doc. 2023/ELE/012/DET.001 (2023-08-09), p. 79 | https://our.org.jm/wp-content/uploads/2023/08/JPS-2023-Annual-Tariff-Review-Determination-Notice.pdf | 2026-09-14 |
| IRP 2022 – BESS do plano preferido, 1ª fase (2024–2027) | 2022 | 264,0 | 528,0 | a contratar (plano do governo; procurement via GPE/JPS) | planejado (plano integrado de recursos, não contratado) | MSET – 2022 Jamaica Integrated Resource Plan (2018 IRP Review and Update), p. 15 e p. 58 | https://www.mset.gov.jm/wp-content/uploads/2024/11/2022-Jamaica-Integrated-Resource-Plan.pdf | 2026-09-14 |
| JPS – BESS em três ou mais locais (licitação EPC junto com 115 MW solar e 12 MW eólica) | 2026 | — | 171,5 | JPS | em contratação (EPC licitado em 2023-12; operação prevista do 4T2026 ao 3T2027) | pv magazine, 2023-12-07 (imprensa especializada; reporta o RFP da JPS) | https://www.pv-magazine.com/2023/12/07/jamaican-utility-launches-solar-plus-storage-wind-project-tender/ | 2026-09-14 |
| GPE – 2ª rodada de leilão: 220 MW renováveis + 110 MW / 220 MWh de BESS (co-localizado) | 2026 | 110,0 | 220,0 | IPPs a selecionar (leilão da Generation Procurement Entity) | em licitação (RFI lançado em 2026-03-19; leilão previsto para o 3T2026) | GPE – '220 MW Renewable Energy/110 MW BESS RFI Launch Session', 2026-03-06 | https://gpe.gov.jm/588-2/ | 2026-09-14 |

Observações por linha:

- Hunts Bay Hybrid Energy Storage System (HESS): Baterias de íon-lítio + flywheels (volantes de inércia) na subestação de Hunts Bay, Kingston; valor = MWh. Composição ADOTADA (decisão de 2026-09-14): a da OUR, no discurso do Diretor-Geral na inauguração em 2019-12-11: 21 MW de baterias + 3,5 MW de flywheel (https://our.org.jm/wp-content/uploads/2021/04/DG-Ansord-Hewitts-Presentation-JPS-storage-facility-2019-Dec-11.pdf). Fonte divergente, não usada: IRP 2022 (p. 39) descreve 20 MW Li-ion + 4,5 MW flywheel com 40 min de duração. Custo reportado pela imprensa: US$21,6 mi (pv magazine, 2018-03-05) a US$25 mi (Gleaner, 2019-04-14).
- IRP 2022 – BESS do plano preferido, 1ª fase (2024–2027): valor = MWh. O plano preferido prevê 493 MW de BESS de 2 horas: 264 MW em 2024–2027 (p. 58: 264 MW e 528 MWh) e 229 MW em 2033–2037 (p. 15). Serve de referência para a meta de 50% de renováveis em 2030; não é projeto contratado.
- JPS – BESS em três ou mais locais (licitação EPC junto com 115 MW solar e 12 MW eólica): valor = MWh. Sistemas de 1 a 50 MW em no mínimo três locais, 171,5 MWh no total; solar e dois BESS previstos para o 4T2026, o terceiro BESS para o 3T2027; MW total não informado. Gleaner (2025-05-09): investimento de US$300 mi em 2025–2028, 133 MW solar e '171,5 MW' de baterias (unidade divergente na imprensa), em substituição à usina a óleo de Hunts Bay. O documento original da JPS (jpsco.com) não pôde ser lido em 2026-09-14 porque o site bloqueia acesso automatizado; confirmar MW/MWh na fonte primária.
- GPE – 2ª rodada de leilão: 220 MW renováveis + 110 MW / 220 MWh de BESS (co-localizado): valor = MWh. BESS de 2 horas, tecnologia LFP; modelo BOO com PPA de 20 anos. Em 2026-05-05 o ministro Daryl Vaz anunciou no Parlamento licitação de 300 MW renováveis + 150 MW de baterias até agosto de 2026 (JIS, 2026-05-06, https://jis.gov.jm/gpe-launches-largest-renewable-energy-tender/); a página de tenders da GPE (2026-09-08) ainda lista '220 MW RFI Files'. A 1ª rodada (2023; 99,83 MW solar: Wigton 49,83 MW + SunTerra 50 MW, licenças em 2025-02) não inclui armazenamento.
