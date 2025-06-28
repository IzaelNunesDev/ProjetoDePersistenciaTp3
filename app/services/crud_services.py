from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from passlib.context import CryptContext

from ..models.pydantic_models import (
    Aluno, AlunoCreate, AlunoUpdate,
    Motorista, MotoristaCreate, MotoristaUpdate,
    Veiculo, VeiculoCreate, VeiculoUpdate,
    Rota, RotaCreate, RotaUpdate,
    Viagem, ViagemCreate, ViagemUpdate,
    Frequencia, FrequenciaCreate, FrequenciaUpdate,
    ViagemDetalhada, PaginatedResponse,
    StatusVeiculo, StatusViagem
)

# Configuração do contexto de senha com bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CRUDService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    # Função auxiliar para hash de senha usando bcrypt
    def _get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    # ==================== ALUNOS ====================
    async def create_aluno(self, aluno: AlunoCreate) -> Aluno:
        """F1: Inserir um aluno"""
        aluno_dict = aluno.model_dump()
        aluno_dict["senha_hash"] = self._get_password_hash(aluno_dict.pop("senha"))
        aluno_dict["_id"] = ObjectId()
        
        await self.db.alunos.insert_one(aluno_dict)
        return Aluno(**aluno_dict)

    async def get_alunos(self, skip: int = 0, limit: int = 100) -> List[Aluno]:
        """F2: Listar todos os alunos"""
        cursor = self.db.alunos.find().skip(skip).limit(limit)
        alunos = await cursor.to_list(length=limit)
        return [Aluno(**aluno) for aluno in alunos]

    async def get_aluno(self, aluno_id: str) -> Optional[Aluno]:
        """F3: Buscar aluno por ID"""
        aluno = await self.db.alunos.find_one({"_id": ObjectId(aluno_id)})
        return Aluno(**aluno) if aluno else None

    async def update_aluno(self, aluno_id: str, aluno_update: AlunoUpdate) -> Optional[Aluno]:
        """F3: Atualizar aluno"""
        update_data = {}
        for field, value in aluno_update.model_dump(exclude_unset=True).items():
            if field == "senha" and value:
                update_data["senha_hash"] = self._get_password_hash(value)
            else:
                update_data[field] = value
        
        if update_data:
            result = await self.db.alunos.update_one(
                {"_id": ObjectId(aluno_id)}, {"$set": update_data}
            )
            if result.modified_count:
                return await self.get_aluno(aluno_id)
        return None

    async def delete_aluno(self, aluno_id: str) -> bool:
        """F3: Deletar aluno"""
        result = await self.db.alunos.delete_one({"_id": ObjectId(aluno_id)})
        return result.deleted_count > 0

    async def count_alunos(self) -> int:
        """F4: Contar total de alunos"""
        return await self.db.alunos.count_documents({})

    async def search_alunos(self, nome: Optional[str] = None, email: Optional[str] = None) -> List[Aluno]:
        """F6: Buscar alunos por filtros"""
        filter_query = {}
        if nome:
            filter_query["nome_completo"] = {"$regex": nome, "$options": "i"}
        if email:
            filter_query["email"] = {"$regex": email, "$options": "i"}
        
        cursor = self.db.alunos.find(filter_query)
        alunos = await cursor.to_list(length=100)
        return [Aluno(**aluno) for aluno in alunos]

    # ==================== MOTORISTAS ====================
    async def create_motorista(self, motorista: MotoristaCreate) -> Motorista:
        """F1: Inserir um motorista"""
        motorista_dict = motorista.model_dump()
        motorista_dict["senha_hash"] = self._get_password_hash(motorista_dict.pop("senha"))
        motorista_dict["_id"] = ObjectId()
        
        await self.db.motoristas.insert_one(motorista_dict)
        return Motorista(**motorista_dict)

    async def get_motoristas(self, skip: int = 0, limit: int = 100) -> List[Motorista]:
        """F2: Listar todos os motoristas"""
        cursor = self.db.motoristas.find().skip(skip).limit(limit)
        motoristas = await cursor.to_list(length=limit)
        return [Motorista(**motorista) for motorista in motoristas]

    async def get_motorista(self, motorista_id: str) -> Optional[Motorista]:
        """F3: Buscar motorista por ID"""
        motorista = await self.db.motoristas.find_one({"_id": ObjectId(motorista_id)})
        return Motorista(**motorista) if motorista else None

    async def update_motorista(self, motorista_id: str, motorista_update: MotoristaUpdate) -> Optional[Motorista]:
        """F3: Atualizar motorista"""
        update_data = {}
        for field, value in motorista_update.model_dump(exclude_unset=True).items():
            if field == "senha" and value:
                update_data["senha_hash"] = self._get_password_hash(value)
            else:
                update_data[field] = value
        
        if update_data:
            result = await self.db.motoristas.update_one(
                {"_id": ObjectId(motorista_id)}, {"$set": update_data}
            )
            if result.modified_count:
                return await self.get_motorista(motorista_id)
        return None

    async def delete_motorista(self, motorista_id: str) -> bool:
        """F3: Deletar motorista"""
        result = await self.db.motoristas.delete_one({"_id": ObjectId(motorista_id)})
        return result.deleted_count > 0

    async def count_motoristas(self) -> int:
        """F4: Contar total de motoristas"""
        return await self.db.motoristas.count_documents({})

    async def search_motoristas(self, nome: Optional[str] = None, status_ativo: Optional[bool] = None) -> List[Motorista]:
        """F6: Buscar motoristas por filtros"""
        filter_query = {}
        if nome:
            filter_query["nome_completo"] = {"$regex": nome, "$options": "i"}
        if status_ativo is not None:
            filter_query["status_ativo"] = status_ativo
        
        cursor = self.db.motoristas.find(filter_query)
        motoristas = await cursor.to_list(length=100)
        return [Motorista(**motorista) for motorista in motoristas]

    # ==================== VEÍCULOS ====================
    async def create_veiculo(self, veiculo: VeiculoCreate) -> Veiculo:
        """F1: Inserir um veículo"""
        veiculo_dict = veiculo.model_dump()
        veiculo_dict["_id"] = ObjectId()
        
        await self.db.veiculos.insert_one(veiculo_dict)
        return Veiculo(**veiculo_dict)

    async def get_veiculos(self, skip: int = 0, limit: int = 100) -> List[Veiculo]:
        """F2: Listar todos os veículos"""
        cursor = self.db.veiculos.find().skip(skip).limit(limit)
        veiculos = await cursor.to_list(length=limit)
        return [Veiculo(**veiculo) for veiculo in veiculos]

    async def get_veiculo(self, veiculo_id: str) -> Optional[Veiculo]:
        """F3: Buscar veículo por ID"""
        veiculo = await self.db.veiculos.find_one({"_id": ObjectId(veiculo_id)})
        return Veiculo(**veiculo) if veiculo else None

    async def update_veiculo(self, veiculo_id: str, veiculo_update: VeiculoUpdate) -> Optional[Veiculo]:
        """F3: Atualizar veículo"""
        update_data = {k: v for k, v in veiculo_update.model_dump(exclude_unset=True).items()}
        
        if update_data:
            result = await self.db.veiculos.update_one(
                {"_id": ObjectId(veiculo_id)}, {"$set": update_data}
            )
            if result.modified_count:
                return await self.get_veiculo(veiculo_id)
        return None

    async def delete_veiculo(self, veiculo_id: str) -> bool:
        """F3: Deletar veículo"""
        result = await self.db.veiculos.delete_one({"_id": ObjectId(veiculo_id)})
        return result.deleted_count > 0

    async def count_veiculos(self) -> int:
        """F4: Contar total de veículos"""
        return await self.db.veiculos.count_documents({})

    async def search_veiculos(self, 
                            status_manutencao: Optional[StatusVeiculo] = None,
                            adaptado_pcd: Optional[bool] = None,
                            ano_fabricacao: Optional[int] = None) -> List[Veiculo]:
        """F6: Buscar veículos por filtros"""
        filter_query = {}
        if status_manutencao:
            filter_query["status_manutencao"] = status_manutencao
        if adaptado_pcd is not None:
            filter_query["adaptado_pcd"] = adaptado_pcd
        if ano_fabricacao:
            filter_query["ano_fabricacao"] = ano_fabricacao
        
        cursor = self.db.veiculos.find(filter_query)
        veiculos = await cursor.to_list(length=100)
        return [Veiculo(**veiculo) for veiculo in veiculos]

    # ==================== ROTAS ====================
    async def create_rota(self, rota: RotaCreate) -> Rota:
        """F1: Inserir uma rota"""
        rota_dict = rota.model_dump()
        rota_dict["_id"] = ObjectId()
        
        await self.db.rotas.insert_one(rota_dict)
        return Rota(**rota_dict)

    async def get_rotas(self, skip: int = 0, limit: int = 100) -> List[Rota]:
        """F2: Listar todas as rotas"""
        cursor = self.db.rotas.find().skip(skip).limit(limit)
        rotas = await cursor.to_list(length=limit)
        return [Rota(**rota) for rota in rotas]

    async def get_rota(self, rota_id: str) -> Optional[Rota]:
        """F3: Buscar rota por ID"""
        rota = await self.db.rotas.find_one({"_id": ObjectId(rota_id)})
        return Rota(**rota) if rota else None

    async def update_rota(self, rota_id: str, rota_update: RotaUpdate) -> Optional[Rota]:
        """F3: Atualizar rota"""
        update_data = {k: v for k, v in rota_update.model_dump(exclude_unset=True).items()}
        
        if update_data:
            result = await self.db.rotas.update_one(
                {"_id": ObjectId(rota_id)}, {"$set": update_data}
            )
            if result.modified_count:
                return await self.get_rota(rota_id)
        return None

    async def delete_rota(self, rota_id: str) -> bool:
        """F3: Deletar rota"""
        result = await self.db.rotas.delete_one({"_id": ObjectId(rota_id)})
        return result.deleted_count > 0

    async def count_rotas(self) -> int:
        """F4: Contar total de rotas"""
        return await self.db.rotas.count_documents({})

    async def search_rotas(self, 
                          nome: Optional[str] = None, 
                          descricao: Optional[str] = None,
                          turno: Optional[str] = None,
                          ativa: Optional[bool] = None) -> List[Rota]:
        """F6: Buscar rotas por filtros"""
        filter_query = {}
        if nome:
            filter_query["nome_rota"] = {"$regex": nome, "$options": "i"}
        if descricao:
            filter_query["descricao"] = {"$regex": descricao, "$options": "i"}
        if turno:
            filter_query["turno"] = {"$regex": turno, "$options": "i"}
        if ativa is not None:
            filter_query["ativa"] = ativa
        
        cursor = self.db.rotas.find(filter_query)
        rotas = await cursor.to_list(length=100)
        return [Rota(**rota) for rota in rotas]

    # ==================== VIAGENS ====================
    async def create_viagem(self, viagem: ViagemCreate) -> Viagem:
        """F1: Inserir uma viagem"""
        viagem_dict = viagem.model_dump()
        viagem_dict["_id"] = ObjectId()
        
        await self.db.viagens.insert_one(viagem_dict)
        return Viagem(**viagem_dict)

    async def get_viagens(self, skip: int = 0, limit: int = 100) -> List[Viagem]:
        """F2: Listar todas as viagens"""
        cursor = self.db.viagens.find().skip(skip).limit(limit)
        viagens = await cursor.to_list(length=limit)
        return [Viagem(**viagem) for viagem in viagens]

    async def get_viagem(self, viagem_id: str) -> Optional[Viagem]:
        """F3: Buscar viagem por ID"""
        viagem = await self.db.viagens.find_one({"_id": ObjectId(viagem_id)})
        return Viagem(**viagem) if viagem else None

    async def update_viagem(self, viagem_id: str, viagem_update: ViagemUpdate) -> Optional[Viagem]:
        """F3: Atualizar viagem"""
        update_data = {k: v for k, v in viagem_update.model_dump(exclude_unset=True).items()}
        
        if update_data:
            result = await self.db.viagens.update_one(
                {"_id": ObjectId(viagem_id)}, {"$set": update_data}
            )
            if result.modified_count:
                return await self.get_viagem(viagem_id)
        return None

    async def delete_viagem(self, viagem_id: str) -> bool:
        """F3: Deletar viagem"""
        result = await self.db.viagens.delete_one({"_id": ObjectId(viagem_id)})
        return result.deleted_count > 0

    async def count_viagens(self) -> int:
        """F4: Contar total de viagens"""
        return await self.db.viagens.count_documents({})

    async def search_viagens(self,
                           status: Optional[StatusViagem] = None,
                           data_inicio: Optional[date] = None,
                           data_fim: Optional[date] = None,
                           motorista_id: Optional[str] = None,
                           rota_id: Optional[str] = None) -> List[Viagem]:
        """F6: Buscar viagens por filtros"""
        filter_query = {}
        if status:
            filter_query["status"] = status
        if data_inicio or data_fim:
            date_filter = {}
            if data_inicio:
                date_filter["$gte"] = data_inicio
            if data_fim:
                date_filter["$lte"] = data_fim
            filter_query["data_viagem"] = date_filter
        if motorista_id:
            filter_query["motorista_id"] = ObjectId(motorista_id)
        if rota_id:
            filter_query["rota_id"] = ObjectId(rota_id)
        
        cursor = self.db.viagens.find(filter_query)
        viagens = await cursor.to_list(length=100)
        return [Viagem(**viagem) for viagem in viagens]

    async def get_viagem_detalhada(self, viagem_id: str) -> Optional[ViagemDetalhada]:
        """F7: Buscar viagem com informações relacionadas"""
        pipeline = [
            {"$match": {"_id": ObjectId(viagem_id)}},
            {"$lookup": {
                "from": "rotas",
                "localField": "rota_id",
                "foreignField": "_id",
                "as": "rota_info"
            }},
            {"$lookup": {
                "from": "motoristas",
                "localField": "motorista_id",
                "foreignField": "_id",
                "as": "motorista_info"
            }},
            {"$lookup": {
                "from": "veiculos",
                "localField": "veiculo_id",
                "foreignField": "_id",
                "as": "veiculo_info"
            }},
            {"$unwind": "$rota_info"},
            {"$unwind": "$motorista_info"},
            {"$unwind": "$veiculo_info"},
            {"$project": {
                "_id": 1,
                "data_viagem": 1,
                "status": 1,
                "incidentes": 1,
                "rota_info": 1,
                "motorista_info": 1,
                "veiculo_info": 1
            }}
        ]
        
        result = await self.db.viagens.aggregate(pipeline).to_list(length=1)
        if result:
            return ViagemDetalhada(**result[0])
        return None

    async def get_alunos_viagem(self, viagem_id: str) -> List[Aluno]:
        """F8: Buscar alunos de uma viagem específica"""
        pipeline = [
            {"$match": {"viagem_id": ObjectId(viagem_id)}},
            {"$lookup": {
                "from": "alunos",
                "localField": "aluno_id",
                "foreignField": "_id",
                "as": "aluno_info"
            }},
            {"$unwind": "$aluno_info"},
            {"$replaceRoot": {"newRoot": "$aluno_info"}}
        ]
        
        alunos = await self.db.frequencias.aggregate(pipeline).to_list(length=100)
        return [Aluno(**aluno) for aluno in alunos]

    async def get_viagens_por_periodo(self, data_inicio: date, data_fim: date) -> List[Dict[str, Any]]:
        """F9: Relatório de viagens por período"""
        pipeline = [
            {"$match": {
                "data_viagem": {"$gte": data_inicio, "$lte": data_fim}
            }},
            {"$lookup": {
                "from": "rotas",
                "localField": "rota_id",
                "foreignField": "_id",
                "as": "rota_info"
            }},
            {"$lookup": {
                "from": "motoristas",
                "localField": "motorista_id",
                "foreignField": "_id",
                "as": "motorista_info"
            }},
            {"$lookup": {
                "from": "veiculos",
                "localField": "veiculo_id",
                "foreignField": "_id",
                "as": "veiculo_info"
            }},
            {"$unwind": "$rota_info"},
            {"$unwind": "$motorista_info"},
            {"$unwind": "$veiculo_info"},
            {"$project": {
                "_id": 1,
                "data_viagem": 1,
                "status": 1,
                "rota_nome": "$rota_info.nome_rota",
                "motorista_nome": "$motorista_info.nome_completo",
                "veiculo_placa": "$veiculo_info.placa",
                "incidentes_count": {"$size": "$incidentes"}
            }}
        ]
        
        return await self.db.viagens.aggregate(pipeline).to_list(length=100)

    async def get_estatisticas_veiculos(self) -> List[Dict[str, Any]]:
        """F10: Estatísticas de uso de veículos"""
        pipeline = [
            {"$lookup": {
                "from": "veiculos",
                "localField": "veiculo_id",
                "foreignField": "_id",
                "as": "veiculo_info"
            }},
            {"$unwind": "$veiculo_info"},
            {"$group": {
                "_id": "$veiculo_id",
                "placa": {"$first": "$veiculo_info.placa"},
                "modelo": {"$first": "$veiculo_info.modelo"},
                "total_viagens": {"$sum": 1},
                "viagens_concluidas": {
                    "$sum": {"$cond": [{"$eq": ["$status", StatusViagem.CONCLUIDA]}, 1, 0]}
                },
                "viagens_canceladas": {
                    "$sum": {"$cond": [{"$eq": ["$status", StatusViagem.CANCELADA]}, 1, 0]}
                }
            }},
            {"$project": {
                "_id": 1,
                "placa": 1,
                "modelo": 1,
                "total_viagens": 1,
                "viagens_concluidas": 1,
                "viagens_canceladas": 1,
                "taxa_conclusao": {
                    "$cond": [
                        {"$eq": ["$total_viagens", 0]},
                        0,
                        {"$divide": ["$viagens_concluidas", "$total_viagens"]}
                    ]
                }
            }}
        ]
        
        return await self.db.viagens.aggregate(pipeline).to_list(length=100)

    # ==================== FREQUÊNCIAS ====================
    async def create_frequencia(self, frequencia: FrequenciaCreate) -> Frequencia:
        """F1: Inserir uma frequência"""
        frequencia_dict = frequencia.model_dump()
        frequencia_dict["_id"] = ObjectId()
        
        await self.db.frequencias.insert_one(frequencia_dict)
        return Frequencia(**frequencia_dict)

    async def get_frequencias(self, skip: int = 0, limit: int = 100) -> List[Frequencia]:
        """F2: Listar todas as frequências"""
        cursor = self.db.frequencias.find().skip(skip).limit(limit)
        frequencias = await cursor.to_list(length=limit)
        return [Frequencia(**frequencia) for frequencia in frequencias]

    async def get_frequencia(self, frequencia_id: str) -> Optional[Frequencia]:
        """F3: Buscar frequência por ID"""
        frequencia = await self.db.frequencias.find_one({"_id": ObjectId(frequencia_id)})
        return Frequencia(**frequencia) if frequencia else None

    async def update_frequencia(self, frequencia_id: str, frequencia_update: FrequenciaUpdate) -> Optional[Frequencia]:
        """F3: Atualizar frequência"""
        update_data = {k: v for k, v in frequencia_update.model_dump(exclude_unset=True).items()}
        
        if update_data:
            result = await self.db.frequencias.update_one(
                {"_id": ObjectId(frequencia_id)}, {"$set": update_data}
            )
            if result.modified_count:
                return await self.get_frequencia(frequencia_id)
        return None

    async def delete_frequencia(self, frequencia_id: str) -> bool:
        """F3: Deletar frequência"""
        result = await self.db.frequencias.delete_one({"_id": ObjectId(frequencia_id)})
        return result.deleted_count > 0

    async def count_frequencias(self) -> int:
        """F4: Contar total de frequências"""
        return await self.db.frequencias.count_documents({})

    # ==================== PAGINAÇÃO GENÉRICA ====================
    async def get_paginated(self, collection_name: str, page: int = 0, limit: int = 10, 
                           filter_query: Optional[Dict] = None) -> PaginatedResponse:
        """F5: Paginação genérica para qualquer coleção"""
        if filter_query is None:
            filter_query = {}
        
        total = await self.db[collection_name].count_documents(filter_query)
        skip = page * limit
        
        cursor = self.db[collection_name].find(filter_query).skip(skip).limit(limit)
        items = await cursor.to_list(length=limit)
        
        pages = (total + limit - 1) // limit
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages=pages
        ) 