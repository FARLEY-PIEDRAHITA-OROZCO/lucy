import json
import os
import sys
from datetime import datetime
from .logger import get_logger
from .config import DEFAULT_COUNTRY, DEFAULT_SEASON

# Importar repositorio MongoDB
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.database.repositories import LeagueRepository

logger = get_logger()

def save_raw(data, name, country=None, season=None):
    """
    Guarda datos raw en formato JSON y MongoDB.
    
    Args:
        data: Datos a guardar
        name: Nombre base del archivo
        country: País de los datos (opcional)
        season: Temporada de los datos (opcional)
    
    Returns:
        str: Path del archivo guardado o None si falla
    """
    if data is None:
        logger.warning("No se guardó RAW: data es None")
        return None

    try:
        # Crear directorio si no existe
        os.makedirs("data/raw/", exist_ok=True)

        filename = f"data/raw/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Guardar en archivo JSON
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logger.info(f"✓ Archivo RAW guardado: {filename}")
        
        # Mostrar estadísticas
        file_size = os.path.getsize(filename)
        logger.info(f"  Tamaño: {file_size / 1024:.2f} KB")
        
        # Guardar en MongoDB (si está disponible)
        try:
            repo = LeagueRepository()
            if repo.is_available():
                country = country or DEFAULT_COUNTRY
                season = season or DEFAULT_SEASON
                mongo_id = repo.save_raw(data, country, season)
                if mongo_id:
                    logger.info(f"  MongoDB ID: {mongo_id}")
        except Exception as mongo_error:
            logger.warning(f"MongoDB no disponible: {str(mongo_error)}")
        
        return filename

    except Exception as e:
        logger.error(f"✗ Error al guardar archivo RAW: {str(e)}")
        raise
