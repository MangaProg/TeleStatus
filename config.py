import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# ---------------------------------------------------------
# BOT TOKEN
# ---------------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN or BOT_TOKEN.strip() == "":
    raise ValueError("❌ ERRO: A variável BOT_TOKEN não está definida no .env")


# ---------------------------------------------------------
# ADMIN IDS
# ---------------------------------------------------------
raw_admins = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(x) for x in raw_admins.split(",") if x.strip().isdigit()]

if len(ADMIN_IDS) == 0:
    print("⚠️ AVISO: ADMIN_IDS está vazio. Nenhum administrador definido.")


# ---------------------------------------------------------
# DATABASE URL
# ---------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if DATABASE_URL == "":
    raise ValueError("❌ ERRO: A variável DATABASE_URL não está definida no .env")

# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------
ENVIRONMENT = os.getenv("ENVIRONMENT", "local").lower()
if ENVIRONMENT not in ("local", "prod", "dev"):
    print(f"⚠️ AVISO: ENVIRONMENT '{ENVIRONMENT}' não é válido. Usando 'local'.")
    ENVIRONMENT = "local"