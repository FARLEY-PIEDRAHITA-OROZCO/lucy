"""Endpoints para consultar fixtures/partidos"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.database.repositories import FixturesRepository
from api.models.schemas import FixtureResponse, PaginatedFixturesResponse, FixturesStatsResponse

router = APIRouter()

@router.get("/fixtures", response_model=PaginatedFixturesResponse)
async def get_fixtures(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(50, ge=1, le=100, description="Registros por página (máx 100)")
):
    """Obtiene todos los fixtures con paginación"""
    repo = FixturesRepository()
    
    if not repo.is_available():
        raise HTTPException(
            status_code=503,
            detail="MongoDB no disponible"
        )
    
    # Obtener fixtures más recientes
    fixtures = repo.get_fixtures_by_date_range('2000-01-01', '2099-12-31', page=page, limit=limit)
    total = repo.count_fixtures()
    
    return PaginatedFixturesResponse(
        total=total,
        page=page,
        limit=limit,
        data=[FixtureResponse(**fixture) for fixture in fixtures]
    )

@router.get("/fixtures/league/{league_id}", response_model=PaginatedFixturesResponse)
async def get_fixtures_by_league(
    league_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    """Filtra fixtures por liga"""
    repo = FixturesRepository()
    
    if not repo.is_available():
        raise HTTPException(status_code=503, detail="MongoDB no disponible")
    
    fixtures = repo.get_fixtures_by_league(league_id, page=page, limit=limit)
    
    if not fixtures:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron fixtures para la liga: {league_id}"
        )
    
    # Contar total para esta liga
    all_league_fixtures = repo.get_fixtures_by_league(league_id, page=1, limit=10000)
    total = len(all_league_fixtures)
    
    return PaginatedFixturesResponse(
        total=total,
        page=page,
        limit=limit,
        data=[FixtureResponse(**fixture) for fixture in fixtures]
    )

@router.get("/fixtures/team/{team_id}", response_model=PaginatedFixturesResponse)
async def get_fixtures_by_team(
    team_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    """Filtra fixtures por equipo (local o visitante)"""
    repo = FixturesRepository()
    
    if not repo.is_available():
        raise HTTPException(status_code=503, detail="MongoDB no disponible")
    
    fixtures = repo.get_fixtures_by_team(team_id, page=page, limit=limit)
    
    if not fixtures:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron fixtures para el equipo: {team_id}"
        )
    
    all_team_fixtures = repo.get_fixtures_by_team(team_id, page=1, limit=10000)
    total = len(all_team_fixtures)
    
    return PaginatedFixturesResponse(
        total=total,
        page=page,
        limit=limit,
        data=[FixtureResponse(**fixture) for fixture in fixtures]
    )

@router.get("/fixtures/date-range", response_model=PaginatedFixturesResponse)
async def get_fixtures_by_date_range(
    start_date: str = Query(..., description="Fecha inicio (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Fecha fin (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    """Filtra fixtures por rango de fechas"""
    repo = FixturesRepository()
    
    if not repo.is_available():
        raise HTTPException(status_code=503, detail="MongoDB no disponible")
    
    fixtures = repo.get_fixtures_by_date_range(start_date, end_date, page=page, limit=limit)
    
    if not fixtures:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron fixtures entre {start_date} y {end_date}"
        )
    
    all_fixtures = repo.get_fixtures_by_date_range(start_date, end_date, page=1, limit=10000)
    total = len(all_fixtures)
    
    return PaginatedFixturesResponse(
        total=total,
        page=page,
        limit=limit,
        data=[FixtureResponse(**fixture) for fixture in fixtures]
    )

@router.get("/fixtures/stats", response_model=FixturesStatsResponse)
async def get_fixtures_stats():
    """Obtiene estadísticas de fixtures"""
    repo = FixturesRepository()
    
    if not repo.is_available():
        raise HTTPException(status_code=503, detail="MongoDB no disponible")
    
    stats = repo.get_fixtures_stats()
    
    return FixturesStatsResponse(**stats)
