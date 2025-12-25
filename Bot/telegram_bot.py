from core.database import SessionLocal
from core.models import Familia

ADMIN_IDS = [123456789]  # substitui pelo teu telegram_id

async def cmd_emoji(update, context):
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

    await update.message.reply_text(f"Emoji da família {nome_familia} atualizado para {emoji} com sucesso!")

# application.add_handler(CommandHandler("emoji", cmd_emoji)) - Adicionar este handler na configuração do bot quando for criado