import sys
from src.fetcher.rapidapi_client import fetch_leagues
from src.fetcher.save_raw import save_raw
from src.fetcher.config import DEFAULT_COUNTRY, DEFAULT_SEASON
from src.fetcher.logger import get_logger
from src.common.exceptions import APIConnectionError, APIResponseError

logger = get_logger("main_fetcher")

def run_fetcher():
    """
    Ejecuta el proceso de extracción de datos desde la API.
    
    Returns:
        bool: True si fue exitoso, False en caso contrario
    """
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO EXTRACCIÓN DE DATOS")
        logger.info("=" * 60)
        
        # Extraer datos
        data = fetch_leagues(DEFAULT_COUNTRY, DEFAULT_SEASON)
        
        if data is None:
            logger.error("No se obtuvieron datos de la API")
            return False
        
        # Guardar datos raw
        filename = save_raw(data, "leagues")
        
        if filename:
            logger.info("=" * 60)
            logger.info("✓ EXTRACCIÓN COMPLETADA EXITOSAMENTE")
            logger.info("=" * 60)
            return True
        else:
            logger.error("Error al guardar datos")
            return False
            
    except APIConnectionError as e:
        logger.error(f"Error de conexión: {str(e)}")
        logger.error("Verifica tu conexión a internet y tu API key")
        return False
        
    except APIResponseError as e:
        logger.error(f"Error en respuesta de API: {str(e)}")
        return False
        
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = run_fetcher()
    sys.exit(0 if success else 1)
