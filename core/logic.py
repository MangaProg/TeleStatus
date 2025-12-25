from sqlalchemy.orm import Session
from core.models import Lojista, Produto, Registo


# ---------------------------------------------------------
# 1. Validar formato da mensagem
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


# ---------------------------------------------------------
# 2. Obter lojista pelo telegram_id
# ---------------------------------------------------------
def obter_lojista(db: Session, telegram_id: str):
    return db.query(Lojista).filter(Lojista.telegram_id == telegram_id).first()


# ---------------------------------------------------------
# 3. Obter produto pelo nome
# ---------------------------------------------------------
def obter_produto(db: Session, nome_produto: str):
    return db.query(Produto).filter(Produto.nome == nome_produto).first()


# ---------------------------------------------------------
# 4. Criar registo na base de dados
# ---------------------------------------------------------
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
# 5. Função principal que processa uma mensagem
# ---------------------------------------------------------

def processar_mensagem(db: Session, telegram_id: str, texto: str):
    lojista = obter_lojista(db, telegram_id)
    if not lojista:
        return "❌ Não estás registado no sistema. Contacta o administrador."

    linhas = parse_linhas(texto)

    respostas = []
    total_pontos = 0

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

        total_pontos += registo.pontos_totais

    respostas.append(f"\n🏁 Total acumulado: {total_pontos} pontos")

    return "\n".join(respostas)