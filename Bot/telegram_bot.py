from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os
from dotenv import load_dotenv

from core.database import get_db
from core.logic import processar_mensagem, comando_meus_pontos
from core.models import Familia, Loja, Produto, Lojista

# ---------------------------------------------------------
# Carregar variáveis do ambiente
# ---------------------------------------------------------
load_dotenv()

ADMIN_IDS = [int(os.getenv("ADMIN_IDS"))]
TOKEN = os.getenv("bot_Token")


# ---------------------------------------------------------
# /start
# ---------------------------------------------------------
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Envia-me os teus registos com a formatação 'produto quantidade '(ex: TV 1) que eu trato do resto :)" \
        "\n\n" \
        "Usa /meuspontos para veres os teus pontos do dia." \
    )

# ---------------------------------------------------------
# /addfamilia
# ---------------------------------------------------------
async def cmd_addfamilia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Uso correto: /addfamilia <nome> <emoji>")
        return

    nome = context.args[0].upper()
    emoji = context.args[1]

    with get_db() as db:
        existente = db.query(Familia).filter(Familia.nome == nome).first()
        if existente:
            await update.message.reply_text(f"⚠️ A família '{nome}' já existe.")
            return

        nova = Familia(nome=nome, emoji=emoji)
        db.add(nova)
        db.commit()

    await update.message.reply_text(f"✅ Família '{nome}' criada com emoji {emoji}.")


# ---------------------------------------------------------
# /addproduto
# ---------------------------------------------------------
async def cmd_addproduto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    if len(context.args) < 3:
        await update.message.reply_text(
            "Uso correto: /addproduto <nome> <pontos> <familia>")
        return

    nome_produto = context.args[0].upper()
    pontos_raw = context.args[1]
    nome_familia = context.args[2].upper()

    try:
        pontos_valor = float(pontos_raw.replace(",", "."))
    except ValueError:
        await update.message.reply_text("❌ Os pontos devem ser um número válido.")
        return

    with get_db() as db:
        familia = db.query(Familia).filter(Familia.nome == nome_familia).first()
        if not familia:
            await update.message.reply_text(f"❌ A família '{nome_familia}' não existe.")
            return

        existente = db.query(Produto).filter(Produto.nome == nome_produto).first()
        if existente:
            await update.message.reply_text(f"⚠️ O produto '{nome_produto}' já existe.")
            return

        novo = Produto(
            nome=nome_produto,
            pontos=pontos_valor,
            familia_id=familia.id
        )

        db.add(novo)
        db.commit()

    await update.message.reply_text(
        f"✅ Produto '{nome_produto}' criado com {pontos_valor} pontos na família {nome_familia}."
    )


