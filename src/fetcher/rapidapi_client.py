import requests
from .config import API_KEY, BASE_URL
from .logger import get_logger

logger = get_logger()

def fetch_leagues(country, season):
    url = f"{BASE_URL}/leagues"

    headers = {
        "x-apisports-key": API_KEY,
    }

    params = {
        "country": country,
        "season": season
    }

    logger.info(f"Solicitando ligas: país={country}, temporada={season}")

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        logger.error(f"Error API: {response.status_code} - {response.text}")
        return None

    data = response.json()

    logger.info(f"Ligas obtenidas: {len(data.get('response', []))}")

    return data
