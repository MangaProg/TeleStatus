# main.py

import os
from core.database import init_db
from Bot.telegram_bot import iniciar_bot
from config import DATABASE_URL

def database_exists() -> bool:
    """
    Verifica se a base de dados já existe.
    Funciona para SQLite e assume que PostgreSQL já existe no servidor.
    """
    if DATABASE_URL.startswith("sqlite:///"):
        path = DATABASE_URL.replace("sqlite:///", "")
        return os.path.exists(path)

    # Para PostgreSQL ou outros, assume-se que a BD já existe
    return True


if __name__ == "__main__":
    if not database_exists():
        init_db()
        print("Base de dados criada com sucesso!")
    else:
        print("Base de dados já existente. A iniciar o bot...")

    iniciar_bot()
    print("Bot Telegram iniciado com sucesso!")