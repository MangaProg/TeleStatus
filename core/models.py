from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
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

    lojas = relationship("Loja", back_populates="area", cascade="all, delete")


# ---------------------------------------------------------
# Tabela: LOJAS
# ---------------------------------------------------------
class Loja(Base):
    __tablename__ = "lojas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    area_id = Column(Integer, ForeignKey("areas.id", ondelete="SET NULL"))

    area = relationship("Area", back_populates="lojas")
    lojistas = relationship("Lojista", back_populates="loja", cascade="all, delete")
    registos = relationship("Registo", back_populates="loja", cascade="all, delete")


# ---------------------------------------------------------
# Tabela: LOJISTAS
# ---------------------------------------------------------
class Lojista(Base):
    __tablename__ = "lojistas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telegram_id = Column(Integer, unique=True, nullable=False)
    loja_id = Column(Integer, ForeignKey("lojas.id", ondelete="CASCADE"))

    loja = relationship("Loja", back_populates="lojistas")
    registos = relationship("Registo", back_populates="lojista", cascade="all, delete")


# ---------------------------------------------------------
# Tabela: FAMÍLIAS
# ---------------------------------------------------------
class Familia(Base):
    __tablename__ = "familias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    emoji = Column(String, nullable=True)

    produtos = relationship("Produto", back_populates="familia", cascade="all, delete")


# ---------------------------------------------------------
# Tabela: PRODUTOS
# ---------------------------------------------------------
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    pontos = Column(Float, nullable=False)
    familia_id = Column(Integer, ForeignKey("familias.id", ondelete="CASCADE"))

    familia = relationship("Familia", back_populates="produtos")
    registos = relationship("Registo", back_populates="produto", cascade="all, delete")


# ---------------------------------------------------------
# Tabela: REGISTOS
# ---------------------------------------------------------
class Registo(Base):
    __tablename__ = "registos"

    id = Column(Integer, primary_key=True, index=True)
    lojista_id = Column(Integer, ForeignKey("lojistas.id", ondelete="CASCADE"))
    loja_id = Column(Integer, ForeignKey("lojas.id", ondelete="CASCADE"))
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"))
    quantidade = Column(Integer, nullable=False)
    pontos_totais = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

    lojista = relationship("Lojista", back_populates="registos")
    loja = relationship("Loja", back_populates="registos")
    produto = relationship("Produto", back_populates="registos")
