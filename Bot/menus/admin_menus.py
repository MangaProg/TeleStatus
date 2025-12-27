# Bot/menus/admin_menus.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Menu principal do admin
menu_admin = InlineKeyboardMarkup([
    [InlineKeyboardButton("🏬 Lojas", callback_data="admin_lojas")],
    [InlineKeyboardButton("📦 Produtos", callback_data="admin_produtos")],
    [InlineKeyboardButton("👥 Lojistas", callback_data="admin_lojistas")],
    [InlineKeyboardButton("📊 Relatórios", callback_data="admin_relatorios")],
    [InlineKeyboardButton("⚙️ Configurações", callback_data="admin_config")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="user_back")],
])

# Submenu: Lojas
menu_admin_lojas = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Adicionar Loja", callback_data="lojas_add")],
    [InlineKeyboardButton("📋 Listar Lojas", callback_data="lojas_list")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="admin_back")],
])

# Submenu: Produtos
menu_admin_produtos = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Adicionar Produto", callback_data="produtos_add")],
    [InlineKeyboardButton("📋 Listar Produtos", callback_data="produtos_list")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="admin_back")],
])

# Submenu: Lojistas
menu_admin_lojistas = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Adicionar Lojista", callback_data="lojistas_add")],
    [InlineKeyboardButton("📋 Listar Lojistas", callback_data="lojistas_list")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="admin_back")],
])

# Submenu: Relatórios
menu_admin_relatorios = InlineKeyboardMarkup([
    [InlineKeyboardButton("📅 Relatório Diário", callback_data="relatorio_dia")],
    [InlineKeyboardButton("📆 Relatório Mensal", callback_data="relatorio_mes")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="admin_back")],
])

# Submenu: Configurações
menu_admin_config = InlineKeyboardMarkup([
    [InlineKeyboardButton("⚙️ Opção 1", callback_data="config_op1")],
    [InlineKeyboardButton("⚙️ Opção 2", callback_data="config_op2")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="admin_back")],
])