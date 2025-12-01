import os

CLEAN_DIR = "data/clean"

def save_clean(df, name="clean_leagues"):
    os.makedirs(CLEAN_DIR, exist_ok=True)
    df.to_csv(f"{CLEAN_DIR}/{name}.csv", index=False)
