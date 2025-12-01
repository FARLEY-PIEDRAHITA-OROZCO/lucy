#!/usr/bin/env python3
"""
Script de prueba para verificar las mejoras de la Fase 1:
- Seguridad (API key en .env)
- Logging completo
- Manejo de errores
- Reintentos automáticos
"""

import os
import sys

def test_config_loading():
    """Test 1: Verificar que la configuración se carga desde .env"""
    print("\n" + "="*60)
    print("TEST 1: Carga de Configuración desde .env")
    print("="*60)
    
    try:
        from src.fetcher.config import API_KEY, BASE_URL, MAX_RETRIES, DEFAULT_COUNTRY
        
        assert API_KEY is not None, "❌ API_KEY no cargada"
        assert BASE_URL is not None, "❌ BASE_URL no cargada"
        assert MAX_RETRIES > 0, "❌ MAX_RETRIES inválido"
        
        print("✓ Variables de entorno cargadas correctamente")
        print(f"  BASE_URL: {BASE_URL}")
        print(f"  DEFAULT_COUNTRY: {DEFAULT_COUNTRY}")
        print(f"  MAX_RETRIES: {MAX_RETRIES}")
        print(f"  API_KEY: {'*' * 20} (oculta por seguridad)")
        print("✅ TEST 1 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 1 FALLADO: {str(e)}\n")
        return False

def test_logger_creation():
    """Test 2: Verificar que los loggers se crean correctamente"""
    print("="*60)
    print("TEST 2: Creación de Loggers")
    print("="*60)
    
    try:
        from src.fetcher.logger import get_logger as get_fetcher_logger
        from src.cleaner.logger import get_logger as get_cleaner_logger
        
        fetcher_logger = get_fetcher_logger()
        cleaner_logger = get_cleaner_logger()
        
        assert fetcher_logger is not None, "❌ Fetcher logger no creado"
        assert cleaner_logger is not None, "❌ Cleaner logger no creado"
        assert os.path.exists("logs"), "❌ Directorio logs no existe"
        
        print("✓ Loggers creados correctamente")
        print(f"  Fetcher logger: {fetcher_logger.name}")
        print(f"  Cleaner logger: {cleaner_logger.name}")
        print(f"  Directorio logs: {os.path.abspath('logs')}")
        print("✅ TEST 2 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 2 FALLADO: {str(e)}\n")
        return False

def test_custom_exceptions():
    """Test 3: Verificar que las excepciones personalizadas existen"""
    print("="*60)
    print("TEST 3: Excepciones Personalizadas")
    print("="*60)
    
    try:
        from src.common.exceptions import (
            APIConnectionError,
            APIResponseError,
            DataValidationError,
            FileProcessingError,
            ConfigurationError
        )
        
        # Probar que se pueden instanciar
        exc1 = APIConnectionError("test")
        exc2 = DataValidationError("test")
        
        print("✓ Excepciones personalizadas importadas")
        print("  - APIConnectionError")
        print("  - APIResponseError")
        print("  - DataValidationError")
        print("  - FileProcessingError")
        print("  - ConfigurationError")
        print("✅ TEST 3 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 3 FALLADO: {str(e)}\n")
        return False

def test_retry_decorator():
    """Test 4: Verificar que el decorador de reintentos funciona"""
    print("="*60)
    print("TEST 4: Decorador de Reintentos")
    print("="*60)
    
    try:
        from src.common.retry import retry_on_failure
        
        # Función de prueba que falla 2 veces y luego funciona
        call_count = 0
        
        @retry_on_failure(max_attempts=3, delay=0.1, exceptions=(ValueError,))
        def test_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError(f"Intento {call_count} fallido")
            return "éxito"
        
        result = test_function()
        
        assert result == "éxito", "❌ Función no retornó resultado esperado"
        assert call_count == 3, "❌ No se ejecutaron los 3 intentos esperados"
        
        print("✓ Decorador de reintentos funciona correctamente")
        print(f"  Intentos realizados: {call_count}")
        print(f"  Resultado final: {result}")
        print("✅ TEST 4 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 4 FALLADO: {str(e)}\n")
        return False

def test_directory_structure():
    """Test 5: Verificar estructura de directorios"""
    print("="*60)
    print("TEST 5: Estructura de Directorios")
    print("="*60)
    
    try:
        required_dirs = ["data", "data/raw", "data/clean", "logs"]
        required_files = [".env", ".env.example", "README.md"]
        
        for directory in required_dirs:
            assert os.path.exists(directory), f"❌ Directorio {directory} no existe"
        
        for file in required_files:
            assert os.path.exists(file), f"❌ Archivo {file} no existe"
        
        print("✓ Estructura de directorios correcta")
        for directory in required_dirs:
            print(f"  ✓ {directory}")
        
        print("\n✓ Archivos de configuración presentes")
        for file in required_files:
            print(f"  ✓ {file}")
        
        print("✅ TEST 5 PASADO\n")
        return True
        
    except AssertionError as e:
        print(f"❌ TEST 5 FALLADO: {str(e)}\n")
        return False

def test_gitignore_security():
    """Test 6: Verificar que .env está en .gitignore"""
    print("="*60)
    print("TEST 6: Seguridad de .gitignore")
    print("="*60)
    
    try:
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
        
        assert ".env" in gitignore_content, "❌ .env no está en .gitignore"
        assert "data/" in gitignore_content, "❌ data/ no está en .gitignore"
        assert "logs/" in gitignore_content, "❌ logs/ no está en .gitignore"
        
        print("✓ Archivos sensibles protegidos en .gitignore")
        print("  ✓ .env (API keys)")
        print("  ✓ data/ (datos)")
        print("  ✓ logs/ (logs)")
        print("✅ TEST 6 PASADO\n")
        return True
        
    except Exception as e:
        print(f"❌ TEST 6 FALLADO: {str(e)}\n")
        return False

def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "█"*60)
    print("█" + " "*18 + "FASE 1: TESTS" + " "*18 + "█")
    print("█"*60)
    
    tests = [
        test_config_loading,
        test_logger_creation,
        test_custom_exceptions,
        test_retry_decorator,
        test_directory_structure,
        test_gitignore_security
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
