# Bot/menus/user_menus.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Menu principal do utilizador
menu_user = InlineKeyboardMarkup([
    [InlineKeyboardButton("📦 Produtos", callback_data="user_produtos")],
    [InlineKeyboardButton("📊 Meus Pontos", callback_data="user_pontos")],
])

# Submenu: Produtos
menu_user_produtos = InlineKeyboardMarkup([
    [InlineKeyboardButton("📋 Lista de Produtos", callback_data="user_produtos_lista")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="user_back")],
])

# Submenu: Pontos
menu_user_pontos = InlineKeyboardMarkup([
    [InlineKeyboardButton("📅 Pontos do Dia", callback_data="user_pontos_dia")],
    [InlineKeyboardButton("📆 Pontos do Mês", callback_data="user_pontos_mes")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="user_back")],
])