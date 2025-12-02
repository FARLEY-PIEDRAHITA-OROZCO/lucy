#!/usr/bin/env python3
"""Script para iniciar la API de LUCY"""
import os
import uvicorn
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8001"))
    
    print("\n" + "="*70)
    print(f"🚀 Iniciando LUCY Sports API")
    print("="*70)
    print(f"📍 URL: http://{host}:{port}")
    print(f"📚 Docs: http://{host}:{port}/docs")
    print(f"🏥 Health: http://{host}:{port}/api/health")
    print("="*70 + "\n")
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
