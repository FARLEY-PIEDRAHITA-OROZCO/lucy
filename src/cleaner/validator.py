import sys
import os
from .logger import get_logger

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.common.exceptions import DataValidationError

logger = get_logger()

def validate_dataframe(df):
    """
    Valida la integridad y calidad de los datos.
    
    Args:
        df: DataFrame a validar
        
    Returns:
        DataFrame: DataFrame validado y limpio
        
    Raises:
        DataValidationError: Si los datos no pasan validación
    """
    logger.info("Iniciando validación de datos...")
    
    initial_rows = len(df)
    
    # Validar columnas requeridas
    required_columns = ["league_id", "league_name", "season", "country"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        error_msg = f"Columnas faltantes: {', '.join(missing_columns)}"
        logger.error(f"✗ {error_msg}")
        raise DataValidationError(error_msg)
    
    logger.info("✓ Todas las columnas requeridas presentes")
    
    # Validar valores nulos en campos críticos
    if df["season"].isna().any():
        null_count = df["season"].isna().sum()
        logger.warning(f"Encontradas {null_count} temporadas vacías - eliminando filas")
        df = df.dropna(subset=["season"])
    
    if df["league_id"].isna().any():
        null_count = df["league_id"].isna().sum()
        logger.warning(f"Encontrados {null_count} league_id vacíos - eliminando filas")
        df = df.dropna(subset=["league_id"])
    
    # Validar tipos de datos
    if df["league_id"].dtype not in ["int64", "int32"]:
        logger.warning(f"Convirtiendo league_id de {df['league_id'].dtype} a int")
        df["league_id"] = df["league_id"].astype(int)
    
    logger.info("✓ Tipos de datos correctos")
    
    # Eliminar duplicados
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        logger.info(f"Eliminando {duplicates} registros duplicados")
        df = df.drop_duplicates()
    
    final_rows = len(df)
    rows_removed = initial_rows - final_rows
    
    if rows_removed > 0:
        logger.info(f"Filas removidas en validación: {rows_removed}")
    
    logger.info(f"✓ Validación completada: {final_rows} registros válidos")
    
    return df
