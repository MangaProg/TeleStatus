from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)

from config import ADMIN_IDS
from Bot.menus import menu_admin

__all__ = ["register_admin_handlers"]


# =========================================================
# AUXILIAR: VERIFICAR ADMIN
# =========================================================
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# =========================================================
# COMANDO /admin
# =========================================================
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Abre o painel de administração apenas para admins."""
    user = update.message.from_user
    first_name = user.first_name

    if not is_admin(user.id):
        await update.message.reply_text(
            "❌ Não tens permissão para aceder ao painel de administração."
        )
        return

    await update.message.reply_text(
        f"👋 Olá, {first_name}! Escolhe uma opção:",
        reply_markup=menu_admin,
    )


# =========================================================
# REGISTO DOS HANDLERS DE ADMIN
# =========================================================
def register_admin_handlers(app):
    """
    Regista todos os handlers relacionados ao admin.
    Mantém o módulo isolado e preparado para crescer.
    """
    app.add_handler(CommandHandler("admin", admin_command))