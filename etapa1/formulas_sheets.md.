# Fórmulas e recursos usados no Google Sheets (Etapa 1)

A limpeza foi feita com os recursos nativos do Sheets (planilha em local **Brasil**).
O script `validacao_limpeza.py` refaz tudo em Python e confere o resultado.

## Prata

| Problema | Recurso usado |
|---|---|
| Linhas vazias | Filtro na coluna Pedido por "Está vazio" e exclusão das linhas |
| Duplicados | Dados > Limpeza de dados > Remover duplicatas (colunas A a F, sem `Linha_Bronze`) |
| Cidade escrita de formas diferentes | Localizar e substituir (Ctrl+H), só na coluna D, com "Corresponder ao conteúdo inteiro da célula" |
| Valores como texto ("R$ 630,00") | Ctrl+H removendo `R$`, depois Formatar > Número > Moeda |
| Datas em formatos diferentes | Formatar > Número > Data (dd/mm/aaaa) |

## Validação cruzada das datas (fórmula auxiliar)

Usada em uma coluna temporária para comparar com o resultado do recurso nativo.
Os resultados foram idênticos nas 53 linhas.

```
=SE(ÉNÚM(B2);B2;SE(EXT.TEXTO(B2;5;1)="-";DATA(ESQUERDA(B2;4);EXT.TEXTO(B2;6;2);EXT.TEXTO(B2;9;2));DATA(DIREITA(B2;4);(PROCURAR(EXT.TEXTO(B2;4;3);"janfevmarabrmaijunjulagosetoutnovdez")+2)/3;ESQUERDA(B2;2))))
```

## Rastreabilidade

Coluna `Linha_Bronze` na Prata: linha de origem de cada pedido na aba Bronze.
Linhas da Bronze que não aparecem na Prata: 16, 35, 53 (vazias) e 25, 33, 36, 61 (duplicadas).

## Conferências feitas na Prata

| Conferência | Fórmula | Resultado |
|---|---|---|
| Pedidos | `=CONT.VALORES(A2:A)` | 53 |
| Pedidos sem repetição | `=CONT.ÚNICOS(A2:A)` | 53 |
| Cidades | `=CONT.ÚNICOS(D2:D)` | 5 |
| Datas válidas | `=CONT.NÚM(B2:B)` | 53 |
| Faixa de datas | `=MÍNIMO(B2:B)` / `=MÁXIMO(B2:B)` | 01/01/2026 / 26/04/2026 |
| Total | `=SOMA(F2:F)` | R$ 178.340,00 |

## Ouro

Tabela dinâmica sobre `Prata!A1:F54`: Linhas = Cidade, Colunas = Data (agrupada por Ano-Mês), Valores = SOMA de Valor (R$).
