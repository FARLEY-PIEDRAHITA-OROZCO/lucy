"""Script para extraer fixtures de una liga específica"""
import sys
import os
from src.fetcher.fixtures_client import fetch_fixtures
from src.fetcher.save_raw import save_raw
from src.fetcher.logger import get_logger
from src.common.exceptions import APIConnectionError, APIResponseError

logger = get_logger("fixtures_fetcher")

def run_fixtures_fetcher(league_id, season):
    """
    Ejecuta extracción de fixtures.
    
    Args:
        league_id: ID de la liga
        season: Temporada
        
    Returns:
        bool: True si fue exitoso
    """
    try:
        logger.info("="*60)
        logger.info("INICIANDO EXTRACCIÓN DE FIXTURES")
        logger.info("="*60)
        logger.info(f"Liga: {league_id}, Temporada: {season}")
        
        # Extraer datos
        data = fetch_fixtures(league_id, season)
        
        if data is None:
            logger.error("No se obtuvieron datos")
            return False
        
        # Guardar datos raw
        filename = save_raw(data, f"fixtures_{league_id}_{season}", country=f"league_{league_id}", season=season)
        
        if filename:
            logger.info("="*60)
            logger.info("✓ EXTRACCIÓN DE FIXTURES COMPLETADA")
            logger.info("="*60)
            return True
        else:
            logger.error("Error al guardar datos")
            return False
            
    except APIConnectionError as e:
        logger.error(f"Error de conexión: {str(e)}")
        return False
        
    except APIResponseError as e:
        logger.error(f"Error en respuesta: {str(e)}")
        return False
        
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Ejemplo: Liga 131 (Primera B Metropolitana Argentina), Temporada 2023
    if len(sys.argv) >= 3:
        league_id = int(sys.argv[1])
        season = int(sys.argv[2])
    else:
        # Por defecto: Primera B Metropolitana
        league_id = 131
        season = 2023
        print(f"\nUsando valores por defecto: Liga {league_id}, Temporada {season}")
        print("Uso: python main_fixtures_fetcher.py <league_id> <season>\n")
    
    success = run_fixtures_fetcher(league_id, season)
    sys.exit(0 if success else 1)
