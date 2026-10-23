# Desafio: do dado bagunçado ao primeiro assistente
**Metalúrgica Mezzalira · Processo seletivo do Citi (área de dados)**

## Resposta da Etapa 1

> **Recife** foi a cidade que mais comprou (R$ 55.260,00 no período), e **março de 2026** foi o seu mês de maior faturamento (R$ 29.730,00).

Março também foi o mês de maior faturamento geral (R$ 79.460,00). Os dados vão de 01/01 a 26/04/2026, então abril está incompleto.

O resultado depende de duas decisões registradas na aba Log:
- **Duplicados:** 4 pedidos repetidos, todos de Caruaru. Se não fossem removidos, Caruaru somaria R$ 60.590,00 e passaria Recife.
- **"REC" = Recife:** interpretação assumida e registrada como dúvida.

## Entregas

| Item | Onde |
|---|---|
| Planilha (abas Bronze, Prata, Log e Ouro) | https://docs.google.com/spreadsheets/d/1XKk1FASJ2rDJvFm9eHV_3j7j_0KjMhtWl9IYu-xO_io/edit?usp=sharing |
| Resposta escrita | Este README e a aba Log |
| Códigos e fórmulas | `etapa1/` |
| Instruções finais do Gem | `etapa2/instrucoes_gem.md` |
| Testes e prints | `etapa2/testes.md` e `prints/` |

## Estrutura

```
etapa1/
  formulas_sheets.md       fórmulas e recursos usados na Prata e na Ouro
  validacao_limpeza.py     refaz a limpeza em Python e confere a aba Ouro
etapa2/
  instrucoes_gem.md        instruções finais do assistente
  testes.md                8 perguntas de teste, esperado e resultado
prints/                    prints das respostas do Gem
```

## Etapa 1: arquitetura Bronze, Prata, Log e Ouro

- **Bronze:** cópia intocada da planilha original (60 linhas de dados, protegida).
- **Prata:** dados corrigidos (53 pedidos), com a coluna `Linha_Bronze` para rastrear cada pedido até a origem.
- **Log:** cada correção, as linhas afetadas e a justificativa das decisões com dúvida.
- **Ouro:** tabela dinâmica de faturamento por cidade e mês, com gráfico.

Problemas tratados: 3 linhas vazias, 4 duplicados, cidade escrita de várias formas (Recife, recife, REC), 7 valores como texto e 17 datas em texto (em dois formatos).

## Validação em Python

O script refaz a limpeza a partir da planilha original e confere o resultado com a aba Ouro (pedidos únicos, total, cidade líder, mês de pico e unicidade dos pedidos).

```bash
pip install -r requirements.txt
python etapa1/validacao_limpeza.py caminho/pedidos_metalurgica_mezzalira.xlsx
```

Saída esperada: `TUDO CONFERE COM A ABA OURO.`

A planilha original não está neste repositório.

## Etapa 2: assistente de manutenção (Gemini Gem)

Assistente que responde só com base no Manual de Procedimentos de Manutenção (Revisão 3). Quando a resposta não está no manual, usa uma frase fixa de "não sei". Recusa tentativas de sair do papel. Detalhes em `etapa2/`.
