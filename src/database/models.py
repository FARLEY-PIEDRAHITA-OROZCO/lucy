"""Modelos y schemas para MongoDB"""
from datetime import datetime
from typing import Dict, List, Any

class RawLeagueModel:
    """Modelo para datos raw de ligas"""
    
    @staticmethod
    def create(data: Dict, country: str, season: int) -> Dict:
        """
        Crea documento para colección raw_leagues
        
        Args:
            data: Datos JSON de la API
            country: País consultado
            season: Temporada consultada
            
        Returns:
            dict: Documento para MongoDB
        """
        return {
            'timestamp': datetime.utcnow(),
            'country': country,
            'season': season,
            'data': data,
            'record_count': len(data.get('response', [])),
            'source': 'football-api-sports'
        }

class FixturesModel:
    """Modelo para datos de fixtures/partidos"""
    
    @staticmethod
    def from_dataframe_row(row: Dict) -> Dict:
        """
        Convierte fila de DataFrame de fixtures a documento MongoDB
        
        Args:
            row: Fila del DataFrame como dict
            
        Returns:
            dict: Documento para MongoDB
        """
        return {
            'id_partido': int(row['id_partido']),
            'equipo_local': str(row['equipo_local']),
            'equipo_visitante': str(row['equipo_visitante']),
            'id_equipo_local': int(row['id_equipo_local']),
            'id_equipo_visitante': int(row['id_equipo_visitante']),
            'estado_del_partido': str(row['estado_del_partido']),
            'fecha': str(row['fecha']) if row.get('fecha') else None,
            'hora': str(row['hora']) if row.get('hora') else None,
            'goles_local_1MT': str(row['goles_local_1MT']),
            'goles_local_TR': str(row['goles_local_TR']),
            'goles_visitante_1MT': str(row['goles_visitante_1MT']),
            'goles_visitante_TR': str(row['goles_visitante_TR']),
            'liga_id': int(row['liga_id']),
            'liga_nombre': str(row['liga_nombre']),
            'ronda': str(row['ronda']),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    
    @staticmethod
    def bulk_from_dataframe(df) -> List[Dict]:
        """Convierte DataFrame completo a lista de documentos"""
        return [FixturesModel.from_dataframe_row(row) 
                for row in df.to_dict('records')]

class CleanLeagueModel:
    """Modelo para datos limpios de ligas"""
    
    @staticmethod
    def from_dataframe_row(row: Dict) -> Dict:
        """
        Convierte una fila de DataFrame a documento MongoDB
        
        Args:
            row: Fila del DataFrame como dict
            
        Returns:
            dict: Documento para MongoDB
        """
        return {
            'league_id': int(row['league_id']),
            'league_name': str(row['league_name']),
            'type': str(row['type']),
            'country': str(row['country']),
            'season': int(row['season']),
            'start': str(row['start']) if row.get('start') else None,
            'end': str(row['end']) if row.get('end') else None,
            'current': bool(row['current']),
            'created_at': datetime.utcnow()
        }
    
    @staticmethod
    def bulk_from_dataframe(df) -> List[Dict]:
        """
        Convierte DataFrame completo a lista de documentos
        
        Args:
            df: DataFrame de pandas
            
        Returns:
            list: Lista de documentos para MongoDB
        """
        return [CleanLeagueModel.from_dataframe_row(row) 
                for row in df.to_dict('records')]
