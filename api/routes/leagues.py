"""Endpoints para consultar ligas"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.database.repositories import LeagueRepository
from api.models.schemas import LeagueResponse, PaginatedResponse, StatsResponse, ErrorResponse

router = APIRouter()

@router.get("/leagues", response_model=PaginatedResponse)
async def get_leagues(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(50, ge=1, le=100, description="Registros por página (máx 100)")
):
    """Obtiene todas las ligas con paginación"""
    repo = LeagueRepository()
    
    if not repo.is_available():
        raise HTTPException(
            status_code=503,
            detail="MongoDB no disponible. Use archivos CSV en data/clean/"
        )
    
    leagues = repo.get_all_leagues(page=page, limit=limit)
    total = repo.count_leagues()
    
    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        data=[LeagueResponse(**league) for league in leagues]
    )

@router.get("/leagues/country/{country}", response_model=PaginatedResponse)
async def get_leagues_by_country(
    country: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    """Filtra ligas por país"""
    repo = LeagueRepository()
    
    if not repo.is_available():
        raise HTTPException(status_code=503, detail="MongoDB no disponible")
    
    leagues = repo.get_by_country(country, page=page, limit=limit)
    
    if not leagues:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron ligas para el país: {country}"
        )
    
    # Contar total para este país
    all_country_leagues = repo.get_by_country(country, page=1, limit=10000)
    total = len(all_country_leagues)
    
    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        data=[LeagueResponse(**league) for league in leagues]
    )

@router.get("/leagues/season/{season}", response_model=PaginatedResponse)
async def get_leagues_by_season(
    season: int,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    """Filtra ligas por temporada"""
    repo = LeagueRepository()
    
    if not repo.is_available():
        raise HTTPException(status_code=503, detail="MongoDB no disponible")
    
    leagues = repo.get_by_season(season, page=page, limit=limit)
    
    if not leagues:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron ligas para la temporada: {season}"
        )
    
    all_season_leagues = repo.get_by_season(season, page=1, limit=10000)
    total = len(all_season_leagues)
    
    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        data=[LeagueResponse(**league) for league in leagues]
    )

@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Obtiene estadísticas generales"""
    repo = LeagueRepository()
    
    if not repo.is_available():
        raise HTTPException(status_code=503, detail="MongoDB no disponible")
    
    stats = repo.get_stats()
    
    return StatsResponse(**stats)
