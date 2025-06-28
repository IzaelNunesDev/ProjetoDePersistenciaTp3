from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Any, Optional
import bcrypt
from datetime import datetime, timedelta
import jwt
from bson import ObjectId

from ..database import get_database
from ..models.pydantic_models import LoginRequest, LoginResponse, UserInfo

router = APIRouter(prefix="/auth", tags=["Autenticação"])
security = HTTPBasic()

# Chave secreta para JWT (em produção, use uma chave segura)
SECRET_KEY = "rotafacil_secret_key_2024"
ALGORITHM = "HS256"

def get_crud_service(db: Any = Depends(get_database)):
    from ..services.crud_services import CRUDService
    return CRUDService(db)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Criar token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar senha com bcrypt"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    crud = Depends(get_crud_service)
):
    """Login de usuário (aluno ou motorista)"""
    try:
        db = crud.db
        
        # Buscar primeiro como aluno
        aluno = await db.alunos.find_one({"email": login_data.email})
        if aluno:
            if verify_password(login_data.senha, aluno["senha_hash"]):
                # Criar token
                access_token = create_access_token(
                    data={"sub": str(aluno["_id"]), "tipo": "aluno", "email": login_data.email}
                )
                return LoginResponse(
                    access_token=access_token,
                    token_type="bearer",
                    user_info=UserInfo(
                        id=str(aluno["_id"]),
                        nome=aluno["nome_completo"],
                        email=aluno["email"],
                        tipo="aluno"
                    )
                )
        
        # Buscar como motorista
        motorista = await db.motoristas.find_one({"email": login_data.email})
        if motorista:
            if verify_password(login_data.senha, motorista["senha_hash"]):
                # Criar token
                access_token = create_access_token(
                    data={"sub": str(motorista["_id"]), "tipo": "motorista", "email": login_data.email}
                )
                return LoginResponse(
                    access_token=access_token,
                    token_type="bearer",
                    user_info=UserInfo(
                        id=str(motorista["_id"]),
                        nome=motorista["nome_completo"],
                        email=motorista["email"],
                        tipo="motorista"
                    )
                )
        
        # Se chegou aqui, credenciais inválidas
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no login: {str(e)}"
        )

@router.post("/register/aluno", response_model=LoginResponse)
async def register_aluno(
    aluno_data: dict,
    crud = Depends(get_crud_service)
):
    """Registrar novo aluno"""
    try:
        from ..models.pydantic_models import AlunoCreate
        
        # Criar o aluno usando o CRUDService
        aluno_create = AlunoCreate(**aluno_data)
        aluno = await crud.create_aluno(aluno_create)
        
        # Fazer login automático
        login_data = LoginRequest(email=aluno_data["email"], senha=aluno_data["senha"])
        return await login(login_data, crud)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao registrar aluno: {str(e)}"
        )

@router.post("/register/motorista", response_model=LoginResponse)
async def register_motorista(
    motorista_data: dict,
    crud = Depends(get_crud_service)
):
    """Registrar novo motorista"""
    try:
        from ..models.pydantic_models import MotoristaCreate
        
        # Criar o motorista usando o CRUDService
        motorista_create = MotoristaCreate(**motorista_data)
        motorista = await crud.create_motorista(motorista_create)
        
        # Fazer login automático
        login_data = LoginRequest(email=motorista_data["email"], senha=motorista_data["senha"])
        return await login(login_data, crud)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao registrar motorista: {str(e)}"
        )

@router.get("/me", response_model=UserInfo)
async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    crud = Depends(get_crud_service)
):
    """Obter informações do usuário atual"""
    try:
        # Decodificar token JWT
        token = credentials.password  # O token vem como senha no Basic Auth
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id = payload.get("sub")
        user_type = payload.get("tipo")
        
        if not user_id or not user_type:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        db = crud.db
        
        if user_type == "aluno":
            user = await db.alunos.find_one({"_id": ObjectId(user_id)})
        elif user_type == "motorista":
            user = await db.motoristas.find_one({"_id": ObjectId(user_id)})
        else:
            raise HTTPException(status_code=401, detail="Tipo de usuário inválido")
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return UserInfo(
            id=str(user["_id"]),
            nome=user["nome_completo"],
            email=user["email"],
            tipo=user_type
        )
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter usuário: {str(e)}") 