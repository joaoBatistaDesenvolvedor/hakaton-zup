from fastapi import FastAPI
from app.api.v1.endpoints import users, auth, empreendimento, area_interesse
from app.db.session import engine
from app.db.base import Base

# Cria as tabelas no banco, caso ainda não existam
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inclui as rotas
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(empreendimento.router, prefix="/empreendimentos", tags=["empreendimentos"])
app.include_router(area_interesse.router, prefix="/areas-interesse", tags=["areas de interesse"])
