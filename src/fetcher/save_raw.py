import json
import os
from datetime import datetime
from .logger import get_logger

logger = get_logger()

def save_raw(data, name):
    """
    Guarda datos raw en formato JSON.
    
    Args:
        data: Datos a guardar
        name: Nombre base del archivo
    
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

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logger.info(f"✓ Archivo RAW guardado: {filename}")
        
        # Mostrar estadísticas
        file_size = os.path.getsize(filename)
        logger.info(f"  Tamaño: {file_size / 1024:.2f} KB")
        
        return filename

    except Exception as e:
        logger.error(f"✗ Error al guardar archivo RAW: {str(e)}")
        raise
