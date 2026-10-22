"""
Validação independente da limpeza feita no Google Sheets (Etapa 1).

Lê a planilha ORIGINAL (equivalente à aba Bronze), refaz a limpeza em Python
e confere se o resultado bate com o que está na aba Ouro.

Uso:
    pip install pandas openpyxl
    python validacao_limpeza.py caminho/pedidos_metalurgica_mezzalira.xlsx
"""
import re
import sys
from datetime import datetime

import pandas as pd

MESES_PT = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
            "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}

# Valores esperados na aba Ouro / resposta escrita
ESPERADO = {
    "linhas_vazias": 3,
    "duplicados": 4,
    "pedidos_unicos": 53,
    "total_geral": 178340.00,
    "cidade_lider": "Recife",
    "total_cidade_lider": 55260.00,
    "mes_pico_cidade_lider": "2026-03",
    "valor_pico": 29730.00,
}


def converter_data(valor):
    """Aceita data real, 'aaaa-mm-dd' e 'dd-mmm-aaaa' (mês abreviado em PT)."""
    if isinstance(valor, (datetime, pd.Timestamp)):
        return pd.Timestamp(valor)
    texto = str(valor).strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", texto):
        return pd.Timestamp(texto)
    m = re.fullmatch(r"(\d{1,2})-([a-zç]{3})-(\d{4})", texto.lower())
    if m:
        return pd.Timestamp(int(m[3]), MESES_PT[m[2]], int(m[1]))
    raise ValueError(f"Formato de data não reconhecido: {valor!r}")


def converter_valor(valor):
    """'R$ 1.200,00' -> 1200.0 ; números passam direto."""
    if isinstance(valor, str):
        limpo = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
        return float(limpo)
    return float(valor)


def padronizar_cidade(cidade):
    c = str(cidade).strip()
    return "Recife" if c.lower() in {"recife", "rec"} else c


def main(caminho):
    bruto = pd.read_excel(caminho, header=0)
    bruto.columns = ["Pedido", "Data", "Cliente", "Cidade", "Produto", "Valor"]
    print(f"Linhas lidas (Bronze): {len(bruto)}")

    # 1) linhas vazias
    vazias = bruto["Pedido"].isna()
    print(f"Linhas vazias: {vazias.sum()}")
    df = bruto[~vazias].copy()

    # 2) formatos
    df["Data"] = df["Data"].apply(converter_data)
    df["Valor"] = df["Valor"].apply(converter_valor)
    df["Cidade"] = df["Cidade"].apply(padronizar_cidade)

    # 3) duplicados (comparando todas as colunas, mantendo a 1ª ocorrência)
    antes = len(df)
    sem_dup = df.drop_duplicates(keep="first").copy()
    n_dup = antes - len(sem_dup)
    print(f"Duplicados removidos: {n_dup}")
    print(f"Pedidos únicos (Prata): {len(sem_dup)}")

    # 4) tabela dinâmica (aba Ouro)
    sem_dup["Mes"] = sem_dup["Data"].dt.to_period("M").astype(str)
    ouro = sem_dup.pivot_table(index="Cidade", columns="Mes", values="Valor",
                               aggfunc="sum", margins=True, margins_name="Total",
                               fill_value=0)
    print("\nAba Ouro (faturamento por cidade e mês, R$):")
    print(ouro.to_string(float_format=lambda x: f"{x:,.2f}"))

    # 5) resposta
    por_cidade = sem_dup.groupby("Cidade")["Valor"].sum().sort_values(ascending=False)
    cidade_lider = por_cidade.index[0]
    por_mes = sem_dup[sem_dup["Cidade"] == cidade_lider].groupby("Mes")["Valor"].sum()
    mes_pico = por_mes.idxmax()
    print(f"\nCidade que mais comprou: {cidade_lider} (R$ {por_cidade.iloc[0]:,.2f})")
    print(f"Mês de pico dessa cidade: {mes_pico} (R$ {por_mes.max():,.2f})")

    # 6) efeito de NÃO remover os duplicados (mostra por que a limpeza importa)
    sem_limpar_dup = df.groupby("Cidade")["Valor"].sum().sort_values(ascending=False)
    print("\nSe os duplicados NÃO fossem removidos, o ranking seria:")
    print(sem_limpar_dup.to_string(float_format=lambda x: f"R$ {x:,.2f}"))

    # 7) conferências automáticas
    checagens = {
        "linhas vazias": (int(vazias.sum()), ESPERADO["linhas_vazias"]),
        "duplicados": (n_dup, ESPERADO["duplicados"]),
        "pedidos únicos": (len(sem_dup), ESPERADO["pedidos_unicos"]),
        "total geral": (round(sem_dup["Valor"].sum(), 2), ESPERADO["total_geral"]),
        "cidade líder": (cidade_lider, ESPERADO["cidade_lider"]),
        "total da cidade líder": (round(por_cidade.iloc[0], 2), ESPERADO["total_cidade_lider"]),
        "mês de pico": (mes_pico, ESPERADO["mes_pico_cidade_lider"]),
        "valor do pico": (round(por_mes.max(), 2), ESPERADO["valor_pico"]),
        "número de pedido sem repetição": (bool(sem_dup["Pedido"].is_unique), True),
    }
    print("\nConferências:")
    ok = True
    for nome, (obtido, esperado) in checagens.items():
        passou = obtido == esperado
        ok &= passou
        print(f"  [{'OK' if passou else 'ERRO'}] {nome}: obtido={obtido} esperado={esperado}")
    print("\nTUDO CONFERE COM A ABA OURO." if ok else "\nHÁ DIVERGÊNCIAS: revisar.")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python validacao_limpeza.py caminho/da/planilha.xlsx")
    sys.exit(main(sys.argv[1]))
