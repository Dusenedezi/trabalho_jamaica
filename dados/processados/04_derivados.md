# Derivados calculados em `transform.py`

> Gerado por `processamento/gerar_tabelas.py` em 2026-09-14 a partir de `dados/processados/` (acesso às fontes em 2026-09-14). Números em formato pt-BR. Traço (—) = sem dado. Comparadores ausentes em uma fonte simplesmente não aparecem.

## PIB per capita PPP como % de República Dominicana (`pib_pc_ppp_pct_dom.csv`)

Fórmula: valor do país ÷ valor de República Dominicana × 100, ano a ano (US$ internacionais constantes de 2021).

| Ano | Jamaica | Trinidad e Tobago | Barbados | Costa Rica | Panamá | Colômbia | América Latina e Caribe |
|---|---|---|---|---|---|---|---|
| 1990 | 121,2 | 162,0 | 262,0 | 149,8 | 140,1 | 136,5 | 169,6 |
| 1995 | 118,1 | 160,2 | 207,3 | 145,3 | 139,2 | 129,9 | 155,0 |
| 2000 | 88,7 | 180,2 | 195,6 | 128,7 | 133,7 | 99,2 | 134,6 |
| 2005 | 85,5 | 245,7 | 183,3 | 130,7 | 140,3 | 99,8 | 129,5 |
| 2010 | 65,5 | 234,7 | 136,7 | 124,7 | 151,8 | 93,7 | 117,2 |
| 2015 | 55,3 | 216,8 | 109,3 | 118,3 | 166,5 | 93,6 | 104,4 |
| 2020 | 50,6 | 157,2 | 83,9 | 114,4 | 137,5 | 81,2 | 89,6 |
| 2025 | 46,3 | 129,2 | 90,2 | 115,9 | 152,9 | 76,5 | 82,7 |

## PIB por pessoa ocupada, índice 1991 = 100 (`pib_por_ocupado_indice_1991.csv`)

Fórmula: valor do ano ÷ valor de 1991 × 100. Série em US$ PPP constantes de 2021, portanto o índice mede variação real.

| Ano | Jamaica | República Dominicana | Trinidad e Tobago | Barbados | Costa Rica | Panamá | Colômbia | América Latina e Caribe |
|---|---|---|---|---|---|---|---|---|
| 1995 | 113,0 | 115,3 | 104,3 | 91,4 | 109,3 | 101,5 | 107,0 | 103,9 |
| 2000 | 108,2 | 138,0 | 126,9 | 95,0 | 114,4 | 115,4 | 115,2 | 110,8 |
| 2005 | 113,0 | 152,7 | 164,3 | 95,9 | 119,3 | 126,8 | 114,7 | 110,5 |
| 2010 | 111,6 | 180,8 | 190,9 | 91,1 | 141,9 | 166,4 | 125,5 | 120,1 |
| 2015 | 100,9 | 198,7 | 208,9 | 90,1 | 149,8 | 209,2 | 140,6 | 125,3 |
| 2020 | 95,5 | 214,0 | 178,4 | 77,6 | 174,8 | 204,0 | 146,9 | 125,0 |
| 2025 | 96,0 | 242,4 | 182,6 | 96,5 | 203,5 | 258,9 | 156,1 | 126,9 |

## Capacidade solar por habitante, kW por 1.000 habitantes (`solar_capacidade_kw_por_mil_hab.csv`)

Fórmula: capacidade (MW) ÷ população (SP.POP.TOTL) × 1.000.000.

| Ano | Jamaica | República Dominicana | Trinidad e Tobago | Barbados | Costa Rica | Panamá | Colômbia |
|---|---|---|---|---|---|---|---|
| 2000 | — | — | 0,26 | — | 0,06 | — | 0,02 |
| 2005 | 0,07 | — | 1,36 | 0,74 | 0,12 | — | 0,03 |
| 2010 | 0,36 | — | 2,15 | 3,63 | 0,14 | — | 0,03 |
| 2015 | 2,32 | 2,26 | 2,96 | 11,09 | 1,77 | 10,78 | 0,03 |
| 2020 | 37,80 | 35,02 | 2,93 | 174,50 | 11,08 | 54,75 | 1,45 |
| 2025 | 41,09 | 180,81 | 70,64 | 245,36 | 16,04 | 212,93 | 32,31 |

## Human Capital Index, ano mais recente (`tabela_hci.csv`)

| País | HCI_2020 |
|---|---|
| Costa Rica | 0,629 |
| Colômbia | 0,604 |
| Trinidad e Tobago | 0,603 |
| Jamaica | 0,535 |
| República Dominicana | 0,503 |
| Panamá | 0,502 |

## Tarifa de eletricidade em US$ com o câmbio do WDI (`tarifa_eletricidade_usd.csv`)

Fórmula: J$/kWh ÷ câmbio médio anual (PA.NUS.FCRF, série `cambio_jmd_usd`). A média do sistema recalculada serve para conferir o US$ publicado pelo MSETT (arredondado a 2 casas); 2015 não tem valor em J$ na fonte.

| Ano | Média do sistema, US$/kWh (publicado) | Média do sistema, J$/kWh | Residencial, J$/kWh | Câmbio, J$ por US$ (PA.NUS.FCRF) | Média do sistema, US$/kWh (calculado) | Residencial, US$/kWh (calculado) |
|---|---|---|---|---|---|---|
| 2015 | 0,270 | — | 32,220 | 116,970 | — | 0,275 |
| 2016 | 0,220 | 26,938 | 30,443 | 125,095 | 0,215 | 0,243 |
| 2017 | 0,250 | 32,651 | 36,768 | 127,965 | 0,255 | 0,287 |
| 2018 | 0,280 | 35,764 | 39,998 | 128,872 | 0,278 | 0,310 |
| 2019 | 0,270 | 35,690 | 40,060 | 133,312 | 0,268 | 0,300 |
| 2020 | 0,280 | 39,930 | 44,040 | 142,403 | 0,280 | 0,309 |
| 2021 | 0,310 | 46,570 | 52,040 | 150,790 | 0,309 | 0,345 |
| 2022 | 0,360 | 55,790 | 62,920 | 153,427 | 0,364 | 0,410 |
| 2023 | 0,310 | 47,730 | 55,140 | 154,159 | 0,310 | 0,358 |
| 2024 | 0,320 | 49,880 | 56,950 | 156,440 | 0,319 | 0,364 |
| 2025 | 0,320 | 51,670 | 58,350 | 159,096 | 0,325 | 0,367 |
