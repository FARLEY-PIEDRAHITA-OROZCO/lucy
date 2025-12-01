from main_fetcher import run_fetcher
from main_cleaner import run_cleaner

def run_pipeline():
    print("\n=== LUCY PIPELINE: EXTRACCIÓN + LIMPIEZA ===\n")

    print("[1/2] Ejecutando Paso 1: Extracción de datos...")
    run_fetcher()

    print("[2/2] Ejecutando Paso 2: Limpieza de datos...")
    run_cleaner()

    print("\n=== PIPELINE FINALIZADO EXITOSAMENTE ===")

if __name__ == "__main__":
    run_pipeline()
