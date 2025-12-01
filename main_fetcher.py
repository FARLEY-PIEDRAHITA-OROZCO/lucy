from src.fetcher.rapidapi_client import fetch_leagues
from src.fetcher.save_raw import save_raw
from src.fetcher.config import DEFAULT_COUNTRY, DEFAULT_SEASON

def run_fetcher():
    data = fetch_leagues(DEFAULT_COUNTRY, DEFAULT_SEASON)
    save_raw(data, "leagues")

if __name__ == "__main__":
    run_fetcher()
