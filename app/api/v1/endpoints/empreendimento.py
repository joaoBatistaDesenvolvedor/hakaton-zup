from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.empreendimento import EmpreendimentoCreate, Empreendimento
from app.db.models.empreendimento import Empreendimento as EmpreendimentoModel

router = APIRouter()

@router.post("/empreendimentos/", response_model=Empreendimento)
def criar_empreendimento(empreendimento: EmpreendimentoCreate, db: Session = Depends(SessionLocal)):
    db_empreendimento = EmpreendimentoModel(**empreendimento.dict())
    db.add(db_empreendimento)
    db.commit()
    db.refresh(db_empreendimento)
    return db_empreendimento
