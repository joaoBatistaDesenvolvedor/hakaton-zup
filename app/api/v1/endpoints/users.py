from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, User
from app.db.models.user import User as UserModel
from app.db.session import SessionLocal
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/", response_model=User)
def criar_usuario(user: UserCreate, db: Session = Depends(SessionLocal)):
    # Verifica se o nome de usuário já existe
    db_user = db.query(UserModel).filter(UserModel.nome_usuario == user.nome_usuario).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já existe")
    
    # Cria o novo usuário
    hashed_password = get_password_hash(user.senha)
    db_user = UserModel(
        nome_usuario=user.nome_usuario,
        senha=hashed_password,
        nome_completo=user.nome_completo,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
