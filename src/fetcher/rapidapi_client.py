import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from .config import API_KEY, BASE_URL, MAX_RETRIES, RETRY_DELAY
from .logger import get_logger
import sys
import os

# Agregar el directorio raíz al path para importar common
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.common.retry import retry_on_failure
from src.common.exceptions import APIConnectionError, APIResponseError

logger = get_logger()

@retry_on_failure(
    max_attempts=MAX_RETRIES, 
    delay=RETRY_DELAY, 
    exceptions=(RequestException, ConnectionError, Timeout)
)
def fetch_leagues(country, season):
    """
    Obtiene ligas desde la API de Football API Sports.
    
    Args:
        country: País de las ligas
        season: Temporada (año)
    
    Returns:
        dict: Datos de las ligas en formato JSON
        
    Raises:
        APIConnectionError: Error de conexión con la API
        APIResponseError: Error en la respuesta de la API
    """
    url = f"{BASE_URL}/leagues"

    headers = {
        "x-apisports-key": API_KEY,
    }

    params = {
        "country": country,
        "season": season
    }

    logger.info(f"Solicitando ligas: país={country}, temporada={season}")

    try:
        response = requests.get(
            url, 
            headers=headers, 
            params=params,
            timeout=30  # Timeout de 30 segundos
        )

        # Verificar status code
        if response.status_code == 401:
            logger.error("Error 401: API key inválida o expirada")
            raise APIConnectionError("API key inválida. Verifica tu configuración en .env")
        
        if response.status_code == 429:
            logger.error("Error 429: Límite de requests excedido")
            raise APIConnectionError("Límite de API excedido. Espera antes de reintentar")
        
        if response.status_code != 200:
            logger.error(f"Error API: {response.status_code} - {response.text}")
            raise APIResponseError(f"API retornó status {response.status_code}")

        data = response.json()

        # Validar estructura de respuesta
        if "response" not in data:
            logger.error("Respuesta de API sin campo 'response'")
            raise APIResponseError("Formato de respuesta inválido")

        num_leagues = len(data.get('response', []))
        logger.info(f"✓ Ligas obtenidas exitosamente: {num_leagues}")

        return data

    except Timeout:
        logger.error("Timeout al conectar con la API")
        raise APIConnectionError("Timeout de conexión - La API no respondió a tiempo")
    
    except ConnectionError as e:
        logger.error(f"Error de conexión: {str(e)}")
        raise APIConnectionError(f"Error de conexión: {str(e)}")
    
    except requests.exceptions.JSONDecodeError:
        logger.error("Error al decodificar respuesta JSON")
        raise APIResponseError("La API retornó una respuesta no válida")