# ---------------------------------------------------------
# /addloja
# ---------------------------------------------------------
async def cmd_addloja(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("Uso correto: /addloja <nome_da_loja>")
        return

    nome_loja = " ".join(context.args).upper()

    with get_db() as db:
        existente = db.query(Loja).filter(Loja.nome == nome_loja).first()
        if existente:
            await update.message.reply_text(f"⚠️ A loja '{nome_loja}' já existe.")
            return

        nova = Loja(nome=nome_loja)
        db.add(nova)
        db.commit()

    await update.message.reply_text(f"✅ Loja '{nome_loja}' criada com sucesso.")


# ---------------------------------------------------------
# /addlojista
# ---------------------------------------------------------
async def cmd_addlojista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    if len(context.args) < 3:
        await update.message.reply_text(
            "Uso correto: /addlojista <nome> <telegram_id> <loja>")
        return

    nome = context.args[0].upper()
    telegram_id = context.args[1]
    nome_loja = context.args[2].upper()

    if not telegram_id.isdigit():
        await update.message.reply_text("❌ O telegram_id deve ser numérico.")
        return

    with get_db() as db:
        loja = db.query(Loja).filter(Loja.nome == nome_loja).first()
        if not loja:
            await update.message.reply_text(f"❌ A loja '{nome_loja}' não existe.")
            return

        existente = db.query(Lojista).filter(Lojista.telegram_id == telegram_id).first()
        if existente:
            await update.message.reply_text(f"⚠️ O lojista com ID {telegram_id} já existe.")
            return

        novo = Lojista(
            nome=nome,
            telegram_id=telegram_id,
            loja_id=loja.id
        )

        db.add(novo)
        db.commit()

    await update.message.reply_text(
        f"✅ Lojista '{nome}' adicionado à loja {nome_loja}."
    )


# ---------------------------------------------------------
# /emoji
# ---------------------------------------------------------
async def cmd_emoji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Uso correto: /emoji <familia> <emoji>")
        return

    nome_familia = context.args[0].upper()
    emoji = context.args[1]

    with get_db() as db:
        familia = db.query(Familia).filter(Familia.nome == nome_familia).first()
        if not familia:
            await update.message.reply_text(f"❌ Família '{nome_familia}' não encontrada.")
            return

        familia.emoji = emoji
        db.commit()

    await update.message.reply_text(
        f"Emoji da família {nome_familia} atualizado para {emoji} com sucesso!"
    )


# ---------------------------------------------------------
# /meuspontos
# ---------------------------------------------------------
async def cmd_meus_pontos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)

    with get_db() as db:
        resposta = comando_meus_pontos(db, telegram_id)

    await update.message.reply_text(resposta)


# ---------------------------------------------------------
# /meuid
# ---------------------------------------------------------
async def cmd_meuid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    await update.message.reply_text(f"O teu Telegram ID é: {telegram_id}")

# -----------------------------
# /editlojas
# -----------------------------
async def cmd_editlojas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Uso correto: /editlojas <nome_atual> <novo_nome>"
        )
        return

    nome_atual = context.args[0].upper()
    novo_nome = " ".join(context.args[1:]).upper()

    with get_db() as db:
        loja = db.query(Loja).filter(Loja.nome == nome_atual).first()

        if not loja:
            await update.message.reply_text(f"❌ Loja '{nome_atual}' não encontrada.")
            return

        loja.nome = novo_nome
        db.commit()

    await update.message.reply_text(
        f"✅ Loja atualizada:\nDe: {nome_atual}\nPara: {novo_nome}"
    )


# -----------------------------
# /editfamilias
# -----------------------------
async def cmd_editfamilias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Uso correto:\n"
            "/editfamilias <nome_atual> <novo_nome> [novo_emoji]\n"
            "/editfamilias <nome_atual> <novo_emoji>"
        )
        return

    nome_atual = context.args[0].upper()
    novo_nome = None
    novo_emoji = None

    if len(context.args) == 2:
        if len(context.args[1]) <= 3:
            novo_emoji = context.args[1]
        else:
            novo_nome = context.args[1].upper()

    if len(context.args) == 3:
        novo_nome = context.args[1].upper()
        novo_emoji = context.args[2]

    with get_db() as db:
        familia = db.query(Familia).filter(Familia.nome == nome_atual).first()

        if not familia:
            await update.message.reply_text(f"❌ Família '{nome_atual}' não encontrada.")
            return

        if novo_nome:
            familia.nome = novo_nome

        if novo_emoji:
            familia.emoji = novo_emoji

        db.commit()

    await update.message.reply_text(
        f"✅ Família atualizada!\n"
        f"Nome: {familia.nome}\nEmoji: {familia.emoji}"
    )

