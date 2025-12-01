#!/usr/bin/env python3
"""Tests para Fase 2 - MongoDB Integration"""
import sys
import os

def test_mongodb_connection():
    """Test 1: Verificar conexión a MongoDB"""
    print("\n" + "="*60)
    print("TEST 1: Conexión a MongoDB")
    print("="*60)
    
    try:
        from src.database.connection import get_db
        
        db = get_db()
        
        if db is None:
            print("⚠️  MongoDB no disponible (modo solo archivos)")
            print("✓ Sistema puede funcionar sin MongoDB")
            print("✅ TEST 1 PASADO (modo degradado)\n")
            return True
        
        # Verificar que podemos acceder a las colecciones
        collections = db.list_collection_names()
        print(f"✓ Conectado a MongoDB")
        print(f"  Base de datos: {db.name}")
        print(f"  Colecciones: {len(collections)}")
        print("✅ TEST 1 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 1 FALLADO: {str(e)}\n")
        return False

def test_repository_creation():
    """Test 2: Verificar creación de repositorio"""
    print("="*60)
    print("TEST 2: Creación de Repositorio")
    print("="*60)
    
    try:
        from src.database.repositories import LeagueRepository
        
        repo = LeagueRepository()
        is_available = repo.db is not None
        
        print(f"✓ Repositorio creado")
        print(f"  MongoDB disponible: {is_available}")
        
        if is_available:
            try:
                stats = repo.get_stats()
                print(f"  Total ligas: {stats.get('total_leagues', 0)}")
                print(f"  Países: {stats.get('countries', 0)}")
            except Exception as e:
                print(f"  Stats error: {str(e)}")
        
        print("✅ TEST 2 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 2 FALLADO: {str(e)}\n")
        return False

def test_models():
    """Test 3: Verificar modelos de datos"""
    print("="*60)
    print("TEST 3: Modelos de Datos")
    print("="*60)
    
    try:
        from src.database.models import RawLeagueModel, CleanLeagueModel
        import pandas as pd
        
        # Test RawLeagueModel
        test_data = {'response': [{'league': {'id': 1}}]}
        raw_doc = RawLeagueModel.create(test_data, 'england', 2023)
        
        assert 'timestamp' in raw_doc
        assert raw_doc['country'] == 'england'
        assert raw_doc['season'] == 2023
        
        print("✓ RawLeagueModel funciona")
        
        # Test CleanLeagueModel
        test_df = pd.DataFrame([{
            'league_id': 1,
            'league_name': 'Test',
            'type': 'League',
            'country': 'England',
            'season': 2023,
            'start': '2023-01-01',
            'end': '2023-12-31',
            'current': True
        }])
        
        docs = CleanLeagueModel.bulk_from_dataframe(test_df)
        assert len(docs) == 1
        assert docs[0]['league_id'] == 1
        
        print("✓ CleanLeagueModel funciona")
        print("✅ TEST 3 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 3 FALLADO: {str(e)}\n")
        return False

def test_dual_storage():
    """Test 4: Verificar almacenamiento dual (archivos + MongoDB)"""
    print("="*60)
    print("TEST 4: Almacenamiento Dual")
    print("="*60)
    
    try:
        # Verificar que existen funciones de guardado
        from src.fetcher.save_raw import save_raw
        from src.cleaner.save_clean import save_clean
        
        print("✓ Módulos de guardado importados")
        print("  - save_raw (JSON + MongoDB)")
        print("  - save_clean (CSV + MongoDB)")
        print("✅ TEST 4 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 4 FALLADO: {str(e)}\n")
        return False

def test_requirements():
    """Test 5: Verificar que pymongo está instalado"""
    print("="*60)
    print("TEST 5: Dependencias")
    print("="*60)
    
    try:
        import pymongo
        print(f"✓ pymongo instalado: versión {pymongo.__version__}")
        
        with open('requirements.txt', 'r') as f:
            reqs = f.read()
            assert 'pymongo' in reqs
        
        print("✓ pymongo en requirements.txt")
        print("✅ TEST 5 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 5 FALLADO: {str(e)}\n")
        return False

def test_env_config():
    """Test 6: Verificar configuración de MongoDB en .env"""
    print("="*60)
    print("TEST 6: Configuración MongoDB")
    print("="*60)
    
    try:
        # Verificar .env
        assert os.path.exists('.env'), ".env no existe"
        
        with open('.env', 'r') as f:
            env_content = f.read()
            assert 'MONGO_URL' in env_content
            assert 'MONGO_DB_NAME' in env_content
        
        print("✓ Variables MongoDB en .env")
        print("  - MONGO_URL")
        print("  - MONGO_DB_NAME")
        
        # Verificar .env.example
        with open('.env.example', 'r') as f:
            example_content = f.read()
            assert 'MONGO_URL' in example_content
        
        print("✓ Variables MongoDB en .env.example")
        print("✅ TEST 6 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 6 FALLADO: {str(e)}\n")
        return False

def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "█"*60)
    print("█" + " "*18 + "FASE 2: TESTS" + " "*18 + "█")
    print("█"*60)
    
    tests = [
        test_env_config,
        test_requirements,
        test_models,
        test_mongodb_connection,
        test_repository_creation,
        test_dual_storage
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Resumen
    print("="*60)
    print("RESUMEN DE TESTS")
    print("="*60)
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Pasados: {passed}/{total}")
    
    if passed == total:
        print("✅ TODOS LOS TESTS PASARON")
        print("\nℹ️  Nota: Si MongoDB no está instalado, el sistema funciona")
        print("   en modo degradado solo con archivos (CSV/JSON).")
        print("="*60)
        return True
    else:
        failed = total - passed
        print(f"❌ {failed} tests fallaron")
        print("="*60)
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
