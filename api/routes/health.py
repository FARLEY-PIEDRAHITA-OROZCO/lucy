"""Endpoints de health check y status"""
from fastapi import APIRouter
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from src.database.repositories import LeagueRepository
from api.models.schemas import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Verifica el estado del sistema"""
    repo = LeagueRepository()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        mongodb_available=repo.is_available(),
        total_leagues=repo.count_leagues() if repo.is_available() else 0
    )
