# Bot/handlers_user.py

from telegram import Update
from telegram.ext import ContextTypes

# Menus modularizados
from Bot.menus.user_menus import (
    menu_user,
    menu_user_produtos,
    menu_user_pontos,
)


# =========================================================
# MENU PRINCIPAL DO UTILIZADOR
# =========================================================
async def user_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    first_name = user.first_name

    await update.message.reply_text(
        f"👋 Olá, {first_name}!\nEscolhe uma opção:",
        reply_markup=menu_user,
    )


# =========================================================
# CALLBACKS DO MENU USER
# =========================================================
async def user_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    first_name = user.first_name

    await query.answer()

    # -------------------------------
    # MENU PRINCIPAL DO USER
    # -------------------------------
    if query.data == "user_menu":
        await query.edit_message_text(
            f"👋 Olá, {first_name}!\nEscolhe uma opção:",
            reply_markup=menu_user,
        )
        return

    # -------------------------------
    # PRODUTOS
    # -------------------------------
    if query.data == "user_produtos":
        await query.edit_message_text(
            "📦 Produtos disponíveis:",
            reply_markup=menu_user_produtos,
        )
        return

    if query.data == "user_produtos_lista":
        await query.edit_message_text(
            "📦 Lista completa de produtos (em desenvolvimento)."
        )
        return

    # -------------------------------
    # PONTOS
    # -------------------------------
    if query.data == "user_pontos":
        await query.edit_message_text(
            "📊 Consultar pontos:",
            reply_markup=menu_user_pontos,
        )
        return

    if query.data == "user_pontos_dia":
        await query.edit_message_text(
            "📅 Pontos do dia (em desenvolvimento)."
        )
        return

    if query.data == "user_pontos_mes":
        await query.edit_message_text(
            "📆 Pontos do mês (em desenvolvimento)."
        )
        return

    # -------------------------------
    # BOTÃO VOLTAR
    # -------------------------------
    if query.data == "user_back":
        await query.edit_message_text(
            f"👋 Olá, {first_name}!\nEscolhe uma opção:",
            reply_markup=menu_user,
        )
        return


# =========================================================
# REGISTO DOS HANDLERS
# =========================================================
def register_user_handlers(app):
    from telegram.ext import CallbackQueryHandler, CommandHandler

    # Comando /menu (opcional)
    app.add_handler(CommandHandler("menu", user_menu))

    # Callback handler do utilizador
    app.add_handler(
        CallbackQueryHandler(
            user_callback_handler,
            pattern="^(user_|user_back)"
        )
    )