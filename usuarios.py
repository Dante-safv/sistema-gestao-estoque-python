import dados
import constantes as con
from utils import limpa_tela, verificar_alerta_estoque
from persistencia import carregar_usuarios, salvar_usuarios


# =========================
# Autenticação
# =========================

def login():
    if not hasattr(dados, "usuarios"):
        carregar_usuarios()

    if not dados.usuarios:
        print("⚠️ Nenhum usuário cadastrado.")
        print("Crie um usuário ADMIN no arquivo usuarios.json.\n")
        return

    while True:
        limpa_tela()
        print("=== LOGIN ===")

        usuario_input = input("Usuário: ").strip()
        senha_input = input("Senha: ").strip()

        for u in dados.usuarios:
            if (
                u.get("usuario", "").lower() == usuario_input.lower()
                and u.get("senha") == senha_input
                and u.get("ativo", True)
            ):
                dados.usuario_logado = u
                print(f"\nBem-vindo, {u['usuario']} ({u['role']})\n")

                # alerta de estoque SOMENTE no login
                if verificar_alerta_estoque():
                    input("\nPressione ENTER para continuar...")

                return

        print("\nUsuário ou senha inválidos.")
        input("Pressione ENTER para tentar novamente...")


def logout():
    if not dados.usuario_logado:
        print("Nenhum usuário logado.")
        return

    op = input("Deseja trocar de usuário? (S/N): ").strip().upper()

    if op == "S":
        dados.usuario_logado = None
        print("Logout realizado.")
        login()  # sem pausa para evitar duplicação
    else:
        print("Logout cancelado.")


# =========================
# Gerenciamento de Usuários
# =========================

def menu_usuarios():
    acoes = {
        "1": listar_usuarios,
        "2": criar_usuario,
        "3": alterar_status_usuario,
        "4": editar_usuario
    }

    while True:
        limpa_tela()
        print("=== GERENCIAMENTO DE USUÁRIOS ===")
        print("1 - Listar usuários")
        print("2 - Criar usuário")
        print("3 - Ativar / Inativar usuário")
        print("4 - Editar usuário")
        print("0 - Voltar")

        op = input("Escolha: ").strip()

        if op == "0":
            return

        acao = acoes.get(op)
        if not acao:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")
            continue

        limpa_tela()
        acao()
        input("\nPressione ENTER para continuar...")


def listar_usuarios():
    if not dados.usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for u in dados.usuarios:
        print("-" * 30)
        print(f"Usuário: {u['usuario']}")
        print(f"Role: {u['role']}")
        print(f"Status: {'ATIVO' if u.get('ativo', True) else 'INATIVO'}")


def criar_usuario():
    usuario = input("Novo usuário: ").strip()
    senha = input("Senha: ").strip()
    role = input(
        "Role (ADMIN / GERENTE / CONTADOR / OPERADOR): "
    ).strip().upper()

    roles_validos = (
        con.ROLE_ADMIN,
        con.ROLE_GERENTE,
        con.ROLE_CONTADOR,
        con.ROLE_OPERADOR
    )

    if role not in roles_validos:
        print("❌ Role inválida.")
        return

    if any(u["usuario"].lower() == usuario.lower() for u in dados.usuarios):
        print("❌ Usuário já existe.")
        return

    dados.usuarios.append({
        "usuario": usuario,
        "senha": senha,
        "role": role,
        "ativo": True
    })

    salvar_usuarios()
    print("✔ Usuário criado com sucesso!")


def alterar_status_usuario():
    usuario_nome = input("Usuário: ").strip()

    if (
        dados.usuario_logado
        and dados.usuario_logado["usuario"].lower() == usuario_nome.lower()
    ):
        print("❌ Você não pode desativar o próprio usuário.")
        return

    for u in dados.usuarios:
        if u["usuario"].lower() == usuario_nome.lower():
            u["ativo"] = not u.get("ativo", True)
            salvar_usuarios()
            print("✔ Status alterado com sucesso.")
            return

    print("❌ Usuário não encontrado.")


# =========================
# Edição completa
# =========================

def editar_usuario():
    usuario_nome = input("Usuário a editar: ").strip()

    for u in dados.usuarios:
        if u["usuario"].lower() == usuario_nome.lower():

            opcoes = [
                ("1", "Alterar nome de usuário", lambda: _editar_nome_usuario(u)),
                ("2", "Alterar senha", lambda: _editar_senha_usuario(u)),
                ("3", "Alterar role", lambda: _editar_role_usuario(u)),
            ]

            while True:
                limpa_tela()
                print(f"=== EDITAR USUÁRIO: {u['usuario']} ===")

                for k, label, _ in opcoes:
                    print(f"{k} - {label}")

                print("0 - Voltar")

                escolha = input("Escolha: ").strip()

                if escolha == "0":
                    salvar_usuarios()
                    print("\n✔ Alterações salvas com sucesso.")
                    return

                opcao = next((o for o in opcoes if o[0] == escolha), None)

                if not opcao:
                    print("\n❌ Opção inválida.")
                    input("Pressione ENTER para continuar...")
                    continue

                limpa_tela()
                opcao[2]()

    print("\n❌ Usuário não encontrado.")
    input("Pressione ENTER para continuar...")


# =========================
# Auxiliares
# =========================

def _editar_nome_usuario(u):
    novo_nome = input("Novo nome de usuário: ").strip()

    if not novo_nome:
        print("\n❌ Nome inválido.")
    elif any(x["usuario"].lower() == novo_nome.lower() for x in dados.usuarios):
        print("\n❌ Já existe um usuário com esse nome.")
    else:
        u["usuario"] = novo_nome
        print("\n✔ Nome de usuário atualizado com sucesso.")

    input("\nPressione ENTER para continuar...")


def _editar_senha_usuario(u):
    nova_senha = input("Nova senha: ").strip()

    if not nova_senha:
        print("\n❌ Senha inválida.")
    else:
        u["senha"] = nova_senha
        print("\n✔ Senha atualizada com sucesso.")

    input("\nPressione ENTER para continuar...")


def _editar_role_usuario(u):
    nova_role = input(
        "Nova role (ADMIN / GERENTE / CONTADOR / OPERADOR): "
    ).strip().upper()

    roles_validos = (
        con.ROLE_ADMIN,
        con.ROLE_GERENTE,
        con.ROLE_CONTADOR,
        con.ROLE_OPERADOR
    )

    if nova_role not in roles_validos:
        print("\n❌ Role inválida.")
    else:
        u["role"] = nova_role
        print("\n✔ Role atualizada com sucesso.")

    input("\nPressione ENTER para continuar...")