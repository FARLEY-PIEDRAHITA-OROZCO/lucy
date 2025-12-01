import pandas as pd
from src.cleaner.loader import load_raw_files
from src.cleaner.normalizer import normalize_leagues
from src.cleaner.validator import validate_dataframe
from src.cleaner.save_clean import save_clean

def run_cleaner():
    raw_files = load_raw_files()

    all_dfs = []
    for raw_data in raw_files:
        df = normalize_leagues(raw_data)
        df = validate_dataframe(df)
        all_dfs.append(df)

    # Concatenar resultados de todos los archivos RAW
    final_df = pd.concat(all_dfs, ignore_index=True)

    save_clean(final_df)

if __name__ == "__main__":
    run_cleaner()
