import os
from datetime import datetime
from .logger import get_logger

logger = get_logger()

CLEAN_DIR = "data/clean"

def save_clean(df, name="clean_leagues"):
    """
    Guarda DataFrame limpio en formato CSV.
    
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
        
        return filename
        
    except Exception as e:
        logger.error(f"✗ Error al guardar archivo limpio: {str(e)}")
        raise
