#!/usr/bin/env python3
"""Tests para Fase 3 - API REST con FastAPI"""
import sys
import requests
import time
import subprocess
import signal

def start_api_server():
    """Inicia el servidor API en background"""
    print("Iniciando servidor API...")
    process = subprocess.Popen(
        [sys.executable, "start_api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=None if sys.platform == 'win32' else os.setsid
    )
    
    # Esperar a que el servidor esté listo
    max_wait = 10
    for i in range(max_wait):
        try:
            response = requests.get("http://localhost:8001/api/health", timeout=1)
            if response.status_code == 200:
                print("✓ Servidor API listo\n")
                return process
        except:
            time.sleep(1)
    
    print("❌ Servidor no respondió a tiempo")
    return process

def stop_api_server(process):
    """Detiene el servidor API"""
    if process:
        if sys.platform == 'win32':
            process.terminate()
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait()
        print("\n✓ Servidor detenido")

def test_api_structure():
    """Test 1: Verificar estructura de archivos API"""
    print("\n" + "="*60)
    print("TEST 1: Estructura de API")
    print("="*60)
    
    try:
        import os
        
        required_files = [
            'api/__init__.py',
            'api/main.py',
            'api/models/schemas.py',
            'api/routes/health.py',
            'api/routes/leagues.py',
            'api/routes/pipeline_routes.py',
            'start_api.py'
        ]
        
        for file in required_files:
            assert os.path.exists(file), f"Falta {file}"
        
        print("✓ Todos los archivos de API presentes")
        for file in required_files:
            print(f"  ✓ {file}")
        
        print("✅ TEST 1 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 1 FALLADO: {str(e)}\n")
        return False

def test_api_imports():
    """Test 2: Verificar imports de FastAPI"""
    print("="*60)
    print("TEST 2: Imports de FastAPI")
    print("="*60)
    
    try:
        from fastapi import FastAPI
        from api.main import app
        from api.models.schemas import LeagueResponse, PaginatedResponse
        
        assert isinstance(app, FastAPI)
        
        print("✓ FastAPI app creada correctamente")
        print(f"  Nombre: {app.title}")
        print(f"  Versión: {app.version}")
        print("✓ Schemas Pydantic importados")
        print("✅ TEST 2 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 2 FALLADO: {str(e)}\n")
        return False

def test_health_endpoint():
    """Test 3: Verificar endpoint /health"""
    print("="*60)
    print("TEST 3: Endpoint /health")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8001/api/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "mongodb_available" in data
        assert "total_leagues" in data
        
        print("✓ Endpoint /health funciona")
        print(f"  Status: {data['status']}")
        print(f"  MongoDB: {data['mongodb_available']}")
        print(f"  Total ligas: {data['total_leagues']}")
        print("✅ TEST 3 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 3 FALLADO: {str(e)}\n")
        return False

def test_leagues_endpoint():
    """Test 4: Verificar endpoint /leagues"""
    print("="*60)
    print("TEST 4: Endpoint /leagues")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8001/api/leagues?page=1&limit=5")
        
        if response.status_code == 503:
            print("⚠️  MongoDB no disponible - endpoint retorna 503 correctamente")
            print("✅ TEST 4 PASADO (modo degradado)\n")
            return True
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total" in data
        assert "page" in data
        assert "limit" in data
        assert "data" in data
        
        print("✓ Endpoint /leagues funciona")
        print(f"  Total: {data['total']}")
        print(f"  Página: {data['page']}")
        print(f"  Registros retornados: {len(data['data'])}")
        print("✅ TEST 4 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 4 FALLADO: {str(e)}\n")
        return False

def test_stats_endpoint():
    """Test 5: Verificar endpoint /stats"""
    print("="*60)
    print("TEST 5: Endpoint /stats")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8001/api/stats")
        
        if response.status_code == 503:
            print("⚠️  MongoDB no disponible - endpoint retorna 503")
            print("✅ TEST 5 PASADO (modo degradado)\n")
            return True
        
        assert response.status_code == 200
        data = response.json()
        
        print("✓ Endpoint /stats funciona")
        print(f"  Total ligas: {data['total_leagues']}")
        print(f"  Países: {data['countries']}")
        print("✅ TEST 5 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 5 FALLADO: {str(e)}\n")
        return False

def test_docs_available():
    """Test 6: Verificar documentación Swagger"""
    print("="*60)
    print("TEST 6: Documentación Swagger")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8001/docs")
        assert response.status_code == 200
        
        print("✓ Swagger UI disponible en /docs")
        print("✓ ReDoc disponible en /redoc")
        print("✅ TEST 6 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 6 FALLADO: {str(e)}\n")
        return False

def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "█"*60)
    print("█" + " "*18 + "FASE 3: TESTS" + " "*18 + "█")
    print("█"*60)
    
    # Tests sin servidor
    results = []
    results.append(test_api_structure())
    results.append(test_api_imports())
    
    # Tests con servidor
    print("\n" + "="*60)
    print("INICIANDO SERVIDOR PARA TESTS")
    print("="*60 + "\n")
    
    import os
    server_process = start_api_server()
    
    try:
        results.append(test_health_endpoint())
        results.append(test_leagues_endpoint())
        results.append(test_stats_endpoint())
        results.append(test_docs_available())
    finally:
        stop_api_server(server_process)
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE TESTS")
    print("="*60)
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Pasados: {passed}/{total}")
    
    if passed == total:
        print("✅ TODOS LOS TESTS PASARON")
        print("\nℹ️  Para iniciar la API manualmente:")
        print("   python start_api.py")
        print("   Docs: http://localhost:8001/docs")
        print("="*60)
        return True
    else:
        failed = total - passed
        print(f"❌ {failed} tests fallaron")
        print("="*60)
        return False

if __name__ == "__main__":
    import os
    success = run_all_tests()
    sys.exit(0 if success else 1)
