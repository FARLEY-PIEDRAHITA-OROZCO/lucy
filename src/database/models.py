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
