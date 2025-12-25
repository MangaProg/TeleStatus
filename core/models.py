from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base


# ---------------------------------------------------------
# Tabela: ÁREAS
# ---------------------------------------------------------
class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)

    lojas = relationship("Loja", back_populates="area")


# ---------------------------------------------------------
# Tabela: LOJAS
# ---------------------------------------------------------
class Loja(Base):
    __tablename__ = "lojas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    area_id = Column(Integer, ForeignKey("areas.id"))

    area = relationship("Area", back_populates="lojas")
    lojistas = relationship("Lojista", back_populates="loja")
    registos = relationship("Registo", back_populates="loja")


# ---------------------------------------------------------
# Tabela: LOJISTAS
# ---------------------------------------------------------
class Lojista(Base):
    __tablename__ = "lojistas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telegram_id = Column(String, unique=True, nullable=False)
    loja_id = Column(Integer, ForeignKey("lojas.id"))

    loja = relationship("Loja", back_populates="lojistas")
    registos = relationship("Registo", back_populates="lojista")


# ---------------------------------------------------------
# Tabela: FAMÍLIAS
# ---------------------------------------------------------
class Familia(Base):
    __tablename__ = "familias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)

    produtos = relationship("Produto", back_populates="familia")


# ---------------------------------------------------------
# Tabela: PRODUTOS
# ---------------------------------------------------------
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    pontos = Column(Integer, nullable=False)
    familia_id = Column(Integer, ForeignKey("familias.id"))

    familia = relationship("Familia", back_populates="produtos")
    registos = relationship("Registo", back_populates="produto")


# ---------------------------------------------------------
# Tabela: REGISTOS
# ---------------------------------------------------------
class Registo(Base):
    __tablename__ = "registos"

    id = Column(Integer, primary_key=True, index=True)
    lojista_id = Column(Integer, ForeignKey("lojistas.id"))
    loja_id = Column(Integer, ForeignKey("lojas.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, nullable=False)
    pontos_totais = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

    lojista = relationship("Lojista", back_populates="registos")
    loja = relationship("Loja", back_populates="registos")
    produto = relationship("Produto", back_populates="registos")
