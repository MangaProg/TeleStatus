from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# 1. Definir o nome da base de dados
# ---------------------------------------------------------
DATABASE_URL = "sqlite:///./database.db"

# ---------------------------------------------------------
# 2. Criar o engine (ligação à base de dados)
# ---------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necessário para SQLite + multithreading
)

# ---------------------------------------------------------
# 3. Criar a Base para os modelos herdarem
# ---------------------------------------------------------
Base = declarative_base()

# ---------------------------------------------------------
# 4. Criar a fábrica de sessões
# ---------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------------------------------
# 5. Função para inicializar a base de dados
# ---------------------------------------------------------
def init_db():
    """
    Cria todas as tabelas definidas em models.py.
    Deve ser chamada uma vez no arranque do sistema.
    """
    from core import models  # Import tardio para evitar circular imports
    Base.metadata.create_all(bind=engine)