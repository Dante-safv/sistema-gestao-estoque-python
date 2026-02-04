import dados as ds
import constantes as con
import persistencia as per

from historico import registrar_movimentacao
from utils import (
    limpa_tela,
    get_usuario_logado,
    _input_campo
)


# =========================
# Utilidades de UX
# =========================

def _normalizar_codigo(valor: str) -> str:
    return valor.strip().upper()


def _exibir_resumo_produto(p: dict):
    print("\n" + "─" * 40)
    print(f"📦 PRODUTO: {p['nome']}")
    print(f"🔢 Código: {p['codigo']}")
    print(f"📊 Estoque Atual: {p['quantidade']}")
    print(f"📉 Estoque Mínimo: {p['estoque_minimo']}")
    print(f"💰 Custo: R$ {p['custo_unitario']:.2f}")
    print(f"💵 Preço Venda: R$ {p['preco_venda']:.2f}")
    print(f"🔘 Status: {'✅ ATIVO' if p['ativo'] else '🚫 INATIVO'}")
    print("─" * 40 + "\n")


# =========================
# Validações
# =========================

def codigo_existente(codigo: str):
    codigo = _normalizar_codigo(codigo)
    for produto in ds.produtos:
        if produto["codigo"] == codigo:
            return produto
    return None


def fornecedor_existente(fornecedor_id: str):
    fornecedor_id = _normalizar_codigo(fornecedor_id)
    for f in ds.fornecedores:
        if f["id"] == fornecedor_id and f["ativo"]:
            return f
    return None


def _listar_fornecedores_ativos_resumido() -> bool:
    print("\nFornecedores disponíveis:")
    print("-" * 35)

    ativos = [f for f in ds.fornecedores if f["ativo"]]

    if not ativos:
        print("⚠️ Nenhum fornecedor ativo cadastrado.")
        return False

    for f in ativos:
        print(f"{f['id']} - {f['nome']}")

    print("-" * 35)
    return True


# =========================
# 1. Cadastro de Produto
# =========================

def cadastrar_produto():
    limpa_tela()
    print("=== Cadastro de Produto ===")
    print("Digite 0 a qualquer momento para cancelar.\n")

    while True:
        codigo = _input_campo("Código do produto: ")
        if codigo is None:
            return
        codigo = _normalizar_codigo(codigo)

        if codigo_existente(codigo):
            print("❌ Código já cadastrado.")
            continue

        nome = _input_campo("Nome do produto: ")
        if nome is None:
            return

        quantidade = _input_campo("Quantidade inicial: ", int, permitir_zero=False)
        if quantidade in (None, "ERRO"):
            if quantidade is None:
                return
            continue

        estoque_minimo = _input_campo("Estoque mínimo: ", int, permitir_zero=False)
        if estoque_minimo in (None, "ERRO"):
            if estoque_minimo is None:
                return
            continue

        custo_unitario = _input_campo("Custo unitário: ", float, permitir_zero=False)
        if custo_unitario in (None, "ERRO"):
            if custo_unitario is None:
                return
            continue

        preco_venda = _input_campo("Preço de venda: ", float, permitir_zero=False)
        if preco_venda in (None, "ERRO"):
            if preco_venda is None:
                return
            continue

        if not _listar_fornecedores_ativos_resumido():
            return

        fornecedor_id = _input_campo("ID do fornecedor: ")
        if fornecedor_id is None:
            return
        fornecedor_id = _normalizar_codigo(fornecedor_id)

        if not fornecedor_existente(fornecedor_id):
            print("❌ Fornecedor inválido ou inativo.")
            continue

        break

    produto = {
        "codigo": codigo,
        "nome": nome,
        "quantidade": quantidade,
        "estoque_minimo": estoque_minimo,
        "custo_unitario": custo_unitario,
        "preco_venda": preco_venda,
        "fornecedor_id": fornecedor_id,
        "ativo": True
    }

    ds.produtos.append(produto)

    registrar_movimentacao(
        tipo=con.TIPO_CADASTRO,
        produto_nome=nome,
        codigo=codigo,
        quantidade=quantidade,
        custo_unitario=custo_unitario,
        preco_venda_unitario=preco_venda
    )

    per.salvar_dados()
    print("\n✅ Produto cadastrado com sucesso!")


# =========================
# 2. Editar Produto
# =========================

def editar_produto():
    limpa_tela()

    if not ds.produtos:
        print("⚠️ Nenhum produto cadastrado.")
        return

    codigo = _normalizar_codigo(input("Código do produto: "))
    produto = codigo_existente(codigo)

    if not produto:
        print("❌ Produto não encontrado.")
        return

    _exibir_resumo_produto(produto)

    def alternar_status():
        produto["ativo"] = not produto["ativo"]
        print(f"✔ Status alterado para {'ATIVO' if produto['ativo'] else 'INATIVO'}.")

    acoes = {
        "1": lambda: produto.update({"nome": input("Novo nome: ").strip()}),
        "2": lambda: produto.update({"quantidade": int(input("Nova quantidade: "))}),
        "3": lambda: produto.update({"estoque_minimo": int(input("Novo estoque mínimo: "))}),
        "4": lambda: produto.update({"custo_unitario": float(input("Novo custo unitário: "))}),
        "5": lambda: produto.update({"preco_venda": float(input("Novo preço de venda: "))}),
        "6": alternar_status
    }

    while True:
        print(f"\n=== Editando: {produto['nome']} ===")
        print("1 - Nome")
        print("2 - Quantidade")
        print("3 - Estoque mínimo")
        print("4 - Custo unitário")
        print("5 - Preço de venda")
        print("6 - Ativar / Inativar")
        print("0 - Finalizar edição")

        op = input("Escolha: ").strip()

        if op == "0":
            per.salvar_dados()
            print("\n✅ Alterações salvas.")
            return

        acao = acoes.get(op)
        if acao:
            try:
                acao()
                print("✅ Alteração aplicada!")
            except ValueError:
                print("❌ Valor inválido.")
        else:
            print("❌ Opção inválida.")


# =========================
# 3. Listar Produtos
# =========================

def listar_produtos():
    limpa_tela()
    usuario = get_usuario_logado()
    print("=== Lista Geral de Produtos ===\n")

    if not ds.produtos:
        print("⚠️ Nenhum produto cadastrado.")
        return

    exibiu = False

    for p in ds.produtos:
        if usuario["role"] != con.ROLE_ADMIN and not p["ativo"]:
            continue

        exibiu = True
        fornecedor = fornecedor_existente(p["fornecedor_id"])
        nome_fornecedor = fornecedor["nome"] if fornecedor else "N/A"

        print("-" * 35)
        print(f"Código: {p['codigo']}")
        print(f"Nome: {p['nome']}")
        print(f"Fornecedor: {nome_fornecedor}")
        print(f"Quantidade: {p['quantidade']}")
        print(f"Estoque mínimo: {p['estoque_minimo']}")
        print(f"Custo: R$ {p['custo_unitario']:.2f}")
        print(f"Preço: R$ {p['preco_venda']:.2f}")
        print(f"Status: {'ATIVO' if p['ativo'] else 'INATIVO'}")

    if not exibiu:
        print("⚠️ Nenhum produto disponível para exibição.")


# =========================
# 4. Entrada de Produto
# =========================

def entrada_produto():
    limpa_tela()

    if not ds.produtos:
        print("⚠️ Nenhum produto cadastrado.")
        return

    codigo = _normalizar_codigo(input("Código do produto: "))
    produto = codigo_existente(codigo)

    if not produto or not produto["ativo"]:
        print("❌ Produto inválido ou inativo.")
        return

    _exibir_resumo_produto(produto)

    try:
        qtd = int(input("Quantidade de ENTRADA: "))
        if qtd <= 0:
            raise ValueError
    except ValueError:
        print("❌ Quantidade inválida.")
        return

    produto["quantidade"] += qtd

    registrar_movimentacao(
        tipo=con.TIPO_ENTRADA,
        produto_nome=produto["nome"],
        codigo=produto["codigo"],
        quantidade=qtd,
        custo_unitario=produto["custo_unitario"]
    )

    per.salvar_dados()
    print(f"\n✅ Entrada de {qtd} unidades registrada!")


# =========================
# 5. Saída de Produto
# =========================

def saida_produto():
    limpa_tela()

    if not ds.produtos:
        print("⚠️ Nenhum produto cadastrado.")
        return

    codigo = _normalizar_codigo(input("Código do produto: "))
    produto = codigo_existente(codigo)

    if not produto or not produto["ativo"]:
        print("❌ Produto inválido ou inativo.")
        return

    _exibir_resumo_produto(produto)

    try:
        qtd = int(input("Quantidade de SAÍDA: "))
        if qtd <= 0:
            raise ValueError
    except ValueError:
        print("❌ Quantidade inválida.")
        return

    if qtd > produto["quantidade"]:
        print("❌ Estoque insuficiente.")
        return

    usuario = get_usuario_logado()
    estoque_final = produto["quantidade"] - qtd

    # ⚠️ ALERTA DE ESTOQUE MÍNIMO
    if estoque_final < produto["estoque_minimo"]:
        if usuario["role"] != con.ROLE_ADMIN:
            print("⚠️ Apenas ADMIN pode autorizar saída abaixo do estoque mínimo.")
            return

        # ADMIN: aviso e confirmação
        print("\n⚠️ ATENÇÃO — ESTOQUE ABAIXO DO MÍNIMO ⚠️")
        print("-" * 40)
        print(f"Produto: {produto['nome']} ({produto['codigo']})")
        print(f"Estoque atual:   {produto['quantidade']}")
        print(f"Estoque mínimo: {produto['estoque_minimo']}")
        print(f"Estoque após saída: {estoque_final}")
        print("-" * 40)

        try:
            op = input("Deseja continuar mesmo assim? (S/N): ").strip().upper()
            if op != "S":
                print("⏪ Operação cancelada.")
                return
        except Exception:
            print("❌ Opção inválida.")
            return

    produto["quantidade"] = estoque_final

    registrar_movimentacao(
        tipo=con.TIPO_SAIDA,
        produto_nome=produto["nome"],
        codigo=produto["codigo"],
        quantidade=-qtd,
        custo_unitario=produto["custo_unitario"],
        preco_venda_unitario=produto["preco_venda"]
    )

    per.salvar_dados()
    print(f"\n✅ Saída de {qtd} unidades registrada com sucesso!")


# =========================
# 6. Histórico
# =========================

def historico_produto():
    limpa_tela()
    print("=== Histórico de Movimentações ===\n")

    if not ds.historico:
        print("⚠️ Nenhuma movimentação registrada.")
        return

    for h in reversed(ds.historico):
        print("-" * 30)
        print(f"{h['data']} | {h['tipo']}")
        print(f"{h['produto']} ({h['codigo']})")
        print(f"Usuário: {h['usuario']} ({h['role']})")
        print(f"Quantidade: {h['quantidade']}")