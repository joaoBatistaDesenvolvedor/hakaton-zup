from pydantic import BaseModel

class UserCreate(BaseModel):
    nome_usuario: str
    nome_completo: str
    email: str
    senha: str

    class Config:
        orm_mode = True
