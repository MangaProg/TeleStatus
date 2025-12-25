from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from core.database import SessionLocal
from core.logic import processar_mensagem
from core.models import Familia

import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Lista de administradores
ADMIN_IDS = [int(os.getenv("ADMIN_IDS"))]  # substitui pelo teu telegram_id

# Token do bot vindo do .env
TOKEN = os.getenv("bot_Token")


# -----------------------------
# Comando /start
# -----------------------------
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Envia-me os teus registos (ex.: 'tv premium 3') que eu trato do resto."
    )

# -----------------------------
# Comando /addfamilia
# -----------------------------
async def cmd_addfamilia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Verifica se é admin
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    # Verifica se tem argumentos suficientes
    if len(context.args) < 2:
        await update.message.reply_text("Uso correto: /addfamilia <nome> <emoji>")
        return

    nome = context.args[0].upper()
    emoji = context.args[1]

    db = SessionLocal()

    # Verificar se já existe família com esse nome
    existente = db.query(Familia).filter(Familia.nome == nome).first()
    if existente:
        await update.message.reply_text(f"⚠️ A família '{nome}' já existe.")
        db.close()
        return

    # Criar nova família
    nova = Familia(nome=nome, emoji=emoji)
    db.add(nova)
    db.commit()
    db.close()

    await update.message.reply_text(f"✅ Família '{nome}' criada com emoji {emoji}.")

# -----------------------------
# Comando /addproduto
# -----------------------------
async def cmd_addproduto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Verifica se é admin
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    # Verifica argumentos
    if len(context.args) < 3:
        await update.message.reply_text(
            "Uso correto: /addproduto \"<nome>\" <pontos> <familia>\n"
            "Exemplo: /addproduto \"TV PREMIUM\" 10 TV"
        )
        return

    # Extrair argumentos
    nome_produto = context.args[0].upper()
    pontos = context.args[1]
    nome_familia = context.args[2].upper()

    # Validar número decimal
    try:
        pontos_valor = float(pontos.replace(",", "."))
    except ValueError:
        await update.message.reply_text("❌ Os pontos devem ser um número (ex.: 10, 7.5, 2.25).")
        return

    db = SessionLocal()

    # Verificar se a família existe
    familia = db.query(Familia).filter(Familia.nome == nome_familia).first()
    if not familia:
        await update.message.reply_text(f"❌ A família '{nome_familia}' não existe.")
        db.close()
        return

    from core.models import Produto

    existente = db.query(Produto).filter(Produto.nome == nome_produto).first()
    if existente:
        await update.message.reply_text(f"⚠️ O produto '{nome_produto}' já existe.")
        db.close()
        return

    novo = Produto(
        nome=nome_produto,
        pontos=pontos_valor,
        familia_id=familia.id
    )

    db.add(novo)
    db.commit()
    db.close()

    await update.message.reply_text(
        f"✅ Produto '{nome_produto}' criado com {pontos_valor} pontos na família {nome_familia}."
    )

# -----------------------------
# Comando /addloja
# -----------------------------
async def cmd_addloja(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Verifica se é admin
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    # Verifica argumentos
    if len(context.args) < 1:
        await update.message.reply_text("Uso correto: /addloja <nome_da_loja>")
        return

    nome_loja = " ".join(context.args).upper()

    db = SessionLocal()

    from core.models import Loja  # import local para evitar ciclos

    # Verificar se já existe
    existente = db.query(Loja).filter(Loja.nome == nome_loja).first()
    if existente:
        await update.message.reply_text(f"⚠️ A loja '{nome_loja}' já existe.")
        db.close()
        return

    nova = Loja(nome=nome_loja)
    db.add(nova)
    db.commit()
    db.close()

    await update.message.reply_text(f"✅ Loja '{nome_loja}' criada com sucesso.")

# -----------------------------
# Comando /addlojista
# -----------------------------
async def cmd_addlojista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Verifica se é admin
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Não tens permissão para usar este comando.")
        return

    # Verifica argumentos
    if len(context.args) < 3:
        await update.message.reply_text(
            "Uso correto: /addlojista <nome> <telegram_id> <loja>\n"
            "Exemplo: /addlojista Miguel 123456789 Almada"
        )
        return

    nome = context.args[0].upper()
    telegram_id = context.args[1]
    nome_loja = context.args[2].upper()

    # Validar telegram_id
    if not telegram_id.isdigit():
        await update.message.reply_text("❌ O telegram_id deve ser numérico.")
        return

    db = SessionLocal()

    from core.models import Loja, Lojista  # import local para evitar ciclos

    # Verificar se a loja existe
    loja = db.query(Loja).filter(Loja.nome == nome_loja).first()
    if not loja:
        await update.message.reply_text(f"❌ A loja '{nome_loja}' não existe.")
        db.close()
        return

    # Verificar se o lojista já existe
    existente = db.query(Lojista).filter(Lojista.telegram_id == telegram_id).first()
    if existente:
        await update.message.reply_text(f"⚠️ O lojista com ID {telegram_id} já existe.")
        db.close()
        return

    # Criar lojista
    novo = Lojista(
        nome=nome,
        telegram_id=telegram_id,
        loja_id=loja.id
    )

    db.add(novo)
    db.commit()
    db.close()

    await update.message.reply_text(
        f"✅ Lojista '{nome}' adicionado à loja {nome_loja}."
    )    

# -----------------------------
# Comando /emoji
# -----------------------------
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

    db = SessionLocal()
    familia = db.query(Familia).filter(Familia.nome == nome_familia).first()

    if not familia:
        await update.message.reply_text(f"❌ Família '{nome_familia}' não encontrada.")
        db.close()
        return

    familia.emoji = emoji
    db.commit()
    db.close()

    await update.message.reply_text(
        f"Emoji da família {nome_familia} atualizado para {emoji} com sucesso!"
    )

# -----------------------------
# Comando /meuid
# -----------------------------
async def cmd_meuid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    await update.message.reply_text(f"O teu Telegram ID é: {telegram_id}")

# -----------------------------
# Comando desconhecido
# -----------------------------
async def cmd_desconhecido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Comando inválido.\nUsa /start para veres como funciona."
    )

# -----------------------------
# Handler principal
# -----------------------------
async def tratar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    telegram_id = str(update.effective_user.id)

    db = SessionLocal()
    try:
        resposta = processar_mensagem(db, telegram_id, texto)
    finally:
        db.close()

    await update.message.reply_text(resposta)


# -----------------------------
# MAIN
# -----------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("addfamilia", cmd_addfamilia))
    app.add_handler(CommandHandler("addproduto", cmd_addproduto))
    app.add_handler(CommandHandler("addloja", cmd_addloja))
    app.add_handler(CommandHandler("addlojista", cmd_addlojista))
    app.add_handler(CommandHandler("emoji", cmd_emoji))
    app.add_handler(CommandHandler("meuid", cmd_meuid))

    # Mensagens normais
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))

    # Handler para comandos inválidos
    app.add_handler(MessageHandler(filters.COMMAND, cmd_desconhecido))


    app.run_polling()


if __name__ == "__main__":
    main()