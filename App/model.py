from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String(50), unique=True, nullable=False)
    senha = Column(Text, nullable=False)
    nome_completo = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    empreendimentos = relationship("Empreendimento", back_populates="usuario")

class Empreendimento(Base):
    __tablename__ = "empreendimentos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    tipo_empreeendimento = Column(String(50))
    descricao_empreeendimento = Column(Text)
    objetivo = Column(Text)
    usuario = relationship("Usuario", back_populates="empreendimentos")

class AreaInteresse(Base):
    __tablename__ = "areas_interesse"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False)

class EmpreendimentoAreaInteresse(Base):
    __tablename__ = "empreendimentos_areas_interesse"
    empreendimento_id = Column(Integer, ForeignKey("empreendimentos.id", ondelete="CASCADE"), primary_key=True)
    area_interesse_id = Column(Integer, ForeignKey("areas_interesse.id", ondelete="CASCADE"), primary_key=True)

class Artigo(Base):
    __tablename__ = "artigos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    conteudo = Column(Text, nullable=False)
    link = Column(String(255))

class ArtigoAreaInteresse(Base):
    __tablename__ = "artigos_areas_interesse"
    artigo_id = Column(Integer, ForeignKey("artigos.id", ondelete="CASCADE"), primary_key=True)
    area_interesse_id = Column(Integer, ForeignKey("areas_interesse.id", ondelete="CASCADE"), primary_key=True)