import json
import os
import dados


# =========================
# Utilitários internos
# =========================

def _salvar_json(caminho, dados_obj):
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados_obj, f, indent=4, ensure_ascii=False)
    except OSError as e:
        print(f"❌ Erro ao salvar {caminho}: {e}")


def _carregar_json(caminho, valor_padrao):
    if not os.path.exists(caminho):
        return valor_padrao

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            return json.loads(conteudo) if conteudo else valor_padrao

    except json.JSONDecodeError:
        print(f"⚠️ Arquivo {caminho} corrompido. Inicializando vazio.")
        return valor_padrao

    except OSError as e:
        print(f"❌ Erro ao ler {caminho}: {e}")
        return valor_padrao


# =========================
# Produtos e Histórico
# =========================

def salvar_dados():
    _salvar_json("produtos.json", dados.produtos)
    _salvar_json("historico.json", dados.historico)


def carregar_dados():
    dados.produtos = _carregar_json("produtos.json", [])
    dados.historico = _carregar_json("historico.json", [])


# =========================
# Fornecedores
# =========================

def salvar_fornecedores():
    _salvar_json("fornecedores.json", dados.fornecedores)


def carregar_fornecedores():
    dados.fornecedores = _carregar_json("fornecedores.json", [])


# =========================
# Usuários
# =========================

def salvar_usuarios():
    _salvar_json("usuarios.json", dados.usuarios)


def carregar_usuarios():
    dados.usuarios = _carregar_json("usuarios.json", [])