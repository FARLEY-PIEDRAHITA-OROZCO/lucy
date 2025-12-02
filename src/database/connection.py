"""Gestión de conexión a MongoDB"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

logger = logging.getLogger(__name__)

_client = None
_db = None

def get_db():
    """
    Obtiene la instancia de base de datos MongoDB.
    Implementa patrón Singleton para reutilizar conexión.
    
    Returns:
        Database: Instancia de MongoDB
    """
    global _client, _db
    
    if _db is not None:
        return _db
    
    try:
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        db_name = os.getenv('MONGO_DB_NAME', 'lucy_sports')
        
        logger.info(f"Conectando a MongoDB: {db_name}")
        
        _client = MongoClient(
            mongo_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000
        )
        
        # Verificar conexión
        _client.admin.command('ping')
        
        _db = _client[db_name]
        
        logger.info(f"✓ Conectado a MongoDB: {db_name}")
        
        # Crear índices al conectar
        _create_indexes(_db)
        
        return _db
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Error conectando a MongoDB: {str(e)}")
        logger.warning("Continuando sin MongoDB - solo archivos")
        return None
    except Exception as e:
        logger.error(f"Error inesperado con MongoDB: {str(e)}")
        return None

def _create_indexes(db):
    """Crea índices para optimizar queries"""
    try:
        # Índices para raw_leagues
        db.raw_leagues.create_index('timestamp')
        db.raw_leagues.create_index('country')
        
        # Índices para clean_leagues
        db.clean_leagues.create_index('league_id')
        db.clean_leagues.create_index('season')
        db.clean_leagues.create_index('country')
        db.clean_leagues.create_index([('country', 1), ('season', 1)])
        
        # Índices para fixtures
        db.fixtures.create_index('id_partido', unique=True)
        db.fixtures.create_index('liga_id')
        db.fixtures.create_index('fecha')
        db.fixtures.create_index('id_equipo_local')
        db.fixtures.create_index('id_equipo_visitante')
        db.fixtures.create_index([('liga_id', 1), ('fecha', -1)])
        
        logger.info("✓ Índices creados en MongoDB")
    except Exception as e:
        logger.warning(f"No se pudieron crear índices: {str(e)}")

def close_connection():
    """Cierra la conexión a MongoDB"""
    global _client, _db
    
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("Conexión a MongoDB cerrada")
