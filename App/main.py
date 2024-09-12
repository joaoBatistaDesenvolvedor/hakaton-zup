from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from App import crud
from App.database import SessionLocal
from sqlalchemy.orm import Session # Corrigido: importando Session do módulo correto

from App.model import Artigo, EmpreendimentoAreaInteresse, Usuario, Empreendimento, AreaInteresse
from App.schema import ArtigoAreaInteresseCreate, ArtigoCreate, ArtigoResponse, EmpreendimentoAreaInteresseCreate, UsuarioCreate, EmpreendimentoCreate
from App.crud import create_artigo, create_artigos_areas_interesse, create_usuario, get_usuario_by_nome, create_empreendimento, get_empreendimento_by_id
from App.auth import hash_password, create_access_token, verify_password
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from App.auth import SECRET_KEY, ALGORITHM

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_usuario_by_nome(db, username)
    if user is None:
        raise credentials_exception
    return user

# Usuários
@app.post("/usuarios/")
async def register_usuario(user: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    user_in_db = await get_usuario_by_nome(db, user.nome_usuario)
    if user_in_db:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    user.senha = hash_password(user.senha)
    return await create_usuario(db, user)

class LoginRequest(BaseModel):
    nome_usuario: str
    senha: str

@app.post("/login/")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_usuario_by_nome(db, request.nome_usuario)
    if not user or not verify_password(request.senha, user.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.nome_usuario}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Empreendimentos
class EmpreendimentoCreate(BaseModel):
    tipo_empreeendimento: str
    descricao_empreeendimento: str
    objetivo: str

@app.post("/empreendimentos/")
async def create_empreendimento_endpoint(empreendimento: EmpreendimentoCreate, db: AsyncSession = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return await create_empreendimento(db, empreendimento, current_user.id)

@app.get("/empreendimentos/{empreendimento_id}")
async def get_empreendimento_endpoint(empreendimento_id: int, db: AsyncSession = Depends(get_db)):
    empreendimento = await get_empreendimento_by_id(db, empreendimento_id)
    if not empreendimento:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    return empreendimento

# Áreas de Interesse
class AreaInteresseCreate(BaseModel):
    nome: str

@app.post("/areas_interesse/")
async def create_area_interesse_endpoint(area_interesse: AreaInteresseCreate, db: AsyncSession = Depends(get_db)):
    new_area_interesse = AreaInteresse(nome=area_interesse.nome)
    db.add(new_area_interesse)
    await db.commit()
    return new_area_interesse

@app.get("/areas_interesse/{area_id}")
async def get_area_interesse_endpoint(area_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AreaInteresse).filter(AreaInteresse.id == area_id))
    area_interesse = result.scalar()
    if not area_interesse:
        raise HTTPException(status_code=404, detail="Área de interesse não encontrada")
    return area_interesse

@app.post("/empreendimentos-areas-interesse/")
async def create_empreendimento_area_interesse(
    empreendimento_area: EmpreendimentoAreaInteresseCreate,
    db: AsyncSession = Depends(get_db)
):
    # Checa se a associação já existe (opcional)
    result = await db.execute(
        select(EmpreendimentoAreaInteresse).filter_by(
            empreendimento_id=empreendimento_area.empreendimento_id,
            area_interesse_id=empreendimento_area.area_interesse_id
        )
    )
    existing_association = result.scalar()

    if existing_association:
        raise HTTPException(status_code=400, detail="Associação já existe.")

    # Cria a nova associação
    return await crud.create_empreendimento_area_interesse(
        db=db,
        empreendimento_id=empreendimento_area.empreendimento_id,
        area_interesse_id=empreendimento_area.area_interesse_id
    )
@app.post("/artigos/", response_model=ArtigoResponse)
async def create_artigo(artigo: ArtigoCreate, db: AsyncSession = Depends(get_db)):
    new_artigo = Artigo(
        titulo=artigo.titulo,
        conteudo=artigo.conteudo,
        link=artigo.link
    )
    db.add(new_artigo)
    await db.commit()
    await db.refresh(new_artigo)
    return new_artigo
@app.post("/artigos-areas-interesse/")
async def associar_artigo_area_interesse(
    body: ArtigoAreaInteresseCreate, db: AsyncSession = Depends(get_db)
):
    return await create_artigos_areas_interesse(db, body.artigo_id, body.area_interesse_id)
