"""Endpoints para ejecutar y monitorear el pipeline ETL"""
from fastapi import APIRouter, BackgroundTasks, HTTPException
import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from api.models.schemas import PipelineResponse

router = APIRouter()

# Estado global del pipeline (en producción usar Redis o base de datos)
pipeline_status = {
    "running": False,
    "last_execution": None,
    "last_status": None,
    "last_duration": None
}

def run_pipeline_task():
    """Ejecuta el pipeline en background"""
    global pipeline_status
    
    try:
        pipeline_status["running"] = True
        start_time = time.time()
        
        # Importar y ejecutar pipeline
        from main_fetcher import run_fetcher
        from main_cleaner import run_cleaner
        
        # Ejecutar fetcher
        fetcher_success = run_fetcher()
        if not fetcher_success:
            raise Exception("Fetcher falló")
        
        # Ejecutar cleaner
        cleaner_success = run_cleaner()
        if not cleaner_success:
            raise Exception("Cleaner falló")
        
        duration = time.time() - start_time
        
        pipeline_status["last_execution"] = datetime.utcnow().isoformat()
        pipeline_status["last_status"] = "success"
        pipeline_status["last_duration"] = duration
        
    except Exception as e:
        pipeline_status["last_execution"] = datetime.utcnow().isoformat()
        pipeline_status["last_status"] = f"error: {str(e)}"
        pipeline_status["last_duration"] = time.time() - start_time
    
    finally:
        pipeline_status["running"] = False

@router.post("/pipeline/run", response_model=PipelineResponse)
async def trigger_pipeline(background_tasks: BackgroundTasks):
    """Ejecuta el pipeline ETL en background"""
    global pipeline_status
    
    if pipeline_status["running"]:
        raise HTTPException(
            status_code=409,
            detail="Pipeline ya está ejecutándose"
        )
    
    # Añadir tarea en background
    background_tasks.add_task(run_pipeline_task)
    
    return PipelineResponse(
        status="started",
        message="Pipeline iniciado en background. Use /api/pipeline/status para monitorear."
    )

@router.get("/pipeline/status", response_model=PipelineResponse)
async def get_pipeline_status():
    """Obtiene el estado actual del pipeline"""
    global pipeline_status
    
    if pipeline_status["running"]:
        return PipelineResponse(
            status="running",
            message="Pipeline en ejecución..."
        )
    
    if pipeline_status["last_execution"] is None:
        return PipelineResponse(
            status="idle",
            message="Pipeline no se ha ejecutado aún"
        )
    
    return PipelineResponse(
        status=pipeline_status["last_status"],
        message=f"Última ejecución: {pipeline_status['last_execution']}",
        execution_time=pipeline_status["last_duration"]
    )
