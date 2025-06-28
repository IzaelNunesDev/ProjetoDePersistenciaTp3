from motor.motor_asyncio import AsyncIOMotorClient
from .core.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None
    is_connected = False

db = Database()

async def connect_to_mongo():
    """Conecta ao MongoDB usando motor"""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
        # Test the connection
        await db.client.admin.command('ping')
        db.db = db.client[settings.DATABASE_NAME]
        db.is_connected = True
        logger.info(f"Conectado ao MongoDB: {settings.MONGODB_URL}")
        logger.info(f"Database: {settings.DATABASE_NAME}")
    except Exception as e:
        logger.error(f"Erro ao conectar ao MongoDB: {e}")
        db.is_connected = False
        # Don't raise the exception, just log it
        # This allows the app to start even without database connection

async def close_mongo_connection():
    """Fecha a conexão com o MongoDB"""
    if db.client:
        db.client.close()
        db.is_connected = False
        logger.info("Conexão com MongoDB fechada")

def get_database():
    """Retorna a instância do banco de dados"""
    if not db.is_connected:
        logger.warning("Tentativa de acessar banco de dados sem conexão")
        return None
    return db.db 