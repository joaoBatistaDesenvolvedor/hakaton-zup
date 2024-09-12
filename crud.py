from sqlalchemy.orm import Session
from model.model import Usuario, Empreendimento, AreaInteresse  # Importar as classes corretas do model
from schema.schema import UsuarioCreate, UsuarioUpdate, EmpreendimentoCreate, EmpreendimentoUpdate, AreaInteresseCreate, AreaInteresseUpdate
from fastapi import HTTPException

# Funções de CRUD para Usuários
def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(**usuario.dict())  # Usar a classe Usuario do model
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def update_usuario(db: Session, usuario_id: int, usuario_update: UsuarioUpdate):
    db_usuario = get_usuario(db, usuario_id=usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    update_data = usuario_update.dict(exclude_unset=True)
    for attr, value in update_data.items():
        setattr(db_usuario, attr, value)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario(db, usuario_id=usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(db_usuario)
    db.commit()
    return {"message": f"Usuário {usuario_id} deletado com sucesso"}

# Funções de CRUD para Empreendimentos
def create_empreendimento(db: Session, empreendimento: EmpreendimentoCreate):
    db_empreendimento = Empreendimento(**empreendimento.dict())  # Usar a classe Empreendimento do model
    db.add(db_empreendimento)
    db.commit()
    db.refresh(db_empreendimento)
    return db_empreendimento

def get_empreendimento(db: Session, empreendimento_id: int):
    return db.query(Empreendimento).filter(Empreendimento.id == empreendimento_id).first()

def update_empreendimento(db: Session, empreendimento_id: int, empreendimento_update: EmpreendimentoUpdate):
    db_empreendimento = get_empreendimento(db, empreendimento_id=empreendimento_id)
    if not db_empreendimento:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    update_data = empreendimento_update.dict(exclude_unset=True)
    for attr, value in update_data.items():
        setattr(db_empreendimento, attr, value)
    db.add(db_empreendimento)
    db.commit()
    db.refresh(db_empreendimento)
    return db_empreendimento

def delete_empreendimento(db: Session, empreendimento_id: int):
    db_empreendimento = get_empreendimento(db, empreendimento_id=empreendimento_id)
    if not db_empreendimento:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    db.delete(db_empreendimento)
    db.commit()
    return {"message": f"Empreendimento {empreendimento_id} deletado com sucesso"}

# Funções de CRUD para Área de Interesse
def create_area_interesse(db: Session, area_interesse: AreaInteresseCreate):
    db_area_interesse = AreaInteresse(**area_interesse.dict())  # Usar a classe AreaInteresse do model
    db.add(db_area_interesse)
    db.commit()
    db.refresh(db_area_interesse)
    return db_area_interesse

def get_area_interesse(db: Session, area_interesse_id: int):
    return db.query(AreaInteresse).filter(AreaInteresse.id == area_interesse_id).first()

def update_area_interesse(db: Session, area_interesse_id: int, area_interesse_update: AreaInteresseUpdate):
    db_area_interesse = get_area_interesse(db, area_interesse_id=area_interesse_id)
    if not db_area_interesse:
        raise HTTPException(status_code=404, detail="Área de Interesse não encontrada")
    update_data = area_interesse_update.dict(exclude_unset=True)
    for attr, value in update_data.items():
        setattr(db_area_interesse, attr, value)
    db.add(db_area_interesse)
    db.commit()
    db.refresh(db_area_interesse)
    return db_area_interesse

def delete_area_interesse(db: Session, area_interesse_id: int):
    db_area_interesse = get_area_interesse(db, area_interesse_id=area_interesse_id)
    if not db_area_interesse:
        raise HTTPException(status_code=404, detail="Área de Interesse não encontrada")
    db.delete(db_area_interesse)
    db.commit()
    return {"message": f"Área de Interesse {area_interesse_id} deletada com sucesso"}