# -----------------------------
# /editlojista
# -----------------------------
async def cmd_editlojista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    if len(context.args) < 3:
        await update.message.reply_text(
            "Uso correto:\n"
            "/editlojista <telegram_id> nome <novo_nome>\n"
            "/editlojista <telegram_id> loja <nova_loja>\n"
            "/editlojista <telegram_id> id <novo_telegram_id>"
        )
        return

    telegram_id = context.args[0]
    campo = context.args[1].lower()
    valor = " ".join(context.args[2:]).upper()

    with get_db() as db:
        lojista = db.query(Lojista).filter(Lojista.telegram_id == telegram_id).first()

        if not lojista:
            await update.message.reply_text(f"❌ Lojista '{telegram_id}' não encontrado.")
            return

        if campo == "nome":
            lojista.nome = valor

        elif campo == "loja":
            loja = db.query(Loja).filter(Loja.nome == valor).first()
            if not loja:
                await update.message.reply_text(f"❌ Loja '{valor}' não existe.")
                return
            lojista.loja_id = loja.id

        elif campo == "id":
            if not valor.isdigit():
                await update.message.reply_text("❌ O novo telegram_id deve ser numérico.")
                return
            lojista.telegram_id = valor

        else:
            await update.message.reply_text("❌ Campo inválido. Usa: nome, loja ou id.")
            return

        db.commit()

    await update.message.reply_text("✅ Lojista atualizado com sucesso!")

# -----------------------------
# /editproduto
# -----------------------------
async def cmd_editproduto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    if len(context.args) < 3:
        await update.message.reply_text(
            "Uso correto:\n"
            "/editproduto <produto> nome <novo_nome>\n"
            "/editproduto <produto> pontos <novo_valor>\n"
            "/editproduto <produto> familia <nova_familia>"
        )
        return

    nome_produto = context.args[0].upper()
    campo = context.args[1].lower()
    valor = " ".join(context.args[2:]).upper()

    with get_db() as db:
        produto = db.query(Produto).filter(Produto.nome == nome_produto).first()

        if not produto:
            await update.message.reply_text(f"❌ Produto '{nome_produto}' não encontrado.")
            return

        if campo == "nome":
            produto.nome = valor

        elif campo == "pontos":
            try:
                produto.pontos = float(valor.replace(",", "."))
            except:
                await update.message.reply_text("❌ Valor de pontos inválido.")
                return

        elif campo == "familia":
            familia = db.query(Familia).filter(Familia.nome == valor).first()
            if not familia:
                await update.message.reply_text(f"❌ Família '{valor}' não existe.")
                return
            produto.familia_id = familia.id

        else:
            await update.message.reply_text("❌ Campo inválido. Usa: nome, pontos ou familia.")
            return

        db.commit()

    await update.message.reply_text("✅ Produto atualizado com sucesso!")

# ---------------------------------------------------------
# Comando desconhecido
# ---------------------------------------------------------
async def cmd_desconhecido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Comando inválido.\nUsa /start para veres como funciona."
    )


# ---------------------------------------------------------
# Handler principal (mensagens normais)
# ---------------------------------------------------------
async def tratar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    telegram_id = str(update.effective_user.id)

    with get_db() as db:
        resposta = processar_mensagem(db, telegram_id, texto)

    await update.message.reply_text(resposta)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("addfamilia", cmd_addfamilia))
    app.add_handler(CommandHandler("addproduto", cmd_addproduto))
    app.add_handler(CommandHandler("addloja", cmd_addloja))
    app.add_handler(CommandHandler("addlojista", cmd_addlojista))
    app.add_handler(CommandHandler("editlojas", cmd_editlojas))
    app.add_handler(CommandHandler("editfamilias", cmd_editfamilias))
    app.add_handler(CommandHandler("editlojista", cmd_editlojista))
    app.add_handler(CommandHandler("editproduto", cmd_editproduto))
    app.add_handler(CommandHandler("emoji", cmd_emoji))
    app.add_handler(CommandHandler("meuspontos", cmd_meus_pontos))
    app.add_handler(CommandHandler("meuid", cmd_meuid))

    # Mensagens normais
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))

    # Comandos inválidos
    app.add_handler(MessageHandler(filters.COMMAND, cmd_desconhecido))

    app.run_polling()


if __name__ == "__main__":
    main()