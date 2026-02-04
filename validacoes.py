from constantes import CAMPOS_PRODUTO


campos_obrigatorios = CAMPOS_PRODUTO

campos_int = ["quantidade", "estoque_minimo"]
campos_float = ["custo_unitario", "preco_venda"]


def validar_colunas_csv(colunas_recebidas, colunas_esperadas):
    recebidas = set(colunas_recebidas)
    esperadas = set(colunas_esperadas)

    erros = []

    if recebidas != esperadas:
        faltando = esperadas - recebidas
        extras = recebidas - esperadas

        if faltando:
            erros.append(f"Colunas faltando: {', '.join(faltando)}")
        if extras:
            erros.append(f"Colunas extras: {', '.join(extras)}")

    return erros


def validar_linha(linha, indice):
    erros = []

    # Campos obrigatórios
    for campo in campos_obrigatorios:
        if campo not in linha:
            erros.append(f"Linha {indice}: campo obrigatório '{campo}' não encontrado.")
            continue

        if str(linha[campo]).strip() == "":
            erros.append(f"Linha {indice}: campo obrigatório '{campo}' está vazio.")

    # Campos inteiros
    for campo in campos_int:
        try:
            valor = int(linha[campo])
            if valor < 0:
                erros.append(f"Linha {indice}: campo '{campo}' não pode ser negativo.")
        except (ValueError, TypeError):
            erros.append(f"Linha {indice}: campo '{campo}' deve ser um número inteiro.")

    # Campos float
    for campo in campos_float:
        try:
            valor = float(linha[campo])
            if valor < 0:
                erros.append(f"Linha {indice}: campo '{campo}' não pode ser negativo.")
        except (ValueError, TypeError):
            erros.append(f"Linha {indice}: campo '{campo}' deve ser numérico.")

    # Campo ativo
    ativo = str(linha.get("ativo", "")).lower()
    if ativo not in ("true", "false", "1", "0", "sim", "nao", "não"):
        erros.append(
            f"Linha {indice}: campo 'ativo' inválido (use true/false)."
        )

    return erros


def validar_duplicados(linhas_validas):
    erros = []
    codigos = set()

    for indice, linha in linhas_validas:
        codigo = linha.get("codigo")

        if codigo in codigos:
            erros.append(f"Linha {indice}: código duplicado '{codigo}'.")
        else:
            codigos.add(codigo)

    return erros


def validar_csv_produtos(reader):
    erros = []

    # 1. Validar colunas
    erros_colunas = validar_colunas_csv(reader.fieldnames, CAMPOS_PRODUTO)
    if erros_colunas:
        return [], erros_colunas

    linhas_validas = []
    erros_linhas = []

    # 2. Validar linha por linha
    for indice, linha in enumerate(reader, start=1):
        erros_linha = validar_linha(linha, indice)

        if erros_linha:
            erros_linhas.extend(erros_linha)
        else:
            linhas_validas.append((indice, linha))

    # 3. Validar duplicados
    erros_duplicados = validar_duplicados(linhas_validas)

    erros.extend(erros_linhas)
    erros.extend(erros_duplicados)

    produtos_validos = [linha for _, linha in linhas_validas]

    return produtos_validos, erros