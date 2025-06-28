from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Any

from ..database import get_database
from ..models.pydantic_models import (
    Rota, RotaCreate, RotaUpdate, PaginatedResponse
)
from ..services.crud_services import CRUDService

router = APIRouter(prefix="/rotas", tags=["Rotas"])

def get_crud_service(db: Any = Depends(get_database)) -> CRUDService:
    return CRUDService(db)

# F1: Inserir uma entidade
@router.post("/", response_model=Rota, status_code=201)
async def criar_rota(
    rota: RotaCreate,
    crud: CRUDService = Depends(get_crud_service)
):
    """Criar uma nova rota"""
    try:
        return await crud.create_rota(rota)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar rota: {str(e)}")

# F2: Listar todas as entidades
@router.get("/", response_model=List[Rota])
async def listar_rotas(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar todas as rotas"""
    return await crud.get_rotas()

# F3: CRUD completo - GET por ID
@router.get("/{rota_id}", response_model=Rota)
async def obter_rota(
    rota_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Obter uma rota específica por ID"""
    rota = await crud.get_rota(rota_id)
    if not rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return rota

# F3: CRUD completo - PUT (atualizar)
@router.put("/{rota_id}", response_model=Rota)
async def atualizar_rota(
    rota_id: str,
    rota_update: RotaUpdate,
    crud: CRUDService = Depends(get_crud_service)
):
    """Atualizar uma rota"""
    rota = await crud.update_rota(rota_id, rota_update)
    if not rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return rota

# F3: CRUD completo - DELETE
@router.delete("/{rota_id}")
async def deletar_rota(
    rota_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Deletar uma rota"""
    success = await crud.delete_rota(rota_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return {"message": "Rota deletada com sucesso"}

# F4: Mostrar quantidade de entidades
@router.get("/quantidade/total")
async def contar_rotas(
    crud: CRUDService = Depends(get_crud_service)
):
    """Contar total de rotas"""
    total = await crud.count_rotas()
    return {"total_rotas": total}

# F5: Implementar paginação
@router.get("/pagina/", response_model=PaginatedResponse)
async def listar_rotas_paginadas(
    page: int = Query(0, ge=0, description="Número da página (começa em 0)"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar rotas com paginação"""
    return await crud.get_paginated("rotas", page, limit)

# F6: Filtrar por atributos
@router.get("/buscar/", response_model=List[Rota])
async def buscar_rotas(
    nome: Optional[str] = Query(None, description="Nome da rota"),
    descricao: Optional[str] = Query(None, description="Descrição da rota"),
    turno: Optional[str] = Query(None, description="Turno da rota"),
    ativa: Optional[bool] = Query(None, description="Se a rota está ativa"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Buscar rotas por filtros"""
    return await crud.search_rotas(
        nome=nome,
        descricao=descricao,
        turno=turno,
        ativa=ativa
    )

# Busca por texto (nome ou descrição)
@router.get("/buscar/texto/", response_model=List[Rota])
async def buscar_rotas_por_texto(
    texto: str = Query(..., min_length=1, description="Texto para buscar em nome ou descrição"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Buscar rotas por texto no nome ou descrição"""
    db = crud.db
    
    filter_query = {
        "$or": [
            {"nome_rota": {"$regex": texto, "$options": "i"}},
            {"descricao": {"$regex": texto, "$options": "i"}}
        ]
    }
    
    cursor = db.rotas.find(filter_query)
    rotas = await cursor.to_list(length=100)
    return [Rota(**rota) for rota in rotas]

# Endpoint adicional: Rotas ativas
@router.get("/ativas/", response_model=List[Rota])
async def listar_rotas_ativas(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar apenas rotas ativas"""
    return await crud.search_rotas(ativa=True)

# Endpoint adicional: Rotas por turno
@router.get("/turno/{turno}", response_model=List[Rota])
async def listar_rotas_por_turno(
    turno: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar rotas por turno específico"""
    return await crud.search_rotas(turno=turno)

# Endpoint adicional: Rotas com mais pontos de parada
@router.get("/mais-pontos/", response_model=List[Rota])
async def listar_rotas_mais_pontos(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar rotas ordenadas por número de pontos de parada (decrescente)"""
    db = crud.db
    
    pipeline = [
        {"$addFields": {"num_pontos": {"$size": "$pontos_de_parada"}}},
        {"$sort": {"num_pontos": -1}}
    ]
    
    cursor = db.rotas.aggregate(pipeline)
    rotas = await cursor.to_list(length=100)
    return [Rota(**rota) for rota in rotas] 