from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class AreaInteresse(Base):
    __tablename__ = "areas_interesse"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False)
