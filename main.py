from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
from  schema.schema import ArtigoCreate, ArtigoResponse, Usuario, UsuarioCreate, UsuarioUpdate, Empreendimento, EmpreendimentoCreate, EmpreendimentoUpdate, AreaInteresse, AreaInteresseCreate,AreaInteresseUpdate
from model.model import Base
from db.db import engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios/", response_model=Usuario)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario


@app.put("/usuarios/{usuario_id}", response_model=Usuario)
def update_usuario(usuario_id: int, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)):
    return crud.update_usuario(db=db, usuario_id=usuario_id, usuario_update=usuario_update)

@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud.delete_usuario(db=db, usuario_id=usuario_id)

# Rotas de Empreendimentos
@app.post("/empreendimentos/", response_model=Empreendimento)
def create_empreendimento(empreendimento: EmpreendimentoCreate, db: Session = Depends(get_db)):
    return crud.create_empreendimento(db=db, empreendimento=empreendimento)

@app.get("/empreendimentos/{empreendimento_id}", response_model=Empreendimento)
def read_empreendimento(empreendimento_id: int, db: Session = Depends(get_db)):
    db_empreendimento = crud.get_empreendimento(db, empreendimento_id=empreendimento_id)
    if db_empreendimento is None:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    return db_empreendimento


@app.put("/empreendimentos/{empreendimento_id}", response_model=Empreendimento)
def update_empreendimento(empreendimento_id: int, empreendimento_update: EmpreendimentoUpdate, db: Session = Depends(get_db)):
    return crud.update_empreendimento(db=db, empreendimento_id=empreendimento_id, empreendimento_update=empreendimento_update)

@app.delete("/empreendimentos/{empreendimento_id}")
def delete_empreendimento(empreendimento_id: int, db: Session = Depends(get_db)):
    return crud.delete_empreendimento(db=db, empreendimento_id=empreendimento_id)

# Rotas de Áreas de Interesse
@app.post("/areas-interesse/", response_model=AreaInteresse)
def create_area_interesse(area_interesse: AreaInteresseCreate, db: Session = Depends(get_db)):
    return crud.create_area_interesse(db=db, area_interesse=area_interesse)

@app.get("/areas-interesse/{area_interesse_id}", response_model=AreaInteresse)
def read_area_interesse(area_interesse_id: int, db: Session = Depends(get_db)):
    db_area_interesse = crud.get_area_interesse(db, area_interesse_id=area_interesse_id)
    if db_area_interesse is None:
        raise HTTPException(status_code=404, detail="Área de Interesse não encontrada")
    return db_area_interesse


@app.put("/areas-interesse/{area_interesse_id}", response_model=AreaInteresse)
def update_area_interesse(area_interesse_id: int, area_interesse_update: AreaInteresseUpdate, db: Session = Depends(get_db)):
    return crud.update_area_interesse(db=db, area_interesse_id=area_interesse_id, area_interesse_update=area_interesse_update)

@app.delete("/areas-interesse/{area_interesse_id}")
def delete_area_interesse(area_interesse_id: int, db: Session = Depends(get_db)):
    return crud.delete_area_interesse(db=db, area_interesse_id=area_interesse_id)
@app.post("/artigos/", response_model=ArtigoResponse)
def create_artigo(artigo: ArtigoCreate, db: Session = Depends(get_db)):
    return crud.create_artigo(db=db, titulo=artigo.titulo, conteudo=artigo.conteudo, link=artigo.link)

# Endpoint para associar um artigo a uma área de interesse
@app.post("/artigos/{artigo_id}/areas-interesse/{area_interesse_id}")
def associate_artigo_area_interesse(artigo_id: int, area_interesse_id: int, db: Session = Depends(get_db)):
    return crud.associate_artigo_area_interesse(db=db, artigo_id=artigo_id, area_interesse_id=area_interesse_id)

# Endpoint para listar todos os artigos
@app.get("/artigos/", response_model=List[ArtigoResponse])
def list_artigos(db: Session = Depends(get_db)):
    return crud.get_artigos(db=db)

# Endpoint para listar artigos por área de interesse
@app.get("/areas-interesse/{area_interesse_id}/artigos", response_model=List[ArtigoResponse])
def list_artigos_por_area_interesse(area_interesse_id: int, db: Session = Depends(get_db)):
    artigos = crud.get_artigos_por_area_interesse(db=db, area_interesse_id=area_interesse_id)
    if not artigos:
        raise HTTPException(status_code=404, detail="Nenhum artigo encontrado para essa área de interesse")
    return artigos
