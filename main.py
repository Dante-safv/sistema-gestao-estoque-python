# Sistema de Gestão de Estoque (SGE)

import estoque as est
import persistencia as per
import usuarios as us
import dados as ds
import constantes as con
import import_export as ie
import fornecedores as forn
import financeiro as fin
from utils import limpa_tela


# =========================
# Ações do menu principal
# =========================

ACOES = {
    "1": {
        "label": "Cadastrar produto",
        "func": est.cadastrar_produto,
        "roles": [con.ROLE_ADMIN]
    },
    "2": {
        "label": "Editar produto",
        "func": est.editar_produto,
        "roles": [con.ROLE_ADMIN]
    },
    "3": {
        "label": "Listar produtos",
        "func": est.listar_produtos,
        "roles": [
            con.ROLE_ADMIN,
            con.ROLE_GERENTE,
            con.ROLE_CONTADOR,
            con.ROLE_OPERADOR
        ]
    },
    "4": {
        "label": "Entrada de produto",
        "func": est.entrada_produto,
        "roles": [
            con.ROLE_ADMIN,
            con.ROLE_GERENTE,
            con.ROLE_OPERADOR
        ]
    },
    "5": {
        "label": "Saída de produto",
        "func": est.saida_produto,
        "roles": [
            con.ROLE_ADMIN,
            con.ROLE_GERENTE,
            con.ROLE_OPERADOR
        ]
    },
    "6": {
        "label": "Histórico",
        "func": est.historico_produto,
        "roles": [
            con.ROLE_ADMIN,
            con.ROLE_GERENTE,
            con.ROLE_OPERADOR
        ]
    },
    "7": {
        "label": "Importar / Exportar dados",
        "func": ie.menu_export_import,
        "roles": [
            con.ROLE_ADMIN,
            con.ROLE_GERENTE,
            con.ROLE_CONTADOR
        ]
    },
    "8": {
        "label": "Gerenciar fornecedores",
        "func": forn.menu_fornecedores,
        "roles": [
            con.ROLE_ADMIN,
            con.ROLE_GERENTE
        ]
    },
    "9": {
        "label": "Financeiro",
        "func": fin.menu,
        "roles": [
            con.ROLE_ADMIN,
            con.ROLE_GERENTE,
            con.ROLE_CONTADOR
        ]
    },
    "10": {
        "label": "Gerenciar usuários",
        "func": us.menu_usuarios,
        "roles": [con.ROLE_ADMIN]
    },
    "11": {
        "label": "Logout",
        "func": us.logout,
        "roles": [
            con.ROLE_ADMIN,
            con.ROLE_GERENTE,
            con.ROLE_CONTADOR,
            con.ROLE_OPERADOR
        ]
    }
}


# =========================
# Menu principal
# =========================

def menu():
    while True:
        limpa_tela()

        print("===== MENU PRINCIPAL =====")
        print(
            f"Usuário logado: "
            f"{ds.usuario_logado['usuario']} "
            f"({ds.usuario_logado['role']})\n"
        )

        # exibe apenas opções permitidas
        for key, acao in ACOES.items():
            if ds.usuario_logado["role"] in acao["roles"]:
                print(f"{key} - {acao['label']}")

        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            limpa_tela()
            print("Saindo do sistema...")
            break

        acao = ACOES.get(opcao)

        if not acao:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")
            continue

        if ds.usuario_logado["role"] not in acao["roles"]:
            print("❌ Acesso negado.")
            input("\nPressione ENTER para continuar...")
            continue

        limpa_tela()
        acao["func"]()

        input("\nPressione ENTER para voltar ao menu...")
        limpa_tela()


# =========================
# Inicialização do sistema
# =========================

if __name__ == "__main__":
    per.carregar_dados()
    per.carregar_fornecedores()

    us.carregar_usuarios()
    us.login()

    menu()