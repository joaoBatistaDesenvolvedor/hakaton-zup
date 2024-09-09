from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import verify_password, get_password_hash
from app.db.session import SessionLocal
from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.db.models.user import User

router = APIRouter()

@router.post("/login")
def login(nome_usuario: str, senha: str, db: Session = Depends(SessionLocal)):
    user = db.query(User).filter(User.nome_usuario == nome_usuario).first()
    if not user or not verify_password(senha, user.senha):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    return {"message": "Login realizado com sucesso!"}
