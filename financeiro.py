from datetime import datetime

import dados as ds
import constantes as con
from utils import limpa_tela
from import_export import (
    exportar_financeiro_geral,
    exportar_financeiro_periodo
)


# =========================
# RELATÓRIOS (TELA)
# =========================

def relatorio_margem():
    limpa_tela()
    print("=== RELATÓRIO DE MARGEM DE LUCRO ===\n")

    if not ds.produtos:
        print("⚠️ Nenhum produto cadastrado.")
        input("\nPressione ENTER para continuar...")
        return

    encontrou = False

    for p in ds.produtos:
        if not p.get("ativo", False):
            continue

        custo = p.get("custo_unitario", 0)
        preco = p.get("preco_venda", 0)

        if custo <= 0 or preco <= 0:
            continue

        margem_unitaria = preco - custo
        margem_percentual = (margem_unitaria / preco) * 100
        encontrou = True

        print("-" * 40)
        print(f"Produto: {p['nome']} ({p['codigo']})")
        print(f"Custo unitário:  R$ {custo:.2f}")
        print(f"Preço de venda:  R$ {preco:.2f}")
        print(f"Margem unitária: R$ {margem_unitaria:.2f}")
        print(f"Margem (%):      {margem_percentual:.2f}%")

    if not encontrou:
        print("⚠️ Nenhum produto válido para cálculo de margem.")

    input("\nPressione ENTER para continuar...")


# =========================
# COMPRAS / ENTRADAS
# =========================

def relatorio_compras():
    limpa_tela()
    print("=== RELATÓRIO DE COMPRAS (ENTRADAS / IMPORTAÇÕES) ===\n")

    if not ds.historico:
        print("⚠️ Nenhuma movimentação registrada.")
        input("\nPressione ENTER para continuar...")
        return

    total_compras = sum(
        h.get("custo_total", 0)
        for h in ds.historico
        if h.get("tipo") in (con.TIPO_ENTRADA, con.TIPO_IMPORTACAO)
    )

    if total_compras == 0:
        print("⚠️ Nenhuma compra registrada.")
    else:
        print(f"Total investido em estoque: R$ {total_compras:.2f}")

    input("\nPressione ENTER para continuar...")


# =========================
# FATURAMENTO
# =========================

def relatorio_faturamento():
    limpa_tela()
    print("=== RELATÓRIO DE FATURAMENTO (SAÍDAS) ===\n")

    if not ds.historico:
        print("⚠️ Nenhuma movimentação registrada.")
        input("\nPressione ENTER para continuar...")
        return

    total = sum(
        h.get("receita_total", 0)
        for h in ds.historico
        if h.get("tipo") == con.TIPO_SAIDA
    )

    if total == 0:
        print("⚠️ Nenhuma venda registrada.")
    else:
        print(f"Total faturado: R$ {total:.2f}")

    input("\nPressione ENTER para continuar...")


# =========================
# LUCRO COM CMV
# =========================

def relatorio_lucro():
    limpa_tela()
    print("=== RELATÓRIO DE LUCRO (COM CMV) ===\n")

    if not ds.historico:
        print("⚠️ Nenhuma movimentação registrada.")
        input("\nPressione ENTER para continuar...")
        return

    receita_total = 0.0
    cmv = 0.0

    for h in ds.historico:
        if h.get("tipo") == con.TIPO_SAIDA:
            qtd = abs(h.get("quantidade", 0))
            receita_total += h.get("preco_venda_unitario", 0) * qtd
            cmv += h.get("custo_unitario", 0) * qtd

    if receita_total == 0:
        print("⚠️ Nenhuma venda registrada.")
    else:
        lucro = receita_total - cmv
        print(f"Receita total: R$ {receita_total:.2f}")
        print(f"CMV:           R$ {cmv:.2f}")
        print(f"Lucro bruto:   R$ {lucro:.2f}")

    input("\nPressione ENTER para continuar...")


# =========================
# RELATÓRIO POR PERÍODO
# =========================

def relatorio_periodo():
    limpa_tela()
    print("=== RELATÓRIO FINANCEIRO POR PERÍODO ===\n")

    if not ds.historico:
        print("⚠️ Nenhuma movimentação registrada.")
        input("\nPressione ENTER para continuar...")
        return

    try:
        inicio = datetime.strptime(
            input("Data inicial (DD/MM/AAAA): "), "%d/%m/%Y"
        )
        fim = datetime.strptime(
            input("Data final   (DD/MM/AAAA): "), "%d/%m/%Y"
        )
    except ValueError:
        print("❌ Formato inválido.")
        input("\nPressione ENTER para continuar...")
        return

    limpa_tela()
    print("=== MOVIMENTAÇÕES NO PERÍODO ===\n")

    encontrou = False

    for h in ds.historico:
        data_mov = datetime.strptime(h["data"], "%d/%m/%Y %H:%M")
        if inicio <= data_mov <= fim:
            encontrou = True
            print("-" * 30)
            print(f"Data: {h['data']}")
            print(f"Tipo: {h['tipo']}")
            print(f"Produto: {h['produto']} ({h['codigo']})")
            print(f"Quantidade: {h['quantidade']}")

    if not encontrou:
        print("⚠️ Nenhuma movimentação encontrada.")

    input("\nPressione ENTER para continuar...")


# =========================
# RESUMO FINANCEIRO
# =========================

def resumo_financeiro():
    limpa_tela()
    print("=== RESUMO FINANCEIRO ===\n")

    if not ds.historico:
        print("⚠️ Nenhuma movimentação registrada.")
        input("\nPressione ENTER para continuar...")
        return

    receita = cmv = compras = 0.0
    itens_vendidos = 0

    for h in ds.historico:
        tipo = h.get("tipo")

        if tipo == con.TIPO_SAIDA:
            qtd = abs(h.get("quantidade", 0))
            receita += h.get("preco_venda_unitario", 0) * qtd
            cmv += h.get("custo_unitario", 0) * qtd
            itens_vendidos += qtd

        elif tipo in (con.TIPO_ENTRADA, con.TIPO_IMPORTACAO):
            compras += h.get("custo_total", 0)

    lucro = receita - cmv

    print(f"Receita total (vendas): R$ {receita:.2f}")
    print(f"CMV:                   R$ {cmv:.2f}")
    print(f"Lucro bruto:           R$ {lucro:.2f}")
    print(f"Compras (estoque):     R$ {compras:.2f}")
    print(f"Itens vendidos:        {itens_vendidos}")

    input("\nPressione ENTER para continuar...")


# =========================
# MENU FINANCEIRO
# =========================

def menu():
    acoes = {
        "1": relatorio_margem,
        "2": relatorio_compras,
        "3": relatorio_faturamento,
        "4": relatorio_lucro,
        "5": relatorio_periodo,
        "6": resumo_financeiro,
        "7": exportar_financeiro_geral,
        "8": exportar_financeiro_periodo
    }

    while True:
        limpa_tela()
        print("===== MENU FINANCEIRO =====")
        print("1 - Relatório de margem por produto")
        print("2 - Relatório de compras (entradas)")
        print("3 - Relatório de faturamento (saídas)")
        print("4 - Relatório de lucro (CMV)")
        print("5 - Relatório financeiro por período")
        print("6 - Resumo financeiro geral")
        print("7 - Exportar financeiro geral (CSV)")
        print("8 - Exportar financeiro por período (CSV)")
        print("0 - Voltar")

        op = input("\nEscolha: ").strip()

        if op == "0":
            return

        acao = acoes.get(op)
        if not acao:
            print("❌ Opção inválida.")
            input("\nPressione ENTER para continuar...")
            continue

        acao()