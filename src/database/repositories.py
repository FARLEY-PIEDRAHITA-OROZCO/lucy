"""Repositorios para operaciones CRUD en MongoDB"""
import logging
from typing import List, Dict, Optional
from datetime import datetime
from .connection import get_db
from .models import RawLeagueModel, CleanLeagueModel, FixturesModel

logger = logging.getLogger(__name__)

class LeagueRepository:
    """Repositorio para operaciones con ligas"""
    
    def __init__(self):
        self.db = get_db()
        self.raw_collection = self.db.raw_leagues if self.db is not None else None
        self.clean_collection = self.db.clean_leagues if self.db is not None else None
    
    def is_available(self) -> bool:
        """Verifica si MongoDB está disponible"""
        try:
            return self.db is not None and self.clean_collection is not None
        except:
            return False
    
    # === RAW DATA OPERATIONS ===
    
    def save_raw(self, data: Dict, country: str, season: int) -> Optional[str]:
        """
        Guarda datos raw en MongoDB
        
        Args:
            data: Datos JSON de la API
            country: País
            season: Temporada
            
        Returns:
            str: ID del documento insertado o None
        """
        if not self.is_available():
            return None
        
        try:
            document = RawLeagueModel.create(data, country, season)
            result = self.raw_collection.insert_one(document)
            logger.info(f"✓ Raw data guardada en MongoDB: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error guardando raw data en MongoDB: {str(e)}")
            return None
    
    def get_latest_raw(self, country: str, season: int) -> Optional[Dict]:
        """Obtiene el dato raw más reciente para país/temporada"""
        if not self.is_available():
            return None
        
        try:
            doc = self.raw_collection.find_one(
                {'country': country, 'season': season},
                sort=[('timestamp', -1)]
            )
            return doc['data'] if doc else None
        except Exception as e:
            logger.error(f"Error obteniendo raw data: {str(e)}")
            return None
    
    # === CLEAN DATA OPERATIONS ===
    
    def save_clean_batch(self, df, batch_size: int = 1000) -> int:
        """
        Guarda DataFrame limpio en MongoDB por lotes
        
        Args:
            df: DataFrame de pandas
            batch_size: Tamaño de lote para inserción
            
        Returns:
            int: Número de documentos insertados
        """
        if not self.is_available():
            return 0
        
        try:
            # Limpiar colección antes de insertar nuevos datos
            # self.clean_collection.delete_many({})  # Comentado para no perder datos históricos
            
            documents = CleanLeagueModel.bulk_from_dataframe(df)
            total_inserted = 0
            
            # Insertar por lotes
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                result = self.clean_collection.insert_many(batch, ordered=False)
                total_inserted += len(result.inserted_ids)
                logger.info(f"  Lote {i//batch_size + 1}: {len(batch)} documentos insertados")
            
            logger.info(f"✓ Total guardado en MongoDB: {total_inserted} documentos")
            return total_inserted
            
        except Exception as e:
            logger.error(f"Error guardando clean data en MongoDB: {str(e)}")
            return 0
    
    def get_all_leagues(self, page: int = 1, limit: int = 50) -> List[Dict]:
        """
        Obtiene ligas con paginación
        
        Args:
            page: Número de página (inicia en 1)
            limit: Registros por página
            
        Returns:
            list: Lista de ligas
        """
        if not self.is_available():
            return []
        
        try:
            skip = (page - 1) * limit
            cursor = self.clean_collection.find().skip(skip).limit(limit)
            leagues = list(cursor)
            
            # Convertir ObjectId a string
            for league in leagues:
                league['_id'] = str(league['_id'])
            
            return leagues
        except Exception as e:
            logger.error(f"Error obteniendo ligas: {str(e)}")
            return []
    
    def get_by_country(self, country: str, page: int = 1, limit: int = 50) -> List[Dict]:
        """Obtiene ligas filtradas por país"""
        if not self.is_available():
            return []
        
        try:
            skip = (page - 1) * limit
            cursor = self.clean_collection.find(
                {'country': country}
            ).skip(skip).limit(limit)
            
            leagues = list(cursor)
            for league in leagues:
                league['_id'] = str(league['_id'])
            
            return leagues
        except Exception as e:
            logger.error(f"Error filtrando por país: {str(e)}")
            return []
    
    def get_by_season(self, season: int, page: int = 1, limit: int = 50) -> List[Dict]:
        """Obtiene ligas filtradas por temporada"""
        if not self.is_available():
            return []
        
        try:
            skip = (page - 1) * limit
            cursor = self.clean_collection.find(
                {'season': season}
            ).skip(skip).limit(limit)
            
            leagues = list(cursor)
            for league in leagues:
                league['_id'] = str(league['_id'])
            
            return leagues
        except Exception as e:
            logger.error(f"Error filtrando por temporada: {str(e)}")
            return []
    
    def count_leagues(self) -> int:
        """Cuenta total de ligas en la base de datos"""
        if not self.is_available():
            return 0
        
        try:
            return self.clean_collection.count_documents({})
        except Exception as e:
            logger.error(f"Error contando documentos: {str(e)}")
            return 0
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de la base de datos"""
        if not self.is_available():
            return {}
        
        try:
            total = self.clean_collection.count_documents({})
            
            # Países únicos
            countries = self.clean_collection.distinct('country')
            
            # Temporadas únicas
            seasons = self.clean_collection.distinct('season')
            
            return {
                'total_leagues': total,
                'countries': len(countries),
                'seasons': sorted(seasons),
                'country_list': sorted(countries)
            }
        except Exception as e:
            logger.error(f"Error obteniendo stats: {str(e)}")
            return {}
