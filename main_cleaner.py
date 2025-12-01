import sys
import pandas as pd
from src.cleaner.loader import load_raw_files
from src.cleaner.normalizer import normalize_leagues
from src.cleaner.validator import validate_dataframe
from src.cleaner.save_clean import save_clean
from src.cleaner.logger import get_logger
from src.common.exceptions import DataValidationError, FileProcessingError

logger = get_logger("main_cleaner")

def run_cleaner():
    """
    Ejecuta el proceso de limpieza y normalización de datos.
    
    Returns:
        bool: True si fue exitoso, False en caso contrario
    """
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO LIMPIEZA DE DATOS")
        logger.info("=" * 60)
        
        # Cargar archivos raw
        raw_files = load_raw_files()
        
        if not raw_files:
            logger.error("No hay archivos para procesar")
            return False

        all_dfs = []
        
        # Procesar cada archivo
        for idx, raw_data in enumerate(raw_files, 1):
            logger.info(f"\nProcesando archivo {idx}/{len(raw_files)}")
            
            try:
                # Normalizar
                df = normalize_leagues(raw_data)
                
                if df.empty:
                    logger.warning(f"Archivo {idx} no generó datos - omitiendo")
                    continue
                
                # Validar
                df = validate_dataframe(df)
                
                all_dfs.append(df)
                
            except DataValidationError as e:
                logger.error(f"Error de validación en archivo {idx}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Error procesando archivo {idx}: {str(e)}")
                continue

        if not all_dfs:
            logger.error("No se procesó ningún archivo exitosamente")
            return False

        # Concatenar resultados de todos los archivos RAW
        logger.info("\nConsolidando datos...")
        final_df = pd.concat(all_dfs, ignore_index=True)
        
        # Estadísticas finales
        logger.info(f"\nEstadísticas finales:")
        logger.info(f"  Total registros: {len(final_df)}")
        logger.info(f"  Ligas únicas: {final_df['league_id'].nunique()}")
        logger.info(f"  Países: {final_df['country'].nunique()}")
        logger.info(f"  Temporadas: {sorted(final_df['season'].unique())}")

        # Guardar
        save_clean(final_df)
        
        logger.info("=" * 60)
        logger.info("✓ LIMPIEZA COMPLETADA EXITOSAMENTE")
        logger.info("=" * 60)
        
        return True
        
    except FileNotFoundError as e:
        logger.error(str(e))
        return False
        
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = run_cleaner()
    sys.exit(0 if success else 1)
