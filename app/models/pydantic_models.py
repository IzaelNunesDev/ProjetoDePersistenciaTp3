from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from pydantic_core import core_schema
from bson import ObjectId
from typing import Optional, List, Dict, Any, Annotated
from datetime import datetime, date
from enum import Enum
import re

class PyObjectId(ObjectId):
    """
    Custom Pydantic type for MongoDB's ObjectId.
    """
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        """
        Return a Pydantic CoreSchema for ObjectId.
        """
        def validate_from_str(v: str) -> ObjectId:
            if not ObjectId.is_valid(v):
                 raise ValueError("Invalid ObjectId")
            return ObjectId(v)

        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance of ObjectId
                    core_schema.is_instance_schema(ObjectId),
                    # if not, try to validate it from a string
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(),
                            core_schema.no_info_plain_validator_function(validate_from_str),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda x: str(x)),
        )

# Enums para status e tipos
class StatusVeiculo(str, Enum):
    DISPONIVEL = "Disponível"
    EM_MANUTENCAO = "Em Manutenção"
    INATIVO = "Inativo"

class StatusViagem(str, Enum):
    AGENDADA = "Agendada"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDA = "Concluída"
    CANCELADA = "Cancelada"

class TipoIncidente(str, Enum):
    MECANICO = "Mecânico"
    TRAFEGO = "Tráfego"
    CLIMATICO = "Climático"
    OUTRO = "Outro"

class TipoRegistro(str, Enum):
    EMBARQUE = "Embarque"
    DESEMBARQUE = "Desembarque"

# Modelos Base
class BaseDocument(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

# Modelos para Alunos (Usuario + Aluno embutidos)
class AlunoCreate(BaseModel):
    nome_completo: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=100)
    senha: str = Field(..., min_length=6)
    matricula: str = Field(..., min_length=1, max_length=20)
    telefone: Optional[str] = Field(None, max_length=15)
    necessidade_especial: Optional[str] = Field(None, max_length=200)
    ponto_embarque_preferencial_id: Optional[PyObjectId] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Email inválido')
        return v

class AlunoUpdate(BaseModel):
    nome_completo: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    senha: Optional[str] = Field(None, min_length=6)
    matricula: Optional[str] = Field(None, min_length=1, max_length=20)
    telefone: Optional[str] = Field(None, max_length=15)
    necessidade_especial: Optional[str] = Field(None, max_length=200)
    ponto_embarque_preferencial_id: Optional[PyObjectId] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, v):
                raise ValueError('Email inválido')
        return v

class Aluno(BaseDocument):
    nome_completo: str
    email: str
    senha_hash: str
    matricula: str
    telefone: Optional[str] = None
    necessidade_especial: Optional[str] = None
    ponto_embarque_preferencial_id: Optional[PyObjectId] = None

# Modelos para Motoristas (Usuario + Motorista embutidos)
class MotoristaCreate(BaseModel):
    nome_completo: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=100)
    senha: str = Field(..., min_length=6)
    cnh: str = Field(..., min_length=1, max_length=20)
    data_admissao: date
    status_ativo: bool = True

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Email inválido')
        return v

class MotoristaUpdate(BaseModel):
    nome_completo: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    senha: Optional[str] = Field(None, min_length=6)
    cnh: Optional[str] = Field(None, min_length=1, max_length=20)
    data_admissao: Optional[date] = None
    status_ativo: Optional[bool] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, v):
                raise ValueError('Email inválido')
        return v

class Motorista(BaseDocument):
    nome_completo: str
    email: str
    senha_hash: str
    cnh: str
    data_admissao: date
    status_ativo: bool

# Modelos para Veículos
class VeiculoCreate(BaseModel):
    placa: str = Field(..., min_length=1, max_length=10)
    modelo: str = Field(..., min_length=1, max_length=50)
    capacidade_passageiros: int = Field(..., gt=0)
    status_manutencao: StatusVeiculo = StatusVeiculo.DISPONIVEL
    adaptado_pcd: bool = False
    ano_fabricacao: int = Field(..., ge=1900, le=2030)

class VeiculoUpdate(BaseModel):
    placa: Optional[str] = Field(None, min_length=1, max_length=10)
    modelo: Optional[str] = Field(None, min_length=1, max_length=50)
    capacidade_passageiros: Optional[int] = Field(None, gt=0)
    status_manutencao: Optional[StatusVeiculo] = None
    adaptado_pcd: Optional[bool] = None
    ano_fabricacao: Optional[int] = Field(None, ge=1900, le=2030)

class Veiculo(BaseDocument):
    placa: str
    modelo: str
    capacidade_passageiros: int
    status_manutencao: StatusVeiculo
    adaptado_pcd: bool
    ano_fabricacao: int

