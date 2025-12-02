"""Aplicación FastAPI principal"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Importar routers
from .routes import health, leagues, pipeline_routes

# Crear app
app = FastAPI(
    title="LUCY Sports API",
    description="API REST para consultar y gestionar datos deportivos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(leagues.router, prefix="/api", tags=["Leagues"])
app.include_router(pipeline_routes.router, prefix="/api", tags=["Pipeline"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "LUCY Sports API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }
