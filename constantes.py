# =========================
# Tipos de movimentação
# =========================

TIPO_CADASTRO = "CADASTRO"
TIPO_ENTRADA = "ENTRADA"
TIPO_SAIDA = "SAÍDA"
TIPO_AJUSTE_QUANTIDADE = "AJUSTE_QUANTIDADE"
TIPO_ALTERACAO_ESTOQUE_MINIMO = "ALTERACAO_ESTOQUE_MINIMO"
TIPO_IMPORTACAO = "IMPORTADO"


# =========================
# Perfis de usuário (roles)
# =========================

ROLE_ADMIN = "ADMIN"
ROLE_OPERADOR = "OPERADOR"
ROLE_CONTADOR = "CONTADOR"
ROLE_GERENTE = "GERENTE"


# =========================
# Estrutura de produto (CSV / JSON)
# =========================

CAMPOS_PRODUTO = [
    "codigo",
    "nome",
    "quantidade",
    "estoque_minimo",
    "custo_unitario",
    "preco_venda",
    "fornecedor_id",
    "ativo"
]