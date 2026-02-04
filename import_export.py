import csv
import os
from datetime import datetime

import dados as ds
import persistencia as per
import constantes as con
from validacoes import validar_csv_produtos
from historico import registrar_movimentacao
from utils import limpa_tela, validar_cnpj


# =========================
# Utilitário
# =========================

def _nome_arquivo(base):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{base}_{timestamp}.csv"


# =========================
# EXPORTAÇÕES
# =========================

def exportar_produtos_csv():
    limpa_tela()

    if not ds.produtos:
        print("⚠️ Nenhum produto cadastrado para exportar.")
        input("\nPressione ENTER para continuar...")
        return

    caminho = _nome_arquivo("produtos")

    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=con.CAMPOS_PRODUTO)
        writer.writeheader()
        writer.writerows(ds.produtos)

    print(f"✅ Produtos exportados: {caminho}")
    input("\nPressione ENTER para continuar...")


def exportar_historico_csv():
    limpa_tela()

    if not ds.historico:
        print("⚠️ Nenhuma movimentação registrada.")
        input("\nPressione ENTER para continuar...")
        return

    caminho = _nome_arquivo("historico")

    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=ds.historico[0].keys())
        writer.writeheader()
        writer.writerows(ds.historico)

    print(f"✅ Histórico exportado: {caminho}")
    input("\nPressione ENTER para continuar...")


def exportar_fornecedores_csv():
    limpa_tela()

    if not ds.fornecedores:
        print("⚠️ Nenhum fornecedor cadastrado.")
        input("\nPressione ENTER para continuar...")
        return

    caminho = _nome_arquivo("fornecedores")

    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "nome", "cnpj", "telefone", "endereco", "ativo"]
        )
        writer.writeheader()
        writer.writerows(ds.fornecedores)

    print(f"✅ Fornecedores exportados: {caminho}")
    input("\nPressione ENTER para continuar...")


def exportar_financeiro_geral():
    limpa_tela()

    if not ds.historico:
        print("⚠️ Nenhuma movimentação registrada.")
        input("\nPressione ENTER para continuar...")
        return

    caminho = _nome_arquivo("financeiro_geral")

    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=ds.historico[0].keys())
        writer.writeheader()
        writer.writerows(ds.historico)

    print(f"✅ Financeiro exportado: {caminho}")
    input("\nPressione ENTER para continuar...")


def exportar_financeiro_periodo():
    limpa_tela()
    print("=== EXPORTAR FINANCEIRO POR PERÍODO ===\n")

    try:
        inicio = datetime.strptime(input("Data inicial (DD/MM/AAAA): "), "%d/%m/%Y")
        fim = datetime.strptime(input("Data final   (DD/MM/AAAA): "), "%d/%m/%Y")
    except ValueError:
        print("❌ Data inválida.")
        input("\nPressione ENTER para continuar...")
        return

    filtrado = [
        h for h in ds.historico
        if inicio <= datetime.strptime(h["data"], "%d/%m/%Y %H:%M") <= fim
    ]

    if not filtrado:
        print("⚠️ Nenhuma movimentação no período.")
        input("\nPressione ENTER para continuar...")
        return

    caminho = _nome_arquivo("financeiro_periodo")

    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=filtrado[0].keys())
        writer.writeheader()
        writer.writerows(filtrado)

    print(f"✅ Financeiro por período exportado: {caminho}")
    input("\nPressione ENTER para continuar...")


# =========================
# IMPORTAÇÕES
# =========================

