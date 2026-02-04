from datetime import datetime

import dados as ds
from utils import get_usuario_logado


def registrar_movimentacao(
    tipo,
    produto_nome,
    codigo,
    quantidade,
    custo_unitario=0,
    preco_venda_unitario=0
):
    usuario = get_usuario_logado()

    custo_total = quantidade * custo_unitario if custo_unitario else 0
    receita_total = abs(quantidade) * preco_venda_unitario if preco_venda_unitario else 0

    ds.historico.append({
        "usuario": usuario["usuario"],
        "role": usuario["role"],
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo": tipo,
        "produto": produto_nome,
        "codigo": codigo,
        "quantidade": quantidade,
        "custo_unitario": custo_unitario,
        "custo_total": custo_total,
        "preco_venda_unitario": preco_venda_unitario,
        "receita_total": receita_total
    })