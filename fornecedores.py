import dados as ds
import persistencia as per
from utils import limpa_tela, validar_cnpj
from import_export import (
    exportar_fornecedores_csv,
    importar_fornecedores_csv
)


# =========================
# Funções auxiliares
# =========================

def gerar_id_fornecedor():
    return f"FORN{len(ds.fornecedores) + 1:03d}"


def fornecedor_existente_por_cnpj(cnpj):
    for f in ds.fornecedores:
        if f["cnpj"] == cnpj:
            return f
    return None


def _buscar_fornecedor_por_id(id_forn):
    id_forn = id_forn.strip().upper()
    for f in ds.fornecedores:
        if f["id"].upper() == id_forn:
            return f
    return None


# =========================
# 1. Cadastrar fornecedor
# =========================

def cadastrar_fornecedor():
    limpa_tela()
    print("=== Cadastro de Fornecedor ===\n")

    nome = input("Nome do fornecedor: ").strip()
    cnpj = input("CNPJ: ").strip()
    telefone = input("Telefone: ").strip()
    endereco = input("Endereço: ").strip()

    if not nome or not cnpj:
        print("\n❌ Nome e CNPJ são obrigatórios.")
        input("\nPressione ENTER para continuar...")
        return

    if not validar_cnpj(cnpj):
        print("\n❌ CNPJ inválido.")
        input("\nPressione ENTER para continuar...")
        return

    if fornecedor_existente_por_cnpj(cnpj):
        print("\n❌ Já existe um fornecedor com este CNPJ.")
        input("\nPressione ENTER para continuar...")
        return

    fornecedor = {
        "id": gerar_id_fornecedor(),
        "nome": nome,
        "cnpj": cnpj,
        "telefone": telefone,
        "endereco": endereco,
        "ativo": True
    }

    ds.fornecedores.append(fornecedor)
    per.salvar_fornecedores()

    print("\n✅ Fornecedor cadastrado com sucesso!")
    input("\nPressione ENTER para continuar...")


# =========================
# 2. Listar fornecedores
# =========================

def listar_fornecedores(mostrar_inativos=False):
    limpa_tela()
    print("=== Fornecedores ===\n")

    encontrados = False

    for f in ds.fornecedores:
        if not mostrar_inativos and not f["ativo"]:
            continue

        encontrados = True
        print("-" * 30)
        print(f"ID: {f['id']}")
        print(f"Nome: {f['nome']}")
        print(f"CNPJ: {f['cnpj']}")
        print(f"Telefone: {f['telefone']}")
        print(f"Endereço: {f['endereco']}")
        print(f"Status: {'Ativo' if f['ativo'] else 'Inativo'}")

    if not encontrados:
        print("Nenhum fornecedor encontrado.")

    input("\nPressione ENTER para continuar...")


# =========================
# 3. Ativar / Inativar fornecedor
# =========================

def alterar_status_fornecedor():
    limpa_tela()
    print("=== Ativar / Inativar Fornecedor ===\n")

    if not ds.fornecedores:
        print("⚠️ Nenhum fornecedor cadastrado.")
        input("\nPressione ENTER para continuar...")
        return

    id_forn = input("Digite o ID do fornecedor: ").strip()
    fornecedor = _buscar_fornecedor_por_id(id_forn)

    if not fornecedor:
        print("\n❌ Fornecedor não encontrado.")
        input("\nPressione ENTER para continuar...")
        return

    print("\nFornecedor encontrado:")
    print(f"ID: {fornecedor['id']}")
    print(f"Nome: {fornecedor['nome']}")
    print(f"Status atual: {'Ativo' if fornecedor['ativo'] else 'Inativo'}")

    op = input("\nDeseja alterar o status? (S/N): ").strip().upper()
    if op != "S":
        print("\nOperação cancelada.")
        input("\nPressione ENTER para continuar...")
        return

    fornecedor["ativo"] = not fornecedor["ativo"]
    per.salvar_fornecedores()

    print("\n✅ Status alterado com sucesso.")
    input("\nPressione ENTER para continuar...")


# =========================
# MENU DE FORNECEDORES
# =========================

ACOES_FORNECEDORES = {
    "1": {
        "label": "Cadastrar fornecedor",
        "func": cadastrar_fornecedor
    },
    "2": {
        "label": "Listar fornecedores ativos",
        "func": lambda: listar_fornecedores(False)
    },
    "3": {
        "label": "Listar todos os fornecedores",
        "func": lambda: listar_fornecedores(True)
    },
    "4": {
        "label": "Ativar / Inativar fornecedor",
        "func": alterar_status_fornecedor
    },
    "5": {
        "label": "Exportar fornecedores (CSV)",
        "func": exportar_fornecedores_csv
    },
    "6": {
        "label": "Importar fornecedores (CSV)",
        "func": importar_fornecedores_csv
    }
}


def menu_fornecedores():
    while True:
        limpa_tela()
        print("=== MENU DE FORNECEDORES ===\n")

        for key, acao in ACOES_FORNECEDORES.items():
            print(f"{key} - {acao['label']}")

        print("0 - Voltar")

        op = input("\nEscolha: ").strip()

        if op == "0":
            return

        acao = ACOES_FORNECEDORES.get(op)
        if not acao:
            print("\n❌ Opção inválida.")
            input("\nPressione ENTER para continuar...")
            continue

        limpa_tela()
        acao["func"]()