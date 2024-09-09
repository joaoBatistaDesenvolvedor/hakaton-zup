from pydantic import BaseModel

class AreaInteresseCreate(BaseModel):
    nome: str

class AreaInteresse(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True
