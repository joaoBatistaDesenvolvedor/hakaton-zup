from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Empreendimento(Base):
    __tablename__ = "empreendimentos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    tipo_empreendimento = Column(String(50), nullable=False)
    descricao_empreendimento = Column(Text, nullable=True)
    
    # Relacionamento com usuário
    usuario = relationship("User", back_populates="empreendimentos")
    
    # Relacionamento com áreas de interesse
    areas_interesse = relationship("EmpreendimentoAreaInteresse", back_populates="empreendimento")
