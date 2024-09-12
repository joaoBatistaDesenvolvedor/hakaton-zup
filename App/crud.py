from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session # Corrigido: importando Session do módulo correto
from sqlalchemy.ext.asyncio import AsyncSession
# No arquivo App/crud.py
from App.model import EmpreendimentoAreaInteresse, Usuario, Empreendimento, AreaInteresse, Artigo, ArtigoAreaInteresse
from App.model import AreaInteresse
from App.schema import AreaInteresseCreate, ArtigoCreate, EmpreendimentoCreate, UsuarioCreate
async def get_usuario_by_nome(db: AsyncSession, nome_usuario: str):
    result = await db.execute(select(Usuario).where(Usuario.nome_usuario == nome_usuario))
    return result.scalars().first()

async def create_usuario(db: AsyncSession, user: UsuarioCreate):
    db_user = Usuario(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def create_empreendimento(db: AsyncSession, empreendimento: EmpreendimentoCreate, usuario_id: int):
    db_empreendimento = Empreendimento(**empreendimento.dict(), usuario_id=usuario_id)
    db.add(db_empreendimento)
    await db.commit()
    await db.refresh(db_empreendimento)
    return db_empreendimento

async def get_empreendimento_by_id(db: AsyncSession, empreendimento_id: int):
    result = await db.execute(select(Empreendimento).filter(Empreendimento.id == empreendimento_id))
    return result.scalar_one_or_none()
async def create_area_interesse(db: AsyncSession, area: AreaInteresseCreate):
    db_area = AreaInteresse(nome=area.nome)
    db.add(db_area)
    await db.commit()
    await db.refresh(db_area)
    return db_area
async def create_empreendimento_area_interesse(db: Session, empreendimento_id: int, area_interesse_id: int):
    empreendimento_area = EmpreendimentoAreaInteresse(
        empreendimento_id=empreendimento_id,
        area_interesse_id=area_interesse_id
    )
    db.add(empreendimento_area)
    db.commit()
    db.refresh(empreendimento_area)
    return empreendimento_area
async def get_areas_interesse(db: AsyncSession):
    result = await db.execute(select(AreaInteresse))
    return result.scalars().all()


async def create_artigo(db: AsyncSession, artigo: ArtigoCreate):
    db_artigo = Artigo(**artigo.dict())
    db.add(db_artigo)
    await db.commit()
    await db.refresh(db_artigo)
    return db_artigo
async def create_artigos_areas_interesse(db: Session, artigo_id: int, area_interesse_id: int):
    associacao = ArtigoAreaInteresse(artigo_id=artigo_id, area_interesse_id=area_interesse_id)
    db.add(associacao)
    await db.commit()
    await db.refresh(associacao)
    return associacao