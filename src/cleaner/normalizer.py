import pandas as pd
from .logger import get_logger

logger = get_logger()

def normalize_leagues(raw_data):
    """
    Normaliza datos raw de ligas a estructura tabular.
    
    Args:
        raw_data: Datos en formato JSON de la API
        
    Returns:
        DataFrame: Datos normalizados
    """
    records = []

    response_data = raw_data.get("response", [])
    logger.info(f"Normalizando {len(response_data)} entradas de ligas...")

    for entry in response_data:
        league = entry.get("league", {})
        country = entry.get("country", {})
        season_list = entry.get("seasons", [])

        for season in season_list:
            records.append({
                "league_id": league.get("id"),
                "league_name": league.get("name"),
                "type": league.get("type"),
                "country": country.get("name"),
                "season": season.get("year"),
                "start": season.get("start"),
                "end": season.get("end"),
                "current": season.get("current"),
            })

    df = pd.DataFrame(records)
    logger.info(f"✓ Normalización completada: {len(df)} registros generados")
    
    return df
