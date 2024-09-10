from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String(50), unique=True, index=True)
    senha = Column(Text)
    nome_completo = Column(String(100))
    email = Column(String(100), unique=True, index=True)

class Empreendimento(Base):
    __tablename__ = "empreendimentos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    tipo_empreeendimento = Column(String(50))
    descricao_empreeendimento = Column(Text)
    objetivo = Column(Text)
    
    usuario = relationship("Usuario")

class AreaInteresse(Base):
    __tablename__ = "areas_interesse"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, index=True)

class EmpreendimentosAreasInteresse(Base):
    __tablename__ = "empreendimentos_areas_interesse"

    empreendimento_id = Column(Integer, ForeignKey("empreendimentos.id"), primary_key=True)
    area_interesse_id = Column(Integer, ForeignKey("areas_interesse.id"), primary_key=True)

class Artigo(Base):
    __tablename__ = "artigos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255))
    conteudo = Column(Text)
    link = Column(String(255))

class ArtigosAreasInteresse(Base):
    __tablename__ = "artigos_areas_interesse"

    artigo_id = Column(Integer, ForeignKey("artigos.id"), primary_key=True)
    area_interesse_id = Column(Integer, ForeignKey("areas_interesse.id"), primary_key=True)