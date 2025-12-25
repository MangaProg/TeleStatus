from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# =========================================================
# MENU PRINCIPAL – ADMIN
# =========================================================
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

# =========================================================
# MENU PRINCIPAL – USER
# =========================================================
menu_user = InlineKeyboardMarkup([
    [InlineKeyboardButton("📦 Ver produtos", callback_data="user_produtos")],
    [InlineKeyboardButton("📊 Consultar pontos", callback_data="user_pontos")]
])

# =========================================================
# SUBMENU – LOJAS
# =========================================================
menu_admin_lojas = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Adicionar loja", callback_data="lojas_add")],
    [InlineKeyboardButton("✏️ Editar loja", callback_data="lojas_edit")],
    [InlineKeyboardButton("❌ Remover loja", callback_data="lojas_remove")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="admin_back")]
])

# =========================================================
# SUBMENU – PRODUTOS
# =========================================================
menu_admin_produtos = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Adicionar produto", callback_data="produtos_add")],
    [InlineKeyboardButton("✏️ Editar produto", callback_data="produtos_edit")],
    [InlineKeyboardButton("❌ Remover produto", callback_data="produtos_remove")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="admin_back")]
])

# =========================================================
# SUBMENU – LOJISTAS
# =========================================================
menu_admin_lojistas = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Adicionar lojista", callback_data="lojistas_add")],
    [InlineKeyboardButton("✏️ Editar lojista", callback_data="lojistas_edit")],
    [InlineKeyboardButton("❌ Remover lojista", callback_data="lojistas_remove")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="admin_back")]
])

# =========================================================
# SUBMENU – RELATÓRIOS
# =========================================================
menu_admin_relatorios = InlineKeyboardMarkup([
    [InlineKeyboardButton("📅 Relatório diário", callback_data="relatorio_diario")],
    [InlineKeyboardButton("📆 Relatório mensal", callback_data="relatorio_mensal")],
    [InlineKeyboardButton("🏬 Relatório por loja", callback_data="relatorio_loja")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="admin_back")]
])

# =========================================================
# SUBMENU – CONFIGURAÇÕES
# =========================================================
menu_admin_config = InlineKeyboardMarkup([
    [InlineKeyboardButton("👑 Gerir administradores", callback_data="config_admins")],
    [InlineKeyboardButton("⚙️ Parâmetros do sistema", callback_data="config_parametros")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="admin_back")]
])

# =========================================================
# SUBMENU – USER: PRODUTOS
# =========================================================
menu_user_produtos = InlineKeyboardMarkup([
    [InlineKeyboardButton("📦 Ver lista completa", callback_data="user_produtos_lista")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="user_back")]
])

# =========================================================
# SUBMENU – USER: PONTOS
# =========================================================
menu_user_pontos = InlineKeyboardMarkup([
    [InlineKeyboardButton("📊 Ver pontos do dia", callback_data="user_pontos_dia")],
    [InlineKeyboardButton("📆 Ver pontos do mês", callback_data="user_pontos_mes")],
    [InlineKeyboardButton("🔙 Voltar", callback_data="user_back")]
])