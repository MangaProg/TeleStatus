# =========================================================
# MENSAGENS PARA ADMINISTRADORES
# =========================================================

WELCOME_ADMIN = """
👋 Olá, {first_name}!

Bem-vindo ao painel de administração.
Escolhe uma das opções abaixo para gerir o sistema.
"""

ADMIN_ONLY = """
❌ {first_name}, não tens permissão para usar este comando.
"""

ADMIN_ACTION_SUCCESS = """
✅ {first_name}, a ação foi concluída com sucesso.
"""

ADMIN_ACTION_ERROR = """
❌ {first_name}, ocorreu um erro ao executar esta ação.
"""


# =========================================================
# MENSAGENS PARA UTILIZADORES NORMAIS
# =========================================================

WELCOME_USER = """
👋 Olá, {first_name}!

Bem-vindo ao sistema de status.
Escolhe uma das opções abaixo para consultar informações.
"""

USER_NOT_REGISTERED = """
❌ {first_name}, não estás registado no sistema.
Por favor, contacta um administrador.
"""

USER_ACTION_SUCCESS = """
✅ {first_name}, a tua ação foi registada com sucesso.
"""

USER_ACTION_ERROR = """
❌ {first_name}, ocorreu um erro ao processar a tua ação.
"""


# =========================================================
# MENSAGENS COMUNS
# =========================================================

UNKNOWN_COMMAND = """
❌ {first_name}, esse comando não existe.
Usa /start para veres as opções disponíveis.
"""

INVALID_FORMAT = """
❌ {first_name}, o formato da mensagem não é válido.
"""

LIMIT_EXCEEDED = """
❌ {first_name}, excedeste o limite máximo de linhas permitidas.
"""

NOT_FOUND = """
❌ {first_name}, o item que procuras não foi encontrado.
"""

ALREADY_EXISTS = """
⚠️ {first_name}, esse item já existe no sistema.
"""