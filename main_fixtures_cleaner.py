"""Script para limpiar y normalizar fixtures"""
import sys
import pandas as pd
from src.cleaner.loader import load_raw_files
from src.cleaner.fixtures_normalizer import normalize_fixtures
from src.cleaner.save_clean import save_clean
from src.cleaner.logger import get_logger
from src.common.exceptions import DataValidationError
import os
import json

logger = get_logger("fixtures_cleaner")

def load_fixtures_raw_files(pattern="fixtures_"):
    """Carga archivos raw de fixtures"""
    RAW_DIR = "data/raw"
    
    if not os.path.exists(RAW_DIR):
        logger.error(f"Directorio {RAW_DIR} no existe")
        raise FileNotFoundError(f"Directorio {RAW_DIR} no encontrado")
    
    files = [f for f in os.listdir(RAW_DIR) if f.endswith(".json") and pattern in f]
    
    if not files:
        logger.warning(f"No se encontraron archivos de fixtures en {RAW_DIR}")
        raise FileNotFoundError(f"No hay archivos de fixtures para procesar")
    
    logger.info(f"Encontrados {len(files)} archivos de fixtures")
    
    datasets = []
    for file in files:
        path = os.path.join(RAW_DIR, file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                datasets.append(data)
                logger.info(f"✓ Cargado: {file}")
        except Exception as e:
            logger.error(f"✗ Error al cargar {file}: {str(e)}")
            continue
    
    logger.info(f"Total datasets de fixtures cargados: {len(datasets)}")
    return datasets

def run_fixtures_cleaner():
    """
    Ejecuta limpieza y normalización de fixtures.
    
    Returns:
        bool: True si fue exitoso
    """
    try:
        logger.info("="*60)
        logger.info("INICIANDO LIMPIEZA DE FIXTURES")
        logger.info("="*60)
        
        # Cargar archivos raw de fixtures
        raw_files = load_fixtures_raw_files()
        
        if not raw_files:
            logger.error("No hay archivos para procesar")
            return False

        all_dfs = []
        
        # Procesar cada archivo
        for idx, raw_data in enumerate(raw_files, 1):
            logger.info(f"\nProcesando archivo {idx}/{len(raw_files)}")
            
            try:
                # Normalizar
                df = normalize_fixtures(raw_data)
                
                if df.empty:
                    logger.warning(f"Archivo {idx} no generó datos")
                    continue
                
                all_dfs.append(df)
                
            except Exception as e:
                logger.error(f"Error en archivo {idx}: {str(e)}")
                continue

        if not all_dfs:
            logger.error("No se procesó ningún archivo exitosamente")
            return False

        # Consolidar
        logger.info("\nConsolidando fixtures...")
        final_df = pd.concat(all_dfs, ignore_index=True)
        
        # Eliminar duplicados
        initial_count = len(final_df)
        final_df = final_df.drop_duplicates(subset=['id_partido'], keep='last')
        duplicates_removed = initial_count - len(final_df)
        
        if duplicates_removed > 0:
            logger.info(f"Duplicados eliminados: {duplicates_removed}")
        
        # Estadísticas
        logger.info(f"\nEstadísticas finales:")
        logger.info(f"  Total fixtures: {len(final_df)}")
        logger.info(f"  Ligas: {final_df['liga_id'].nunique()}")
        logger.info(f"  Estados: {final_df['estado_del_partido'].unique().tolist()}")
        logger.info(f"  Rango de fechas: {final_df['fecha'].min()} a {final_df['fecha'].max()}")

        # Guardar
        save_clean(final_df, name="fixtures_clean")
        
        logger.info("="*60)
        logger.info("✓ LIMPIEZA DE FIXTURES COMPLETADA")
        logger.info("="*60)
        
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
    success = run_fixtures_cleaner()
    sys.exit(0 if success else 1)
