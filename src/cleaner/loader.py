import json
import os
from .logger import get_logger

logger = get_logger()

RAW_DIR = "data/raw"

def load_raw_files():
    """
    Carga todos los archivos JSON del directorio raw.
    
    Returns:
        list: Lista de datasets cargados
        
    Raises:
        FileNotFoundError: Si no existe el directorio o no hay archivos
    """
    if not os.path.exists(RAW_DIR):
        logger.error(f"Directorio {RAW_DIR} no existe")
        raise FileNotFoundError(f"Directorio {RAW_DIR} no encontrado. Ejecuta primero main_fetcher.py")
    
    files = [f for f in os.listdir(RAW_DIR) if f.endswith(".json")]
    
    if not files:
        logger.warning(f"No se encontraron archivos JSON en {RAW_DIR}")
        raise FileNotFoundError(f"No hay archivos para procesar en {RAW_DIR}")
    
    logger.info(f"Encontrados {len(files)} archivos para procesar")
    
    datasets = []

    for file in files:
        path = os.path.join(RAW_DIR, file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                datasets.append(data)
                logger.info(f"✓ Cargado: {file}")
        except json.JSONDecodeError as e:
            logger.error(f"✗ Error al decodificar {file}: {str(e)}")
            continue
        except Exception as e:
            logger.error(f"✗ Error al cargar {file}: {str(e)}")
            continue
    
    logger.info(f"Total datasets cargados exitosamente: {len(datasets)}")
    return datasets
