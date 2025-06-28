from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Any

from ..database import get_database
from ..models.pydantic_models import (
    Veiculo, VeiculoCreate, VeiculoUpdate, 
    PaginatedResponse, StatusVeiculo
)
from ..services.crud_services import CRUDService

router = APIRouter(prefix="/veiculos", tags=["Veículos"])

def get_crud_service(db: Any = Depends(get_database)) -> CRUDService:
    return CRUDService(db)

# F1: Inserir uma entidade
@router.post("/", response_model=Veiculo, status_code=201)
async def criar_veiculo(
    veiculo: VeiculoCreate,
    crud: CRUDService = Depends(get_crud_service)
):
    """Criar um novo veículo"""
    try:
        return await crud.create_veiculo(veiculo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar veículo: {str(e)}")

# F2: Listar todas as entidades
@router.get("/", response_model=List[Veiculo])
async def listar_veiculos(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar todos os veículos"""
    return await crud.get_veiculos()

# F3: CRUD completo - GET por ID
@router.get("/{veiculo_id}", response_model=Veiculo)
async def obter_veiculo(
    veiculo_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Obter um veículo específico por ID"""
    veiculo = await crud.get_veiculo(veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo

# F3: CRUD completo - PUT (atualizar)
@router.put("/{veiculo_id}", response_model=Veiculo)
async def atualizar_veiculo(
    veiculo_id: str,
    veiculo_update: VeiculoUpdate,
    crud: CRUDService = Depends(get_crud_service)
):
    """Atualizar um veículo"""
    veiculo = await crud.update_veiculo(veiculo_id, veiculo_update)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo

# F3: CRUD completo - DELETE
@router.delete("/{veiculo_id}")
async def deletar_veiculo(
    veiculo_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Deletar um veículo"""
    success = await crud.delete_veiculo(veiculo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return {"message": "Veículo deletado com sucesso"}

# F4: Mostrar quantidade de entidades
@router.get("/quantidade/total")
async def contar_veiculos(
    crud: CRUDService = Depends(get_crud_service)
):
    """Contar total de veículos"""
    total = await crud.count_veiculos()
    return {"total_veiculos": total}

# F5: Implementar paginação
@router.get("/pagina/", response_model=PaginatedResponse)
async def listar_veiculos_paginados(
    page: int = Query(0, ge=0, description="Número da página (começa em 0)"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar veículos com paginação"""
    return await crud.get_paginated("veiculos", page, limit)

# F6: Filtrar por atributos
@router.get("/buscar/", response_model=List[Veiculo])
async def buscar_veiculos(
    status_manutencao: Optional[StatusVeiculo] = Query(None, description="Status de manutenção"),
    adaptado_pcd: Optional[bool] = Query(None, description="Adaptado para PCD"),
    ano_fabricacao: Optional[int] = Query(None, ge=1900, le=2030, description="Ano de fabricação"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Buscar veículos por filtros"""
    return await crud.search_veiculos(
        status_manutencao=status_manutencao,
        adaptado_pcd=adaptado_pcd,
        ano_fabricacao=ano_fabricacao
    )

# Busca por texto (placa ou modelo)
@router.get("/buscar/texto/", response_model=List[Veiculo])
async def buscar_veiculos_por_texto(
    texto: str = Query(..., min_length=1, description="Texto para buscar em placa ou modelo"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Buscar veículos por texto na placa ou modelo"""
    # Implementação usando regex para busca parcial
    db = crud.db
    
    filter_query = {
        "$or": [
            {"placa": {"$regex": texto, "$options": "i"}},
            {"modelo": {"$regex": texto, "$options": "i"}}
        ]
    }
    
    cursor = db.veiculos.find(filter_query)
    veiculos = await cursor.to_list(length=100)
    return [Veiculo(**veiculo) for veiculo in veiculos]

# F7: Consulta complexa - Estatísticas de veículos
@router.get("/estatisticas/")
async def obter_estatisticas_veiculos(
    crud: CRUDService = Depends(get_crud_service)
):
    """Obter estatísticas de uso dos veículos"""
    return await crud.get_estatisticas_veiculos()

# Endpoint adicional: Veículos disponíveis
@router.get("/disponiveis/", response_model=List[Veiculo])
async def listar_veiculos_disponiveis(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar apenas veículos disponíveis"""
    return await crud.search_veiculos(status_manutencao=StatusVeiculo.DISPONIVEL)

# Endpoint adicional: Veículos adaptados para PCD
@router.get("/adaptados-pcd/", response_model=List[Veiculo])
async def listar_veiculos_adaptados_pcd(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar veículos adaptados para PCD"""
    return await crud.search_veiculos(adaptado_pcd=True) 