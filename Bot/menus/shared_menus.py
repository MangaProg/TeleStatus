# Bot/menus/shared_menus.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Botão voltar genérico (caso precises no futuro)
back_button = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Voltar", callback_data="back")]
])

# Exemplo de botões comuns (para uso futuro)
confirm_cancel_menu = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("✔ Confirmar", callback_data="confirm"),
        InlineKeyboardButton("❌ Cancelar", callback_data="cancel"),
    ]
])