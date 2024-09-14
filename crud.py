from sqlalchemy.orm import Session
from model.model import Usuario, Empreendimento, AreaInteresse, Artigo, ArtigosAreasInteresse
from schema.schema import UsuarioCreate, UsuarioUpdate, EmpreendimentoCreate, EmpreendimentoUpdate, AreaInteresseCreate, AreaInteresseUpdate
from fastapi import HTTPException
from typing import List
from auth.auth import get_password_hash

# Função para obter ou criar áreas de interesse
def get_or_create_areas_interesse(db: Session, areas_interesse_nomes: List[str]):
    areas_interesse_ids = []
    for nome in areas_interesse_nomes:
        # Verificar se a área de interesse já existe
        area_interesse = db.query(AreaInteresse).filter(AreaInteresse.nome == nome).first()
        if not area_interesse:
            # Criar a área de interesse se não existir
            new_area_interesse = AreaInteresse(nome=nome)
            db.add(new_area_interesse)
            db.commit()
            db.refresh(new_area_interesse)
            areas_interesse_ids.append(new_area_interesse.id)
        else:
            areas_interesse_ids.append(area_interesse.id)
    return areas_interesse_ids

# Funções de CRUD para Usuários
def create_usuario(db: Session, usuario: UsuarioCreate):
    # Verifica se o email já existe
    db_email = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email já existe")
    
    # Verifica se o nome de usuário já existe
    db_nome = db.query(Usuario).filter(Usuario.nome_usuario == usuario.nome_usuario).first()
    if db_nome:
        raise HTTPException(status_code=400, detail="Nome de usuário já existe")
    
    # Obter ou criar as áreas de interesse
    db_areas_interesse_ids = get_or_create_areas_interesse(db, usuario.areas_interesse)
    
    # Criar o novo usuário, incluindo as áreas de interesse como lista de IDs
    db_usuario = Usuario(
        nome_usuario=usuario.nome_usuario,
        nome_completo=usuario.nome_completo,
        email=usuario.email,
        senha=get_password_hash(usuario.senha),
        areas_interesse=db_areas_interesse_ids  # Armazena a lista de IDs
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario(db: Session, usuario_id: int):
    # Obter o usuário e suas áreas de interesse
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Obter os nomes das áreas de interesse associadas ao usuário
    areas_interesse = db.query(AreaInteresse).filter(AreaInteresse.id.in_(db_usuario.areas_interesse)).all()
    areas_interesse_nomes = [area.nome for area in areas_interesse]
    
    # Adicionar as áreas de interesse ao objeto de resposta
    db_usuario.areas_interesse = areas_interesse_nomes
    return db_usuario

def get_areas_interesse_usuario(db: Session, usuario_id: int):
    # Buscar o usuário pelo ID
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Pegar os IDs das áreas de interesse do usuário
    areas_interesse_ids = usuario.areas_interesse

    if not areas_interesse_ids:
        return []

    # Buscar as áreas de interesse pelo ID
    areas_interesse = db.query(AreaInteresse).filter(AreaInteresse.id.in_(areas_interesse_ids)).all()

    return areas_interesse

def update_usuario(db: Session, usuario_id: int, usuario_update: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Atualizar os campos
    db_usuario.nome_usuario = usuario_update.nome_usuario
    db_usuario.nome_completo = usuario_update.nome_completo
    db_usuario.email = usuario_update.email
    
    # Atualizar as áreas de interesse
    db_areas_interesse_ids = get_or_create_areas_interesse(db, usuario_update.areas_interesse)
    db_usuario.areas_interesse = db_areas_interesse_ids
    
    # Atualizar a senha se fornecida
    if usuario_update.senha:
        db_usuario.senha = get_password_hash(usuario_update.senha)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    # Remover todos os empreendimentos associados ao usuário
    db.query(Empreendimento).filter(Empreendimento.usuario_id == usuario_id).delete()
    
    # Agora, deletar o usuário
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(db_usuario)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}

# Funções de CRUD para Empreendimentos
def create_empreendimento(db: Session, empreendimento: EmpreendimentoCreate):
    db_empreendimento = Empreendimento(
        tipo_empreendimento=empreendimento.tipo_empreendimento,
        descricao_empreendimento=empreendimento.descricao_empreendimento,
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
    db_empreendimento.tipo_empreendimento = empreendimento_update.tipo_empreendimento
    db_empreendimento.descricao_empreendimento = empreendimento_update.descricao_empreendimento
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
    db_area_interesse = AreaInteresse(nome=area_interesse.nome)
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
    return {"message": "Área de Interesse deletada com sucesso"}

# Funções de CRUD para Artigos
def create_artigo(db: Session, titulo: str, conteudo: str, link: str):
    db_artigo = Artigo(titulo=titulo, conteudo=conteudo, link=link)
    db.add(db_artigo)
    db.commit()
    db.refresh(db_artigo)
    return db_artigo

def associate_artigo_area_interesse(db: Session, artigo_id: int, area_interesse_id: int):
    db_association = ArtigosAreasInteresse(artigo_id=artigo_id, area_interesse_id=area_interesse_id)
    db.add(db_association)
    db.commit()
    return db_association

def get_artigos(db: Session):
    return db.query(Artigo).all()

def get_artigos_por_area_interesse(db: Session, area_interesse_id: int):
    return db.query(Artigo).join(ArtigosAreasInteresse).filter(ArtigosAreasInteresse.area_interesse_id == area_interesse_id).all()