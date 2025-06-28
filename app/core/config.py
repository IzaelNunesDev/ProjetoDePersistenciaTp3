import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo config.env
load_dotenv("config.env")

class Settings:
    # Configurações do MongoDB (mantidas para compatibilidade)
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "rotafacil")
    
    # Configurações do SQLite
    SQLITE_DATABASE_URL: str = os.getenv("SQLITE_DATABASE_URL", "sqlite:///./rotafacil.db")
    
    # Configurações da API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RotaFácil API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API RESTful para gerenciamento de transporte escolar"
    
    # Configurações de Segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "uma_chave_padrao_apenas_para_dev_nao_usar_em_producao")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24

settings = Settings() 