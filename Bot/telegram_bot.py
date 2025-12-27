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
from Bot.menus import (
    menu_admin,
    menu_user,
    menu_admin_lojas,
    menu_admin_produtos,
    menu_admin_lojistas,
    menu_admin_relatorios,
    menu_admin_config,
    menu_user_produtos,
    menu_user_pontos,
)
from Bot.messages import (
    WELCOME_ADMIN,
    WELCOME_USER,
    ADMIN_ONLY,
)

# =========================================================
# FUNÇÃO AUXILIAR: VERIFICAR ADMIN
# =========================================================
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# =========================================================
# COMANDO /start
# =========================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name

    if is_admin(user_id):
        await update.message.reply_text(
            WELCOME_ADMIN.format(first_name=first_name),
            reply_markup=menu_admin
        )
    else:
        await update.message.reply_text(
            WELCOME_USER.format(first_name=first_name),
            reply_markup=menu_user
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
# CALLBACK HANDLER (CORRIGIDO)
# =========================================================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    first_name = query.from_user.first_name

    await query.answer()

    # -------------------------------
    # VERIFICAÇÃO DE PERMISSÕES
    # -------------------------------
    if query.data.startswith(("admin_", "lojas_", "produtos_", "lojistas_", "relatorio_", "config_")):
        if not is_admin(user_id):
            await query.edit_message_text(f"❌ {first_name}, não tens permissão para usar esta opção.")
            return

    # -------------------------------
    # CALLBACKS DO MENU ADMIN
    # -------------------------------
    if query.data == "admin_lojas":
        await query.edit_message_text("🏬 Gestão de lojas:", reply_markup=menu_admin_lojas)
        return

    if query.data == "admin_produtos":
        await query.edit_message_text("📦 Gestão de produtos:", reply_markup=menu_admin_produtos)
        return

    if query.data == "admin_lojistas":
        await query.edit_message_text("👥 Gestão de lojistas:", reply_markup=menu_admin_lojistas)
        return

    if query.data == "admin_relatorios":
        await query.edit_message_text("📊 Relatórios:", reply_markup=menu_admin_relatorios)
        return

    if query.data == "admin_config":
        await query.edit_message_text("⚙️ Configurações:", reply_markup=menu_admin_config)
        return

    # -------------------------------
    # CALLBACKS DO MENU USER
    # -------------------------------
    if query.data == "user_produtos":
        await query.edit_message_text("📦 Produtos disponíveis:", reply_markup=menu_user_produtos)
        return

    if query.data == "user_pontos":
        await query.edit_message_text("📊 Consultar pontos:", reply_markup=menu_user_pontos)
        return

    # -------------------------------
    # SUBMENUS USER
    # -------------------------------
    if query.data == "user_produtos_lista":
        await query.edit_message_text("📦 Lista completa de produtos (em desenvolvimento).")
        return

    if query.data == "user_pontos_dia":
        await query.edit_message_text("📅 Pontos do dia (em desenvolvimento).")
        return

    if query.data == "user_pontos_mes":
        await query.edit_message_text("📆 Pontos do mês (em desenvolvimento).")
        return

    # -------------------------------
    # BOTÃO VOLTAR
    # -------------------------------
    if query.data == "admin_back":
        await query.edit_message_text(f"👋 Olá, {first_name}!\nEscolhe uma opção:", reply_markup=menu_admin)
        return

    if query.data == "user_back":
        await query.edit_message_text(f"👋 Olá, {first_name}!\nEscolhe uma opção:", reply_markup=menu_user)
        return

    # -------------------------------
    # PLACEHOLDERS PARA CRUD
    # -------------------------------
    if query.data.startswith(("lojas_", "produtos_", "lojistas_", "relatorio_", "config_")):
        await query.edit_message_text("⚠️ Esta funcionalidade ainda está em desenvolvimento.")
        return


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

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meuspontos", meuspontos))
    app.add_handler(CommandHandler("meuid", meuid))

    # Callback buttons
    app.add_handler(CallbackQueryHandler(callback_handler))

    # Mensagens normais
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tratar_mensagem))

    print("🤖 Bot iniciado com sucesso!")
    app.run_polling()