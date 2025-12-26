import os
from dotenv import load_dotenv

#Carrega as variáveis locais do .env
load_dotenv()

#Token do bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

#IDs dos administradores
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]

#URL da base de dados
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://database.db")

#Ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

