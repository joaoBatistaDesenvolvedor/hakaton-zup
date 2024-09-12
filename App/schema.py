from pydantic import BaseModel
from typing import List, Optional

class UsuarioCreate(BaseModel):
    nome_usuario: str
    senha: str
    nome_completo: str
    email: str

class EmpreendimentoCreate(BaseModel):
    tipo_empreeendimento: str
    descricao_empreeendimento: Optional[str] = None
    objetivo: Optional[str] = None

class AreaInteresseCreate(BaseModel):
    nome: str

class AreaInteresseResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True  # Atualize de orm_mode para from_attributes

class ArtigoCreate(BaseModel):
    titulo: str
    conteudo: str
    link: Optional[str] = None

class ArtigoResponse(BaseModel):
    id: int
    titulo: str
    conteudo: str
    link: Optional[str] = None

    class Config:
        from_attributes = True     
        
from pydantic import BaseModel

class ArtigoAreaInteresseCreate(BaseModel):
    artigo_id: int
    area_interesse_id: int

class EmpreendimentoAreaInteresseCreate(BaseModel):
    empreendimento_id: int
    area_interesse_id: int
