from sqlalchemy.orm import Session
from model.model import Usuario, Empreendimento, AreaInteresse
from schema.schema import UsuarioCreate, UsuarioUpdate, EmpreendimentoCreate, EmpreendimentoUpdate, AreaInteresseCreate, AreaInteresseUpdate
from fastapi import HTTPException
from auth.auth import get_password_hash  # Importar a função para hashear a senha

# Funções de CRUD para Usuários
def create_usuario(db: Session, usuario: UsuarioCreate):
    # Verificar se o nome de usuário já existe
    existing_user = db.query(Usuario).filter(Usuario.nome_usuario == usuario.nome_usuario).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já existe")

    existing_user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já existe")

    # Hashear a senha
    hashed_password = get_password_hash(usuario.senha)
    
    # Criar o novo usuário
    db_usuario = Usuario(
        nome_usuario=usuario.nome_usuario,
        nome_completo=usuario.nome_completo,
        email=usuario.email,
        senha=hashed_password  # Armazenar a senha hasheada
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def update_usuario(db: Session, usuario_id: int, usuario_update: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Atualizar os campos
    db_usuario.nome_usuario = usuario_update.nome_usuario
    db_usuario.nome_completo = usuario_update.nome_completo  # Adicionar nome_completo
    db_usuario.email = usuario_update.email
    
    # Atualizar a senha se fornecida
    if usuario_update.senha:
        db_usuario.senha = get_password_hash(usuario_update.senha)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(db_usuario)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}

# Funções de CRUD para Empreendimentos
def create_empreendimento(db: Session, empreendimento: EmpreendimentoCreate):
    db_empreendimento = Empreendimento(
        tipo_empreeendimento=empreendimento.tipo_empreeendimento,  # Corrigir o nome do campo
        descricao_empreeendimento=empreendimento.descricao_empreeendimento,  # Corrigir o nome do campo
        objetivo=empreendimento.objetivo
    )
    db.add(db_empreendimento)
    db.commit()
    db.refresh(db_empreendimento)
    return db_empreendimento

def get_empreendimento(db: Session, empreendimento_id: int):
    return db.query(Empreendimento).filter(Empreendimento.id == empreendimento_id).first()

def update_empreendimento(db: Session, empreendimento_id: int, empreendimento_update: EmpreendimentoUpdate):
    db_empreendimento = db.query(Empreendimento).filter(Empreendimento.id == empreendimento_id).first()
    if db_empreendimento is None:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    
    # Atualizar os campos
    db_empreendimento.tipo_empreeendimento = empreendimento_update.tipo_empreeendimento
    db_empreendimento.descricao_empreeendimento = empreendimento_update.descricao_empreeendimento
    db_empreendimento.objetivo = empreendimento_update.objetivo
    
    db.commit()
    db.refresh(db_empreendimento)
    return db_empreendimento

def delete_empreendimento(db: Session, empreendimento_id: int):
    db_empreendimento = db.query(Empreendimento).filter(Empreendimento.id == empreendimento_id).first()
    if db_empreendimento is None:
        raise HTTPException(status_code=404, detail="Empreendimento não encontrado")
    db.delete(db_empreendimento)
    db.commit()
    return {"message": "Empreendimento deletado com sucesso"}

# Funções de CRUD para Áreas de Interesse
def create_area_interesse(db: Session, area_interesse: AreaInteresseCreate):
    db_area_interesse = AreaInteresse(
        nome=area_interesse.nome
    )
    db.add(db_area_interesse)
    db.commit()
    db.refresh(db_area_interesse)
    return db_area_interesse

def get_area_interesse(db: Session, area_interesse_id: int):
    return db.query(AreaInteresse).filter(AreaInteresse.id == area_interesse_id).first()

def update_area_interesse(db: Session, area_interesse_id: int, area_interesse_update: AreaInteresseUpdate):
    db_area_interesse = db.query(AreaInteresse).filter(AreaInteresse.id == area_interesse_id).first()
    if db_area_interesse is None:
        raise HTTPException(status_code=404, detail="Área de Interesse não encontrada")
    
    # Atualizar os campos
    db_area_interesse.nome = area_interesse_update.nome
    
    db.commit()
    db.refresh(db_area_interesse)
    return db_area_interesse

def delete_area_interesse(db: Session, area_interesse_id: int):
    db_area_interesse = db.query(AreaInteresse).filter(AreaInteresse.id == area_interesse_id).first()
    if db_area_interesse is None:
        raise HTTPException(status_code=404, detail="Área de Interesse não encontrada")
    db.delete(db_area_interesse)
    db.commit()
    return {"message": f"Área de Interesse {area_interesse_id} deletada com sucesso"}
# crud.py
from sqlalchemy.orm import Session
from model.model import Artigo, ArtigosAreasInteresse, AreaInteresse

# Função para criar um novo artigo
def create_artigo(db: Session, titulo: str, conteudo: str, link: str):
    db_artigo = Artigo(titulo=titulo, conteudo=conteudo, link=link)
    db.add(db_artigo)
    db.commit()
    db.refresh(db_artigo)
    return db_artigo

# Função para associar um artigo a uma área de interesse
def associate_artigo_area_interesse(db: Session, artigo_id: int, area_interesse_id: int):
    db_association = ArtigosAreasInteresse(artigo_id=artigo_id, area_interesse_id=area_interesse_id)
    db.add(db_association)
    db.commit()
    return db_association

# Função para listar todos os artigos
def get_artigos(db: Session):
    return db.query(Artigo).all()

# Função para listar artigos por área de interesse
def get_artigos_por_area_interesse(db: Session, area_interesse_id: int):
    return db.query(Artigo).join(ArtigosAreasInteresse).filter(ArtigosAreasInteresse.area_interesse_id == area_interesse_id).all()