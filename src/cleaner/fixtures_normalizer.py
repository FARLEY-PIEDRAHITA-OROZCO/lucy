"""Normalizador de fixtures al formato requerido para pronósticos"""
import pandas as pd
from .logger import get_logger
from datetime import datetime

logger = get_logger()

def normalize_fixtures(raw_data):
    """
    Normaliza fixtures de la API al formato requerido.
    
    Formato objetivo:
    {
        "equipo_local": str,
        "equipo_visitante": str,
        "estado_del_partido": str,
        "fecha": str (YYYY-MM-DD),
        "goles_local_1MT": str,
        "goles_local_TR": str,
        "goles_visitante_1MT": str,
        "goles_visitante_TR": str,
        "hora": str (HH:MM:SS),
        "id_equipo_local": int,
        "id_equipo_visitante": int,
        "id_partido": int,
        "liga_id": int,
        "liga_nombre": str,
        "ronda": str
    }
    
    Args:
        raw_data: Datos JSON de la API
        
    Returns:
        DataFrame: Fixtures normalizados
    """
    records = []

    response_data = raw_data.get("response", [])
    logger.info(f"Normalizando {len(response_data)} fixtures...")

    for fixture_data in response_data:
        try:
            # Extraer información del fixture
            fixture = fixture_data.get('fixture', {})
            league = fixture_data.get('league', {})
            teams = fixture_data.get('teams', {})
            goals = fixture_data.get('goals', {})
            score = fixture_data.get('score', {})
            
            # Fecha y hora
            fixture_date = fixture.get('date', '')
            if fixture_date:
                dt = datetime.fromisoformat(fixture_date.replace('Z', '+00:00'))
                fecha = dt.strftime('%Y-%m-%d')
                hora = dt.strftime('%H:%M:%S.%f')
            else:
                fecha = None
                hora = None
            
            # Estado del partido
            status = fixture.get('status', {})
            status_long = status.get('long', 'Desconocido')
            
            # Mapear estados
            estado_map = {
                'Match Finished': 'Partido Finalizado',
                'Not Started': 'No Iniciado',
                'First Half': 'Primer Tiempo',
                'Halftime': 'Medio Tiempo',
                'Second Half': 'Segundo Tiempo',
                'Extra Time': 'Tiempo Extra',
                'Penalty In Progress': 'Penales',
                'Match Postponed': 'Pospuesto',
                'Match Cancelled': 'Cancelado',
                'Match Suspended': 'Suspendido',
                'Match Abandoned': 'Abandonado'
            }
            estado_del_partido = estado_map.get(status_long, status_long)
            
            # Equipos
            home_team = teams.get('home', {})
            away_team = teams.get('away', {})
            
            # Goles totales (tiempo reglamentario)
            goles_local_TR = str(goals.get('home', 0) or 0)
            goles_visitante_TR = str(goals.get('away', 0) or 0)
            
            # Goles medio tiempo
            halftime = score.get('halftime', {})
            goles_local_1MT = str(halftime.get('home', 0) or 0)
            goles_visitante_1MT = str(halftime.get('away', 0) or 0)
            
            record = {
                "equipo_local": home_team.get('name', 'Desconocido'),
                "equipo_visitante": away_team.get('name', 'Desconocido'),
                "estado_del_partido": estado_del_partido,
                "fecha": fecha,
                "goles_local_1MT": goles_local_1MT,
                "goles_local_TR": goles_local_TR,
                "goles_visitante_1MT": goles_visitante_1MT,
                "goles_visitante_TR": goles_visitante_TR,
                "hora": hora,
                "id_equipo_local": home_team.get('id', 0),
                "id_equipo_visitante": away_team.get('id', 0),
                "id_partido": fixture.get('id', 0),
                "liga_id": league.get('id', 0),
                "liga_nombre": league.get('name', 'Desconocida'),
                "ronda": league.get('round', 'N/A')
            }
            
            records.append(record)
            
        except Exception as e:
            logger.warning(f"Error procesando fixture: {str(e)}")
            continue

    df = pd.DataFrame(records)
    logger.info(f"✓ Normalización completada: {len(df)} fixtures")
    
    return df
