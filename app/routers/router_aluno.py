from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Any
from bson import ObjectId

from ..database import get_database
from ..models.pydantic_models import (
    Aluno, AlunoCreate, AlunoUpdate, PaginatedResponse
)
from ..services.crud_services import CRUDService

router = APIRouter(prefix="/alunos", tags=["Alunos"])

def get_crud_service(db: Any = Depends(get_database)) -> CRUDService:
    return CRUDService(db)

# F1: Inserir uma entidade
@router.post("/", response_model=Aluno, status_code=201)
async def criar_aluno(
    aluno: AlunoCreate,
    crud: CRUDService = Depends(get_crud_service)
):
    """Criar um novo aluno"""
    try:
        return await crud.create_aluno(aluno)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar aluno: {str(e)}")

# F2: Listar todas as entidades
@router.get("/", response_model=List[Aluno])
async def listar_alunos(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar todos os alunos"""
    return await crud.get_alunos()

# F3: CRUD completo - GET por ID
@router.get("/{aluno_id}", response_model=Aluno)
async def obter_aluno(
    aluno_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Obter um aluno específico por ID"""
    aluno = await crud.get_aluno(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

# F3: CRUD completo - PUT (atualizar)
@router.put("/{aluno_id}", response_model=Aluno)
async def atualizar_aluno(
    aluno_id: str,
    aluno_update: AlunoUpdate,
    crud: CRUDService = Depends(get_crud_service)
):
    """Atualizar um aluno"""
    aluno = await crud.update_aluno(aluno_id, aluno_update)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

# F3: CRUD completo - DELETE
@router.delete("/{aluno_id}")
async def deletar_aluno(
    aluno_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Deletar um aluno"""
    success = await crud.delete_aluno(aluno_id)
    if not success:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"message": "Aluno deletado com sucesso"}

# F4: Mostrar quantidade de entidades
@router.get("/quantidade/total")
async def contar_alunos(
    crud: CRUDService = Depends(get_crud_service)
):
    """Contar total de alunos"""
    total = await crud.count_alunos()
    return {"total_alunos": total}

# F5: Implementar paginação
@router.get("/pagina/", response_model=PaginatedResponse)
async def listar_alunos_paginados(
    page: int = Query(0, ge=0, description="Número da página (começa em 0)"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar alunos com paginação"""
    return await crud.get_paginated("alunos", page, limit)

# F6: Filtrar por atributos
@router.get("/buscar/", response_model=List[Aluno])
async def buscar_alunos(
    nome: Optional[str] = Query(None, description="Nome do aluno"),
    email: Optional[str] = Query(None, description="Email do aluno"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Buscar alunos por filtros"""
    return await crud.search_alunos(nome=nome, email=email)

# Busca por texto (nome ou email)
@router.get("/buscar/texto/", response_model=List[Aluno])
async def buscar_alunos_por_texto(
    texto: str = Query(..., min_length=1, description="Texto para buscar em nome ou email"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Buscar alunos por texto no nome ou email"""
    db = crud.db
    
    filter_query = {
        "$or": [
            {"nome_completo": {"$regex": texto, "$options": "i"}},
            {"email": {"$regex": texto, "$options": "i"}}
        ]
    }
    
    cursor = db.alunos.find(filter_query)
    alunos = await cursor.to_list(length=100)
    return [Aluno(**aluno) for aluno in alunos]

# Endpoint adicional: Alunos com necessidades especiais
@router.get("/necessidades-especiais/", response_model=List[Aluno])
async def listar_alunos_necessidades_especiais(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar alunos com necessidades especiais"""
    db = crud.db
    
    filter_query = {
        "necessidade_especial": {"$exists": True, "$ne": None, "$ne": ""}
    }
    
    cursor = db.alunos.find(filter_query)
    alunos = await cursor.to_list(length=100)
    return [Aluno(**aluno) for aluno in alunos]

# Endpoint adicional: Alunos por ponto de embarque preferencial
@router.get("/ponto-embarque/{ponto_id}", response_model=List[Aluno])
async def listar_alunos_por_ponto_embarque(
    ponto_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar alunos por ponto de embarque preferencial"""
    db = crud.db
    
    filter_query = {
        "ponto_embarque_preferencial_id": ObjectId(ponto_id)
    }
    
    cursor = db.alunos.find(filter_query)
    alunos = await cursor.to_list(length=100)
    return [Aluno(**aluno) for aluno in alunos] 