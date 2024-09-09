from pydantic import BaseModel

class EmpreendimentoCreate(BaseModel):
    tipo_empreendimento: str
    descricao_empreendimento: str

class Empreendimento(BaseModel):
    id: int
    tipo_empreendimento: str
    descricao_empreendimento: str

    class Config:
        orm_mode = True
