from sqlalchemy import Column, Integer, ForeignKey
from app.db.base_class import Base

class EmpreendimentoAreaInteresse(Base):
    __tablename__ = "empreendimentos_areas_interesse"

    empreendimento_id = Column(Integer, ForeignKey("empreendimentos.id", ondelete="CASCADE"), primary_key=True)
    area_interesse_id = Column(Integer, ForeignKey("areas_interesse.id", ondelete="CASCADE"), primary_key=True)
