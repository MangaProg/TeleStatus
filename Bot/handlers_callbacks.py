# Bot/handlers_callbacks.py

from telegram import Update
from telegram.ext import ContextTypes

# Menus modularizados
from Bot.menus.admin_menus import (
    menu_admin,
    menu_admin_lojas,
    menu_admin_produtos,
    menu_admin_lojistas,
    menu_admin_relatorios,
    menu_admin_config,
)

from Bot.menus.user_menus import menu_user

from config import ADMIN_IDS


# =========================================================
# AUXILIAR: VERIFICAR ADMIN
# =========================================================
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# =========================================================
# CALLBACKS GENÉRICOS (NÃO USER, NÃO ADMIN)
# =========================================================
async def generic_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    first_name = user.first_name

    await query.answer()

    # -------------------------------
    # VERIFICAÇÃO DE PERMISSÕES (ÁREA ADMIN)
    # -------------------------------
    if query.data.startswith(("admin_", "lojas_", "produtos_", "lojistas_", "relatorio_", "config_")):
        if not is_admin(user.id):
            await query.edit_message_text(
                f"❌ {first_name}, não tens permissão para usar esta opção."
            )
            return

    # -------------------------------
    # MENUS ADMIN (GENÉRICOS)
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
    # BOTÕES VOLTAR (GENÉRICOS)
    # -------------------------------
    if query.data == "admin_back":
        await query.edit_message_text(
            f"👋 Olá, {first_name}!\nEscolhe uma opção:",
            reply_markup=menu_admin,
        )
        return

    if query.data == "user_back":
        await query.edit_message_text(
            f"👋 Olá, {first_name}!\nEscolhe uma opção:",
            reply_markup=menu_user,
        )
        return

    # -------------------------------
    # PLACEHOLDERS PARA CRUD
    # -------------------------------
    if query.data.startswith(("lojas_", "produtos_", "lojistas_", "relatorio_", "config_")):
        await query.edit_message_text("⚠️ Esta funcionalidade ainda está em desenvolvimento.")
        return


# =========================================================
# REGISTO DOS HANDLERS
# =========================================================
def register_generic_callbacks(app):
    from telegram.ext import CallbackQueryHandler

    app.add_handler(
        CallbackQueryHandler(
            generic_callback_handler,
            pattern="^(admin_|lojas_|produtos_|lojistas_|relatorio_|config_|admin_back|user_back)"
        )
    )