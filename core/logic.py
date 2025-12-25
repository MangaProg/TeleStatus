from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from core.models import Lojista, Produto, Registo


# ---------------------------------------------------------
# 1. Parsing e validação
# ---------------------------------------------------------
def validar_mensagem(texto: str):
    """
    Valida o formato da mensagem enviada pelo lojista.
    Exemplo válido: 'TV 3'
    Retorna (produto, quantidade) ou None se inválido.
    """
    try:
        partes = texto.strip().split()
        if len(partes) != 2:
            return None

        produto_nome = partes[0].upper()
        quantidade = int(partes[1])

        if quantidade <= 0:
            return None

        return produto_nome, quantidade

    except:
        return None


def parse_linhas(texto: str):
    """Divide o texto em linhas, ignorando linhas vazias."""
    return [linha.strip() for linha in texto.split("\n") if linha.strip()]


def interpretar_linha(linha: str):
    """Wrapper simples para manter consistência."""
    return validar_mensagem(linha)


# ---------------------------------------------------------
# 2. Acesso à base de dados
# ---------------------------------------------------------
def obter_lojista(db: Session, telegram_id: str):
    return db.query(Lojista).filter(Lojista.telegram_id == telegram_id).first()


def obter_produto(db: Session, nome_produto: str):
    return db.query(Produto).filter(Produto.nome == nome_produto).first()


def criar_registo(db: Session, lojista: Lojista, produto: Produto, quantidade: int):
    pontos_totais = produto.pontos * quantidade

    registo = Registo(
        lojista_id=lojista.id,
        loja_id=lojista.loja_id,
        produto_id=produto.id,
        quantidade=quantidade,
        pontos_totais=pontos_totais
    )

    db.add(registo)
    db.commit()
    db.refresh(registo)

    return registo


# ---------------------------------------------------------
# 3. Cálculo de pontos
# ---------------------------------------------------------
def obter_pontos_do_dia(db: Session, lojista: Lojista):
    """Devolve um dicionário com totais por família para o dia atual."""
    hoje = datetime.now().date()

    registos_dia = (
        db.query(Registo)
        .join(Produto)
        .join(Produto.familia)
        .filter(Registo.lojista_id == lojista.id)
        .filter(func.date(Registo.data) == hoje)
        .all()
    )

    totais = {}

    for r in registos_dia:
        familia = r.produto.familia
        nome = familia.nome
        emoji = familia.emoji or "📦"

        if nome not in totais:
            totais[nome] = {"emoji": emoji, "pontos": 0}

        totais[nome]["pontos"] += r.pontos_totais

    return totais


# ---------------------------------------------------------
# 4. Comando /meuspontos
# ---------------------------------------------------------
def comando_meus_pontos(db: Session, telegram_id: str):
    lojista = obter_lojista(db, telegram_id)
    if not lojista:
        return "❌ Não estás registado no sistema."

    totais_por_familia = obter_pontos_do_dia(db, lojista)

    resposta = ["📅 Pontos do dia por família:\n"]

    if not totais_por_familia:
        resposta.append("Ainda não tens pontos registados hoje.")
        return "\n".join(resposta)

    max_len = max(len(nome) for nome in totais_por_familia.keys())
    total_geral = 0

    for nome, dados in totais_por_familia.items():
        nome_fmt = nome.ljust(max_len)
        resposta.append(f"{dados['emoji']} {nome_fmt} → {dados['pontos']} pontos")
        total_geral += dados["pontos"]

    resposta.append(f"\n🏁 Total do dia: {total_geral} pontos")

    return "\n".join(resposta)


# ---------------------------------------------------------
# 5. Função principal: processar mensagem normal
# ---------------------------------------------------------
def processar_mensagem(db: Session, telegram_id: str, texto: str):
    lojista = obter_lojista(db, telegram_id)
    if not lojista:
        return "❌ Não estás registado no sistema. Contacta o administrador."

    linhas = parse_linhas(texto)
    respostas = []
    total_msg = 0

    # Processar cada linha
    for linha in linhas:
        interpretado = interpretar_linha(linha)

        if not interpretado:
            respostas.append(f"❌ Linha inválida: {linha}")
            continue

        nome_produto, quantidade = interpretado
        produto = obter_produto(db, nome_produto)

        if not produto:
            respostas.append(f"❌ Produto não encontrado: {nome_produto}")
            continue

        registo = criar_registo(db, lojista, produto, quantidade)
        emoji = produto.familia.emoji or "📦"

        respostas.append(
            f"{emoji} {produto.nome} — {quantidade} unidades → ⭐ {registo.pontos_totais} pontos"
        )

        total_msg += registo.pontos_totais

    # Totais do dia
    totais_por_familia = obter_pontos_do_dia(db, lojista)

    respostas.append(f"\n🏁 Total desta mensagem: {total_msg} pontos")
    respostas.append("\n📅 Total do dia por família:\n")

    if not totais_por_familia:
        respostas.append("Ainda não tens pontos registados hoje.")
    else:
        max_len = max(len(nome) for nome in totais_por_familia.keys())

        for nome, dados in totais_por_familia.items():
            nome_fmt = nome.ljust(max_len)
            respostas.append(f"{dados['emoji']} {nome_fmt} → {dados['pontos']} pontos")

    return "\n".join(respostas)