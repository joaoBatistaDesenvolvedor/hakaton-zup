from pydantic import BaseModel
from typing import List, Optional

print("Arquivo schema.py carregado com sucesso")

# Esquemas de Usuário
class UsuarioBase(BaseModel):
    nome_usuario: str
    nome_completo: str
    email: str

    class Config:
        from_attributes = True  # Substitui o orm_mode

class UsuarioCreate(UsuarioBase):
    senha: str
    areas_interesse: List[str]  # Agora aceita uma lista de nomes de áreas de interesse

class UsuarioUpdate(UsuarioBase):
    senha: Optional[str] = None  # Senha opcional para atualização
    areas_interesse: List[str]

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas de Empreendimento
class EmpreendimentoBase(BaseModel):
    tipo_empreendimento: str  # Corrigir o nome do campo
    descricao_empreendimento: str  # Corrigir o nome do campo
    objetivo: str

    class Config:
        from_attributes = True

class EmpreendimentoCreate(EmpreendimentoBase):
    usuario_id: int

class EmpreendimentoUpdate(EmpreendimentoBase):
    pass  # Todos os campos serão atualizados, você pode customizar se necessário

class Empreendimento(EmpreendimentoBase):
    id: int

# Esquemas de Área de Interesse
class AreaInteresseBase(BaseModel):
    nome: str

    class Config:
        from_attributes = True

class AreaInteresseCreate(AreaInteresseBase):
    pass

class AreaInteresseUpdate(AreaInteresseBase):
    pass

class AreaInteresse(AreaInteresseBase):
    id: int

class ArtigoCreate(BaseModel):
    titulo: str
    conteudo: str
    link: Optional[str] = None

# Schema para retornar um artigo
class ArtigoResponse(BaseModel):
    id: int
    titulo: str
    conteudo: str
    link: Optional[str] = None

    class Config:
        orm_mode = True