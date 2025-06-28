from motor.motor_asyncio import AsyncIOMotorClient
from .core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    """Conecta ao MongoDB usando motor"""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.db = db.client[settings.DATABASE_NAME]
    print(f"Conectado ao MongoDB: {settings.MONGODB_URL}")
    print(f"Database: {settings.DATABASE_NAME}")

async def close_mongo_connection():
    """Fecha a conexão com o MongoDB"""
    if db.client:
        db.client.close()
        print("Conexão com MongoDB fechada")

def get_database():
    """Retorna a instância do banco de dados"""
    return db.db 