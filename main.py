from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import (
    router_aluno,
    router_motorista,
    router_veiculo,
    router_rota,
    router_viagem,
    router_auth
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

# Criação da aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos routers
app.include_router(router_auth.router, prefix=settings.API_V1_STR)
app.include_router(router_aluno.router, prefix=settings.API_V1_STR)
app.include_router(router_motorista.router, prefix=settings.API_V1_STR)
app.include_router(router_veiculo.router, prefix=settings.API_V1_STR)
app.include_router(router_rota.router, prefix=settings.API_V1_STR)
app.include_router(router_viagem.router, prefix=settings.API_V1_STR)

# Rota raiz
@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API RotaFácil",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Rota de health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API RotaFácil está funcionando"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 