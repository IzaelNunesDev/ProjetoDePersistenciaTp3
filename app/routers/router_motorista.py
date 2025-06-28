from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Any

from ..database import get_database
from ..models.pydantic_models import (
    Motorista, MotoristaCreate, MotoristaUpdate, PaginatedResponse
)
from ..services.crud_services import CRUDService

router = APIRouter(prefix="/motoristas", tags=["Motoristas"])

def get_crud_service(db: Any = Depends(get_database)) -> CRUDService:
    return CRUDService(db)

# F1: Inserir uma entidade
@router.post("/", response_model=Motorista, status_code=201)
async def criar_motorista(
    motorista: MotoristaCreate,
    crud: CRUDService = Depends(get_crud_service)
):
    """Criar um novo motorista"""
    try:
        return await crud.create_motorista(motorista)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar motorista: {str(e)}")

# F2: Listar todas as entidades
@router.get("/", response_model=List[Motorista])
async def listar_motoristas(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar todos os motoristas"""
    return await crud.get_motoristas()

# F4: Mostrar quantidade de entidades
@router.get("/quantidade/total")
async def contar_motoristas(
    crud: CRUDService = Depends(get_crud_service)
):
    """Contar total de motoristas"""
    total = await crud.count_motoristas()
    return {"total_motoristas": total}

# F5: Implementar paginação
@router.get("/pagina/", response_model=PaginatedResponse)
async def listar_motoristas_paginados(
    page: int = Query(0, ge=0, description="Número da página (começa em 0)"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar motoristas com paginação"""
    return await crud.get_paginated("motoristas", page, limit)

# F6: Filtrar por atributos
@router.get("/buscar/", response_model=List[Motorista])
async def buscar_motoristas(
    nome: Optional[str] = Query(None, description="Nome do motorista"),
    status_ativo: Optional[bool] = Query(None, description="Status ativo"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Buscar motoristas por filtros"""
    return await crud.search_motoristas(nome=nome, status_ativo=status_ativo)

# Busca por texto (nome ou email)
@router.get("/buscar/texto/", response_model=List[Motorista])
async def buscar_motoristas_por_texto(
    texto: str = Query(..., min_length=1, description="Texto para buscar em nome ou email"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Buscar motoristas por texto no nome ou email"""
    db = crud.db
    
    filter_query = {
        "$or": [
            {"nome_completo": {"$regex": texto, "$options": "i"}},
            {"email": {"$regex": texto, "$options": "i"}}
        ]
    }
    
    cursor = db.motoristas.find(filter_query)
    motoristas = await cursor.to_list(length=100)
    return [Motorista(**motorista) for motorista in motoristas]

# Endpoint adicional: Motoristas ativos
@router.get("/ativos/", response_model=List[Motorista])
async def listar_motoristas_ativos(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar apenas motoristas ativos"""
    return await crud.search_motoristas(status_ativo=True)

# Endpoint adicional: Motoristas inativos
@router.get("/inativos/", response_model=List[Motorista])
async def listar_motoristas_inativos(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar apenas motoristas inativos"""
    return await crud.search_motoristas(status_ativo=False)

# F3: CRUD completo - GET por ID (DEVE VIR DEPOIS DAS ROTAS ESPECÍFICAS)
@router.get("/{motorista_id}", response_model=Motorista)
async def obter_motorista(
    motorista_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Obter um motorista específico por ID"""
    motorista = await crud.get_motorista(motorista_id)
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    return motorista

# F3: CRUD completo - PUT (atualizar)
@router.put("/{motorista_id}", response_model=Motorista)
async def atualizar_motorista(
    motorista_id: str,
    motorista_update: MotoristaUpdate,
    crud: CRUDService = Depends(get_crud_service)
):
    """Atualizar um motorista"""
    motorista = await crud.update_motorista(motorista_id, motorista_update)
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    return motorista

# F3: CRUD completo - DELETE
@router.delete("/{motorista_id}")
async def deletar_motorista(
    motorista_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Deletar um motorista"""
    success = await crud.delete_motorista(motorista_id)
    if not success:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    return {"message": "Motorista deletado com sucesso"} 