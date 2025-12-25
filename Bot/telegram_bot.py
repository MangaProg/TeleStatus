from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from core.database import SessionLocal
from core.logic import processar_mensagem
from core.models import Familia

# Lista de administradores
ADMIN_IDS = [123456789]  # substitui pelo teu telegram_id

TOKEN = "8103956919:AAEdnLz-OsCCK7IOSgWjsSW3D-4O4ZbZ7rc"


# -----------------------------
# Comando /start
# -----------------------------
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Envia-me os teus registos (ex.: 'tv premium 3') que eu trato do resto."
    )


# -----------------------------
# Comando /emoji (já tinhas)
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
# Handler principal (mensagens normais)
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
    app.add_handler(CommandHandler("emoji", cmd_emoji))

    # Mensagens normais
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))

    app.run_polling()


if __name__ == "__main__":
    main()