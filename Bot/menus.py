from telegram import InlineKeyboardButton, InlineKeyboardMarkup

menu_admin = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🏬 Lojas", callback_data="admin_lojas"),
        InlineKeyboardButton("📦 Produtos", callback_data="admin_produtos")
    ],
    [
        InlineKeyboardButton("👥 Lojistas", callback_data="admin_lojistas"),
        InlineKeyboardButton("📊 Relatórios", callback_data="admin_relatorios")
    ],
    [
        InlineKeyboardButton("⚙️ Configurações", callback_data="admin_config")
    ]
])

menu_user = InlineKeyboardMarkup([
    [InlineKeyboardButton("📦 Ver produtos", callback_data="user_produtos")],
    [InlineKeyboardButton("📊 Consultar pontos", callback_data="user_pontos")]
])