# Modelos para Pontos de Parada (embutidos em Rota)
class PontoDeParada(BaseModel):
    nome_ponto: str = Field(..., min_length=1, max_length=100)
    endereco: str = Field(..., min_length=1, max_length=200)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    ordem: int = Field(..., ge=1)

# Modelos para Rotas (com Pontos de Parada embutidos)
class RotaCreate(BaseModel):
    nome_rota: str = Field(..., min_length=1, max_length=100)
    descricao: str = Field(..., min_length=1, max_length=500)
    turno: str = Field(..., min_length=1, max_length=20)
    ativa: bool = True
    pontos_de_parada: List[PontoDeParada]

    @field_validator('pontos_de_parada')
    @classmethod
    def validate_pontos_de_parada(cls, v):
        if len(v) < 2:
            raise ValueError('Uma rota deve ter pelo menos 2 pontos de parada')
        return v

class RotaUpdate(BaseModel):
    nome_rota: Optional[str] = Field(None, min_length=1, max_length=100)
    descricao: Optional[str] = Field(None, min_length=1, max_length=500)
    turno: Optional[str] = Field(None, min_length=1, max_length=20)
    ativa: Optional[bool] = None
    pontos_de_parada: Optional[List[PontoDeParada]] = None

    @field_validator('pontos_de_parada')
    @classmethod
    def validate_pontos_de_parada(cls, v):
        if v is not None and len(v) < 2:
            raise ValueError('Uma rota deve ter pelo menos 2 pontos de parada')
        return v

class Rota(BaseDocument):
    nome_rota: str
    descricao: str
    turno: str
    ativa: bool
    pontos_de_parada: List[PontoDeParada]

# Modelos para Incidentes (embutidos em Viagem)
class Incidente(BaseModel):
    descricao: str = Field(..., min_length=1, max_length=500)
    tipo: TipoIncidente
    data_hora: datetime

# Modelos para Viagens
class ViagemCreate(BaseModel):
    data_viagem: date
    status: StatusViagem = StatusViagem.AGENDADA
    rota_id: PyObjectId
    motorista_id: PyObjectId
    veiculo_id: PyObjectId
    incidentes: Optional[List[Incidente]] = []

class ViagemUpdate(BaseModel):
    data_viagem: Optional[date] = None
    status: Optional[StatusViagem] = None
    rota_id: Optional[PyObjectId] = None
    motorista_id: Optional[PyObjectId] = None
    veiculo_id: Optional[PyObjectId] = None
    incidentes: Optional[List[Incidente]] = None

class Viagem(BaseDocument):
    data_viagem: date
    status: StatusViagem
    rota_id: PyObjectId
    motorista_id: PyObjectId
    veiculo_id: PyObjectId
    incidentes: List[Incidente] = []

# Modelos para Frequência
class FrequenciaCreate(BaseModel):
    aluno_id: PyObjectId
    viagem_id: PyObjectId
    data_hora_embarque: datetime
    tipo_registro: TipoRegistro

class FrequenciaUpdate(BaseModel):
    aluno_id: Optional[PyObjectId] = None
    viagem_id: Optional[PyObjectId] = None
    data_hora_embarque: Optional[datetime] = None
    tipo_registro: Optional[TipoRegistro] = None

class Frequencia(BaseDocument):
    aluno_id: PyObjectId
    viagem_id: PyObjectId
    data_hora_embarque: datetime
    tipo_registro: TipoRegistro

# Modelo para Viagem Detalhada (com informações relacionadas)
class ViagemDetalhada(BaseModel):
    id: PyObjectId = Field(alias="_id")
    data_viagem: date
    status: StatusViagem
    rota_info: Rota
    motorista_info: Motorista
    veiculo_info: Veiculo
    incidentes: List[Incidente] = []

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )

# Modelos para Paginação
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int
    pages: int

# Modelos para Filtros
class FiltroVeiculo(BaseModel):
    status_manutencao: Optional[StatusVeiculo] = None
    adaptado_pcd: Optional[bool] = None
    ano_fabricacao: Optional[int] = None

class FiltroViagem(BaseModel):
    status: Optional[StatusViagem] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    motorista_id: Optional[PyObjectId] = None
    rota_id: Optional[PyObjectId] = None

# Modelos para Autenticação
class LoginRequest(BaseModel):
    email: str = Field(..., max_length=100)
    senha: str = Field(..., min_length=1)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Email inválido')
        return v

class UserInfo(BaseModel):
    id: str
    nome: str
    email: str
    tipo: str  # "aluno" ou "motorista"

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_info: UserInfo 