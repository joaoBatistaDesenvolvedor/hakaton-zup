from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    nome_completo = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    # Relacionamento com empreendimentos
    empreendimentos = relationship("Empreendimento", back_populates="usuario")