def importar_produtos_csv():
    limpa_tela()
    caminho = input("Caminho do CSV: ").strip()

    if not os.path.exists(caminho):
        print("❌ Arquivo não encontrado.")
        input("\nPressione ENTER para continuar...")
        return

    with open(caminho, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        produtos_validos, erros = validar_csv_produtos(reader)

        fornecedores_validos = {f["id"] for f in ds.fornecedores}
        codigos_existentes = {p["codigo"] for p in ds.produtos}

        erros_fornecedor = []
        erros_duplicados = []

        importados = 0

        for i, linha in enumerate(produtos_validos, start=1):
            codigo = linha["codigo"].strip()
            fornecedor_id = linha.get("fornecedor_id", "").strip()

            # 🚫 Produto já cadastrado
            if codigo in codigos_existentes:
                erros_duplicados.append(
                    f"Linha {i}: produto com código '{codigo}' já existe."
                )
                continue

            # 🚫 Fornecedor inexistente
            if fornecedor_id not in fornecedores_validos:
                erros_fornecedor.append(
                    f"Linha {i}: fornecedor '{fornecedor_id}' não cadastrado."
                )
                continue

            produto = {
                "codigo": codigo,
                "nome": linha["nome"].strip(),
                "quantidade": int(linha["quantidade"]),
                "estoque_minimo": int(linha["estoque_minimo"]),
                "custo_unitario": float(linha["custo_unitario"]),
                "preco_venda": float(linha["preco_venda"]),
                "fornecedor_id": fornecedor_id,
                "ativo": str(linha["ativo"]).lower() in ("true", "1", "sim", "s")
            }

            ds.produtos.append(produto)
            codigos_existentes.add(codigo)
            importados += 1

            registrar_movimentacao(
                tipo=con.TIPO_IMPORTACAO,
                produto_nome=produto["nome"],
                codigo=produto["codigo"],
                quantidade=produto["quantidade"],
                custo_unitario=produto["custo_unitario"],
                preco_venda_unitario=produto["preco_venda"]
            )

    per.salvar_dados()

    limpa_tela()
    print("=== RESULTADO DA IMPORTAÇÃO ===")
    print(f"✔ Importados com sucesso: {importados}")
    print(f"⚠️ Erros validação: {len(erros)}")
    print(f"⚠️ Erros fornecedor: {len(erros_fornecedor)}")
    print(f"⚠️ Duplicados ignorados: {len(erros_duplicados)}")

    if erros:
        print("\nErros de validação:")
        for e in erros:
            print("-", e)

    if erros_fornecedor:
        print("\nFornecedores inexistentes:")
        for e in erros_fornecedor:
            print("-", e)

    if erros_duplicados:
        print("\nProdutos duplicados:")
        for e in erros_duplicados:
            print("-", e)

    input("\nPressione ENTER para continuar...")


def importar_fornecedores_csv():
    limpa_tela()
    caminho = input("Caminho do CSV: ").strip()

    if not os.path.exists(caminho):
        print("❌ Arquivo não encontrado.")
        input("\nPressione ENTER para continuar...")
        return

    importados = 0
    erros = []
    erros_duplicados = []

    # 🔑 CNPJs já existentes (chave lógica)
    cnpjs_existentes = {f["cnpj"] for f in ds.fornecedores}

    with open(caminho, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for i, linha in enumerate(reader, start=2):
            try:
                nome = linha.get("nome", "").strip()
                cnpj = linha.get("cnpj", "").strip()

                if not nome or not cnpj:
                    raise ValueError("Nome ou CNPJ vazio")

                if not validar_cnpj(cnpj):
                    raise ValueError("CNPJ inválido")

                # 🚫 Fornecedor já cadastrado
                if cnpj in cnpjs_existentes:
                    erros_duplicados.append(
                        f"Linha {i}: fornecedor com CNPJ '{cnpj}' já existe."
                    )
                    continue

                fornecedor = {
                    "id": f"FORN{len(ds.fornecedores) + 1:03d}",
                    "nome": nome,
                    "cnpj": cnpj,
                    "telefone": linha.get("telefone", "").strip(),
                    "endereco": linha.get("endereco", "").strip(),
                    "ativo": True
                }

                ds.fornecedores.append(fornecedor)
                cnpjs_existentes.add(cnpj)
                importados += 1

            except Exception as e:
                erros.append(f"Linha {i}: {e}")

    per.salvar_fornecedores()

    limpa_tela()
    print("=== RESULTADO DA IMPORTAÇÃO DE FORNECEDORES ===")
    print(f"✔ Importados com sucesso: {importados}")
    print(f"⚠️ Erros: {len(erros)}")
    print(f"⚠️ Duplicados ignorados: {len(erros_duplicados)}")

    if erros:
        print("\nErros:")
        for e in erros:
            print("-", e)

    if erros_duplicados:
        print("\nFornecedores duplicados:")
        for e in erros_duplicados:
            print("-", e)

    input("\nPressione ENTER para continuar...")


# =========================
# MENU CENTRAL
# =========================

def menu_export_import():
    acoes = {
        "1": ("Exportar produtos (CSV)", exportar_produtos_csv),
        "2": ("Exportar histórico (CSV)", exportar_historico_csv),
        "3": ("Exportar fornecedores (CSV)", exportar_fornecedores_csv),
        "4": ("Exportar financeiro geral (CSV)", exportar_financeiro_geral),
        "5": ("Exportar financeiro por período (CSV)", exportar_financeiro_periodo),
        "6": ("Importar produtos (CSV)", importar_produtos_csv),
        "7": ("Importar fornecedores (CSV)", importar_fornecedores_csv),
    }

    while True:
        limpa_tela()
        print("=== IMPORTAÇÃO / EXPORTAÇÃO ===\n")

        for k, (label, _) in acoes.items():
            print(f"{k} - {label}")

        print("0 - Voltar")

        op = input("\nEscolha: ").strip()

        if op == "0":
            return

        acao = acoes.get(op)
        if not acao:
            print("❌ Opção inválida.")
            input("\nPressione ENTER para continuar...")
            continue

        limpa_tela()
        acao[1]()