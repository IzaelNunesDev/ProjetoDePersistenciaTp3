from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Any
from datetime import date

from ..database import get_database
from ..models.pydantic_models import (
    Viagem, ViagemCreate, ViagemUpdate, ViagemDetalhada,
    PaginatedResponse, StatusViagem, Aluno
)
from ..services.crud_services import CRUDService

router = APIRouter(prefix="/viagens", tags=["Viagens"])

def get_crud_service(db: Any = Depends(get_database)) -> CRUDService:
    return CRUDService(db)

# F1: Inserir uma entidade
@router.post("/", response_model=Viagem, status_code=201)
async def criar_viagem(
    viagem: ViagemCreate,
    crud: CRUDService = Depends(get_crud_service)
):
    """Criar uma nova viagem"""
    try:
        return await crud.create_viagem(viagem)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar viagem: {str(e)}")

# F2: Listar todas as entidades
@router.get("/", response_model=List[Viagem])
async def listar_viagens(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar todas as viagens"""
    return await crud.get_viagens()

# F4: Mostrar quantidade de entidades
@router.get("/quantidade/total")
async def contar_viagens(
    crud: CRUDService = Depends(get_crud_service)
):
    """Contar total de viagens"""
    total = await crud.count_viagens()
    return {"total_viagens": total}

# F5: Implementar paginação
@router.get("/pagina/", response_model=PaginatedResponse)
async def listar_viagens_paginadas(
    page: int = Query(0, ge=0, description="Número da página (começa em 0)"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar viagens com paginação"""
    return await crud.get_paginated("viagens", page, limit)

# F6: Filtrar por atributos
@router.get("/buscar/", response_model=List[Viagem])
async def buscar_viagens(
    status: Optional[StatusViagem] = Query(None, description="Status da viagem"),
    data_inicio: Optional[date] = Query(None, description="Data de início"),
    data_fim: Optional[date] = Query(None, description="Data de fim"),
    motorista_id: Optional[str] = Query(None, description="ID do motorista"),
    rota_id: Optional[str] = Query(None, description="ID da rota"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Buscar viagens por filtros"""
    return await crud.search_viagens(
        status=status,
        data_inicio=data_inicio,
        data_fim=data_fim,
        motorista_id=motorista_id,
        rota_id=rota_id
    )

# F7: Consulta complexa 3 - Viagens por período com estatísticas
@router.get("/estatisticas/periodo/")
async def obter_estatisticas_periodo(
    data_inicio: date = Query(..., description="Data de início do período"),
    data_fim: date = Query(..., description="Data de fim do período"),
    crud: CRUDService = Depends(get_crud_service)
):
    """Obter estatísticas de viagens por período"""
    return await crud.get_viagens_por_periodo(data_inicio, data_fim)

# Endpoint adicional: Viagens por status
@router.get("/status/{status}", response_model=List[Viagem])
async def listar_viagens_por_status(
    status: StatusViagem,
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar viagens por status específico"""
    return await crud.search_viagens(status=status)

# Endpoint adicional: Viagens de hoje
@router.get("/hoje/", response_model=List[Viagem])
async def listar_viagens_hoje(
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar viagens agendadas para hoje"""
    hoje = date.today()
    return await crud.search_viagens(data_inicio=hoje, data_fim=hoje)

# Endpoint adicional: Viagens por motorista
@router.get("/motorista/{motorista_id}", response_model=List[Viagem])
async def listar_viagens_por_motorista(
    motorista_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar todas as viagens de um motorista específico"""
    return await crud.search_viagens(motorista_id=motorista_id)

# Endpoint adicional: Viagens por rota
@router.get("/rota/{rota_id}", response_model=List[Viagem])
async def listar_viagens_por_rota(
    rota_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar todas as viagens de uma rota específica"""
    return await crud.search_viagens(rota_id=rota_id)

# Endpoint adicional: Viagens por aluno
@router.get("/aluno/{aluno_id}", response_model=List[Viagem])
async def listar_viagens_por_aluno(
    aluno_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar todas as viagens de um aluno específico"""
    try:
        return await crud.search_viagens_por_aluno(aluno_id)
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail=f"Serviço temporariamente indisponível: {str(e)}"
        )

# F3: CRUD completo - GET por ID (DEVE VIR DEPOIS DAS ROTAS ESPECÍFICAS)
@router.get("/{viagem_id}", response_model=Viagem)
async def obter_viagem(
    viagem_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Obter uma viagem específica por ID"""
    viagem = await crud.get_viagem(viagem_id)
    if not viagem:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return viagem

# F3: CRUD completo - PUT (atualizar)
@router.put("/{viagem_id}", response_model=Viagem)
async def atualizar_viagem(
    viagem_id: str,
    viagem_update: ViagemUpdate,
    crud: CRUDService = Depends(get_crud_service)
):
    """Atualizar uma viagem"""
    viagem = await crud.update_viagem(viagem_id, viagem_update)
    if not viagem:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return viagem

# F3: CRUD completo - DELETE
@router.delete("/{viagem_id}")
async def deletar_viagem(
    viagem_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Deletar uma viagem"""
    success = await crud.delete_viagem(viagem_id)
    if not success:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return {"message": "Viagem deletada com sucesso"}

# F7: Consulta complexa 1 - Detalhes completos de uma viagem
@router.get("/{viagem_id}/detalhes", response_model=ViagemDetalhada)
async def obter_viagem_detalhada(
    viagem_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Obter detalhes completos de uma viagem com dados do motorista, veículo e rota"""
    viagem_detalhada = await crud.get_viagem_detalhada(viagem_id)
    if not viagem_detalhada:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return viagem_detalhada

# F7: Consulta complexa 2 - Listar todos os alunos de uma viagem específica
@router.get("/{viagem_id}/alunos", response_model=List[Aluno])
async def obter_alunos_viagem(
    viagem_id: str,
    crud: CRUDService = Depends(get_crud_service)
):
    """Listar todos os alunos que embarcaram em uma viagem específica"""
    alunos = await crud.get_alunos_viagem(viagem_id)
    return alunos 