import os
import sys
from datetime import datetime
from .logger import get_logger

# Importar repositorios MongoDB
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.database.repositories import LeagueRepository, FixturesRepository

logger = get_logger()

CLEAN_DIR = "data/clean"

def save_clean(df, name="clean_leagues"):
    """
    Guarda DataFrame limpio en formato CSV y MongoDB.
    
    Args:
        df: DataFrame a guardar
        name: Nombre base del archivo
        
    Returns:
        str: Path del archivo guardado
    """
    try:
        # Crear directorio si no existe
        os.makedirs(CLEAN_DIR, exist_ok=True)
        
        # Agregar timestamp al nombre
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{CLEAN_DIR}/{name}_{timestamp}.csv"
        
        # Guardar CSV
        df.to_csv(filename, index=False, encoding="utf-8")
        
        # Estadísticas
        file_size = os.path.getsize(filename)
        logger.info(f"✓ Archivo limpio guardado: {filename}")
        logger.info(f"  Registros: {len(df)}")
        logger.info(f"  Columnas: {len(df.columns)}")
        logger.info(f"  Tamaño: {file_size / 1024:.2f} KB")
        
        # Guardar en MongoDB (si está disponible)
        try:
            # Detectar si son fixtures o ligas basado en columnas
            is_fixtures = 'id_partido' in df.columns
            
            if is_fixtures:
                repo = FixturesRepository()
                if repo.is_available():
                    logger.info("\nGuardando fixtures en MongoDB...")
                    inserted = repo.save_fixtures_batch(df, batch_size=1000)
                    if inserted > 0:
                        logger.info(f"✓ MongoDB: {inserted} fixtures guardados")
            else:
                repo = LeagueRepository()
                if repo.is_available():
                    logger.info("\nGuardando ligas en MongoDB...")
                    inserted = repo.save_clean_batch(df, batch_size=1000)
                    if inserted > 0:
                        logger.info(f"✓ MongoDB: {inserted} documentos guardados")
        except Exception as mongo_error:
            logger.warning(f"MongoDB no disponible: {str(mongo_error)}")
        
        return filename
        
    except Exception as e:
        logger.error(f"✗ Error al guardar archivo limpio: {str(e)}")
        raise
