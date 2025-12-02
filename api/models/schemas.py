"""Schemas Pydantic para validación y serialización"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Response Models

class LeagueResponse(BaseModel):
    """Schema para respuesta de liga individual"""
    league_id: int = Field(..., description="ID único de la liga")
    league_name: str = Field(..., description="Nombre de la liga")
    type: str = Field(..., description="Tipo: League o Cup")
    country: str = Field(..., description="País")
    season: int = Field(..., description="Temporada")
    start: Optional[str] = Field(None, description="Fecha inicio")
    end: Optional[str] = Field(None, description="Fecha fin")
    current: bool = Field(..., description="Si es temporada actual")
    
    class Config:
        json_schema_extra = {
            "example": {
                "league_id": 39,
                "league_name": "Premier League",
                "type": "League",
                "country": "England",
                "season": 2023,
                "start": "2023-08-11",
                "end": "2024-05-19",
                "current": False
            }
        }

class PaginatedResponse(BaseModel):
    """Schema para respuestas paginadas"""
    total: int = Field(..., description="Total de registros")
    page: int = Field(..., description="Página actual")
    limit: int = Field(..., description="Registros por página")
    data: List[LeagueResponse] = Field(..., description="Datos")

class StatsResponse(BaseModel):
    """Schema para estadísticas"""
    total_leagues: int
    countries: int
    seasons: List[int]
    country_list: List[str]

class HealthResponse(BaseModel):
    """Schema para health check"""
    status: str
    timestamp: datetime
    mongodb_available: bool
    total_leagues: int

class PipelineResponse(BaseModel):
    """Schema para respuesta de pipeline"""
    status: str
    message: str
    execution_time: Optional[float] = None

class ErrorResponse(BaseModel):
    """Schema para errores"""
    error: str
    detail: Optional[str] = None

class FixtureResponse(BaseModel):
    """Schema para respuesta de fixture individual"""
    id_partido: int
    equipo_local: str
    equipo_visitante: str
    id_equipo_local: int
    id_equipo_visitante: int
    estado_del_partido: str
    fecha: Optional[str]
    hora: Optional[str]
    goles_local_1MT: str
    goles_local_TR: str
    goles_visitante_1MT: str
    goles_visitante_TR: str
    liga_id: int
    liga_nombre: str
    ronda: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id_partido": 986991,
                "equipo_local": "Canuelas",
                "equipo_visitante": "Ituzaingó",
                "id_equipo_local": 1947,
                "id_equipo_visitante": 8386,
                "estado_del_partido": "Partido Finalizado",
                "fecha": "2023-02-11",
                "hora": "15:00:00.000000",
                "goles_local_1MT": "1",
                "goles_local_TR": "1",
                "goles_visitante_1MT": "0",
                "goles_visitante_TR": "0",
                "liga_id": 131,
                "liga_nombre": "Primera B Metropolitana",
                "ronda": "Apertura - 1"
            }
        }

class PaginatedFixturesResponse(BaseModel):
    """Schema para fixtures paginados"""
    total: int
    page: int
    limit: int
    data: List[FixtureResponse]

class FixturesStatsResponse(BaseModel):
    """Schema para estadísticas de fixtures"""
    total_fixtures: int
    total_ligas: int
    estados: List[str]
    ligas: List[int]
