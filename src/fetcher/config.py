import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Validar que existan las variables críticas
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY no encontrada en .env - Por favor configura tu API key")

BASE_URL = os.getenv("BASE_URL", "https://v3.football.api-sports.io")

# Endpoints disponibles
ENDPOINTS = {
    "leagues": "/leagues",
    "fixtures": "/fixtures",
    "teams": "/teams",
}

# Parámetros por defecto
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "england")
DEFAULT_SEASON = int(os.getenv("DEFAULT_SEASON", "2023"))

# Configuración de reintentos
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))
