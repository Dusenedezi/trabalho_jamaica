# Painel: todos os indicadores no último ano com dado para os países presentes

> Gerado por `processamento/gerar_tabelas.py` em 2026-09-14 a partir de `dados/processados/` (acesso às fontes em 2026-09-14). Números em formato pt-BR. Traço (—) = sem dado. Comparadores ausentes em uma fonte simplesmente não aparecem.

"Último ano comum" = último ano com dado para todos os países que a fonte cobre (mesmo critério de `transform.py`, função `ultimo_ano_comum`); por isso o ano varia entre indicadores. Quando nenhum ano tem dado para todos os países (dívida no WDI), usa-se o último ano com dado para Jamaica. A posição é só ordem de grandeza: em dívida e importações de energia, valor maior não é "melhor".

| Indicador | Ano | Jamaica | República Dominicana | Trinidad e Tobago | Barbados | Costa Rica | Panamá | Colômbia | América Latina e Caribe | Jamaica (1 = maior valor) |
|---|---|---|---|---|---|---|---|---|---|---|
| IDH (Índice 0–1) | 2023 | 0,720 | 0,776 | 0,807 | 0,811 | 0,833 | 0,839 | 0,788 | — | 7º de 7 |
| PIB per capita PPP (US$ internacionais constantes de 2021) | 2025 | 11.358 | 24.543 | 31.722 | 22.127 | 28.443 | 37.516 | 18.779 | 20.287 | 8º de 8 |
| PIB por pessoa ocupada (US$ internacionais constantes de 2021 (PPP)) | 2025 | 20.659 | 54.043 | 68.867 | 44.125 | 64.823 | 81.808 | 40.369 | 43.303 | 8º de 8 |
| Human Capital Index (Índice 0–1) | 2020 | 0,535 | 0,503 | 0,603 | — | 0,629 | 0,502 | 0,604 | — | 4º de 6 |
| Importações líquidas de energia (%) | 2022 | 112,6 | 94,4 | -75,5 | — | 53,1 | 171,2 | -139,1 | -2,8 | 2º de 7 |
| Dívida do governo central (% do PIB) | 2020 | 97,9 | — | — | — | — | — | 91,2 | 77,7 | 1º de 3 |
| WGI Rule of Law (Escore padronizado, aprox. −2,5 a 2,5) | 2024 | -0,08 | -0,18 | -0,37 | 0,73 | 0,62 | -0,26 | -0,56 | — | 3º de 7 |
| Capacidade solar instalada (MW) | 2025 | 116,6 | 2.083,1 | 96,6 | 69,3 | 82,6 | 973,4 | 1.726,2 | — | 4º de 7 |
| Solar na geração elétrica (% da geração) | 2024 | 3,05 | 6,45 | 0,10 | 9,01 | 0,82 | 7,37 | 3,85 | — | 5º de 7 |
| Renováveis na geração elétrica (% da geração) | 2024 | 12,6 | 18,9 | 0,1 | 9,0 | 99,9 | 68,0 | 61,3 | — | 5º de 7 |
| População (milhões de pessoas (valor ÷ 1e6)) | 2025 | 2,84 | 11,52 | 1,37 | 0,28 | 5,15 | 4,57 | 53,43 | 666,59 | 6º de 8 |
