from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
from schema.schema import ArtigoCreate, ArtigoResponse, Usuario, UsuarioCreate, UsuarioUpdate, Empreendimento, EmpreendimentoCreate, EmpreendimentoUpdate, AreaInteresse, AreaInteresseCreate, AreaInteresseUpdate
from model.model import Base
from db.db import engine, SessionLocal
from auth.auth import authenticate_user, create_access_token, get_current_user  # Importar funções de autenticação
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware

# Definir o app primeiro
app = FastAPI()

# Adicionar o middleware CORS após definir o app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens (ou especifique o domínio do frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota de login para gerar o token JWT
@app.post("/token")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.nome_usuario}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/usuarios/{usuario_id}/areas-interesse", response_model=List[AreaInteresse])
def get_areas_interesse_usuario(usuario_id: int, db: Session = Depends(get_db)):
    areas_interesse = crud.get_areas_interesse_usuario(db=db, usuario_id=usuario_id)
    if not areas_interesse:
        raise HTTPException(status_code=404, detail="Áreas de Interesse não encontradas para este usuário")
    return areas_interesse

# Rotas de Usuários
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