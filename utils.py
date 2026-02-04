import os
import re
import dados as ds

def limpa_tela():
    os.system("cls" if os.name == "nt" else "clear")


def get_usuario_logado():
    if not ds.usuario_logado:
        return {"usuario": "DESCONHECIDO", "role": "DESCONHECIDO"}
    return ds.usuario_logado

def verificar_alerta_estoque():
    alertas = []

    for p in ds.produtos:
        # ignora produtos inativos
        if not p.get("ativo", True):
            continue

        quantidade = p.get("quantidade", 0)
        minimo = p.get("estoque_minimo", 0)

        if quantidade <= minimo:
            alertas.append({
                "produto": p,
                "status": "CRÍTICO" if quantidade < minimo else "NO LIMITE"
            })

    if not alertas:
        return False

    print("⚠️ ALERTA DE ESTOQUE ⚠️\n")

    for item in alertas:
        p = item["produto"]
        status = item["status"]

        print("-" * 40)
        print(f"Produto: {p['nome']} ({p['codigo']})")
        print(f"Estoque atual: {p['quantidade']}")
        print(f"Estoque mínimo: {p['estoque_minimo']}")
        print(f"Status: {status}")

    print("-" * 40)
    return True

def validar_cnpj(cnpj: str) -> bool:
    if not cnpj:
        return False
        
    cnpj = re.sub(r"\D", "", cnpj)

    if len(cnpj) != 14:
        return False

    # rejeita sequências inválidas
    if cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj_parcial, pesos):
        soma = sum(int(d) * p for d, p in zip(cnpj_parcial, pesos))
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_2 = [6] + pesos_1

    digito_1 = calcular_digito(cnpj[:12], pesos_1)
    digito_2 = calcular_digito(cnpj[:12] + digito_1, pesos_2)

    return cnpj[-2:] == digito_1 + digito_2
    
def _input_campo(label, tipo=str, permitir_zero=True):
    valor = input(label).strip()

    if valor == "0":
        print("\n⏪ Cadastro cancelado.")
        return None

    try:
        convertido = tipo(valor)
        if not permitir_zero and convertido < 0:
            raise ValueError
        return convertido
    except ValueError:
        print("❌ Valor inválido.")
        return "ERRO"