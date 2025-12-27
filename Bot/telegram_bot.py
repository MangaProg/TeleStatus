from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN, ADMIN_IDS
from core.database import get_db
from core.logic import processar_mensagem, comando_meus_pontos

# Menus
from Bot.menus import menu_user

# Mensagens
from Bot.messages import WELCOME_USER

# Handlers modularizados
from Bot.handlers_admin import register_admin_handlers
from Bot.handlers_user import register_user_handlers


# =========================================================
# FUNÇÃO AUXILIAR: VERIFICAR ADMIN
# =========================================================
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# =========================================================
# COMANDO /start
# =========================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    first_name = user.first_name

    await update.message.reply_text(
        WELCOME_USER.format(first_name=first_name),
        reply_markup=menu_user,
    )


# =========================================================
# COMANDO /meuspontos
# =========================================================
async def meuspontos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id

    with get_db() as db:
        resposta = comando_meus_pontos(db, telegram_id)

    await update.message.reply_text(resposta)


# =========================================================
# COMANDO /meuid
# =========================================================
async def meuid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    await update.message.reply_text(f"O teu Telegram ID é: {telegram_id}")


# =========================================================
# MENSAGENS NORMAIS (REGISTO DE PONTOS)
# =========================================================
async def tratar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    texto = update.message.text

    with get_db() as db:
        resposta = processar_mensagem(db, telegram_id, texto)

    await update.message.reply_text(resposta)


# =========================================================
# MAIN
# =========================================================
def iniciar_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers modularizados
    register_admin_handlers(app)
    register_user_handlers(app)

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meuspontos", meuspontos))
    app.add_handler(CommandHandler("meuid", meuid))

    # Mensagens normais
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))

    print("🤖 Bot iniciado com sucesso!")
    app.run_polling()