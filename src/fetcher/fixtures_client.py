"""Cliente para obtener fixtures/partidos de la API"""
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from .config import API_KEY, BASE_URL, MAX_RETRIES, RETRY_DELAY
from .logger import get_logger
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.common.retry import retry_on_failure
from src.common.exceptions import APIConnectionError, APIResponseError

logger = get_logger()

@retry_on_failure(
    max_attempts=MAX_RETRIES, 
    delay=RETRY_DELAY, 
    exceptions=(RequestException, ConnectionError, Timeout)
)
def fetch_fixtures(league_id, season):
    """
    Obtiene fixtures (partidos) de una liga y temporada.
    
    Args:
        league_id: ID de la liga
        season: Temporada (año)
    
    Returns:
        dict: Datos de fixtures en formato JSON
    """
    url = f"{BASE_URL}/fixtures"

    headers = {
        "x-apisports-key": API_KEY,
    }

    params = {
        "league": league_id,
        "season": season
    }

    logger.info(f"Solicitando fixtures: liga={league_id}, temporada={season}")

    try:
        response = requests.get(
            url, 
            headers=headers, 
            params=params,
            timeout=30
        )

        if response.status_code == 401:
            logger.error("Error 401: API key inválida")
            raise APIConnectionError("API key inválida")
        
        if response.status_code == 429:
            logger.error("Error 429: Límite de requests excedido")
            raise APIConnectionError("Límite de API excedido")
        
        if response.status_code != 200:
            logger.error(f"Error API: {response.status_code}")
            raise APIResponseError(f"API retornó status {response.status_code}")

        data = response.json()

        if "response" not in data:
            logger.error("Respuesta sin campo 'response'")
            raise APIResponseError("Formato de respuesta inválido")

        num_fixtures = len(data.get('response', []))
        logger.info(f"✓ Fixtures obtenidos: {num_fixtures}")

        return data

    except Timeout:
        logger.error("Timeout al conectar con la API")
        raise APIConnectionError("Timeout de conexión")
    
    except ConnectionError as e:
        logger.error(f"Error de conexión: {str(e)}")
        raise APIConnectionError(f"Error de conexión: {str(e)}")
    
    except requests.exceptions.JSONDecodeError:
        logger.error("Error al decodificar respuesta JSON")
        raise APIResponseError("Respuesta no válida")

@retry_on_failure(
    max_attempts=MAX_RETRIES, 
    delay=RETRY_DELAY, 
    exceptions=(RequestException, ConnectionError, Timeout)
)
def fetch_fixture_by_id(fixture_id):
    """
    Obtiene un fixture específico por ID.
    
    Args:
        fixture_id: ID del fixture
    
    Returns:
        dict: Datos del fixture
    """
    url = f"{BASE_URL}/fixtures"

    headers = {
        "x-apisports-key": API_KEY,
    }

    params = {
        "id": fixture_id
    }

    logger.info(f"Solicitando fixture ID: {fixture_id}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code != 200:
            raise APIResponseError(f"API retornó status {response.status_code}")

        data = response.json()
        
        if data.get('response'):
            logger.info(f"✓ Fixture {fixture_id} obtenido")
        
        return data

    except Exception as e:
        logger.error(f"Error obteniendo fixture {fixture_id}: {str(e)}")
        raise
