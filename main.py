from core.database import init_db
from Bot.telegram_bot import main as start_bot

if __name__ == "__main__":
    init_db()
    print("Base de dados criada com sucesso!")
    start_bot()