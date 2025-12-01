import sys
import logging
from datetime import datetime
from main_fetcher import run_fetcher
from main_cleaner import run_cleaner

# Configurar logger del pipeline
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pipeline")

def run_pipeline():
    """
    Ejecuta el pipeline completo de ETL.
    
    Returns:
        bool: True si todo fue exitoso, False en caso contrario
    """
    start_time = datetime.now()
    
    print("\n" + "=" * 70)
    print("🚀 LUCY PIPELINE: EXTRACCIÓN + LIMPIEZA + TRANSFORMACIÓN")
    print("=" * 70)
    print(f"Inicio: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        # PASO 1: Extracción
        print("\n" + "-" * 70)
        print("📥 [1/2] PASO 1: EXTRACCIÓN DE DATOS")
        print("-" * 70)
        
        fetcher_success = run_fetcher()
        
        if not fetcher_success:
            logger.error("❌ Extracción falló - abortando pipeline")
            return False
        
        print("\n✅ Extracción completada\n")

        # PASO 2: Limpieza
        print("-" * 70)
        print("🧹 [2/2] PASO 2: LIMPIEZA Y NORMALIZACIÓN")
        print("-" * 70)
        
        cleaner_success = run_cleaner()
        
        if not cleaner_success:
            logger.error("❌ Limpieza falló")
            return False
        
        print("\n✅ Limpieza completada\n")

        # Resumen final
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("=" * 70)
        print("✅ PIPELINE FINALIZADO EXITOSAMENTE")
        print("=" * 70)
        print(f"Duración total: {duration:.2f} segundos")
        print(f"Fin: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70 + "\n")
        
        return True
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Pipeline interrumpido por el usuario")
        return False
        
    except Exception as e:
        logger.error(f"\n❌ Error inesperado en pipeline: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
