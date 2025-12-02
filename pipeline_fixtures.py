"""Pipeline completo para fixtures"""
import sys
import logging
from datetime import datetime
from main_fixtures_fetcher import run_fixtures_fetcher
from main_fixtures_cleaner import run_fixtures_cleaner

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pipeline_fixtures")

def run_fixtures_pipeline(league_id=131, season=2023):
    """
    Ejecuta pipeline completo de fixtures.
    
    Args:
        league_id: ID de la liga
        season: Temporada
        
    Returns:
        bool: True si fue exitoso
    """
    start_time = datetime.now()
    
    print("\n" + "="*70)
    print(f"🏆 LUCY FIXTURES PIPELINE - Liga {league_id}, Temporada {season}")
    print("="*70)
    print(f"Inicio: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        # PASO 1: Extracción
        print("\n" + "-"*70)
        print("📊 [1/2] PASO 1: EXTRACCIÓN DE FIXTURES")
        print("-"*70)
        
        fetcher_success = run_fixtures_fetcher(league_id, season)
        
        if not fetcher_success:
            logger.error("❌ Extracción falló")
            return False
        
        print("\n✅ Extracción completada\n")

        # PASO 2: Limpieza
        print("-"*70)
        print("🧹 [2/2] PASO 2: LIMPIEZA Y NORMALIZACIÓN")
        print("-"*70)
        
        cleaner_success = run_fixtures_cleaner()
        
        if not cleaner_success:
            logger.error("❌ Limpieza falló")
            return False
        
        print("\n✅ Limpieza completada\n")

        # Resumen
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("="*70)
        print("✅ FIXTURES PIPELINE FINALIZADO EXITOSAMENTE")
        print("="*70)
        print(f"Duración total: {duration:.2f} segundos")
        print(f"Fin: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        return True
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Pipeline interrumpido")
        return False
        
    except Exception as e:
        logger.error(f"\n❌ Error en pipeline: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Obtener parámetros de línea de comandos
    if len(sys.argv) >= 3:
        league_id = int(sys.argv[1])
        season = int(sys.argv[2])
    else:
        # Por defecto: Primera B Metropolitana Argentina
        league_id = 131
        season = 2023
        print(f"\nUsando valores por defecto: Liga {league_id}, Temporada {season}")
        print("Uso: python pipeline_fixtures.py <league_id> <season>\n")
    
    success = run_fixtures_pipeline(league_id, season)
    sys.exit(0 if success else 1)
