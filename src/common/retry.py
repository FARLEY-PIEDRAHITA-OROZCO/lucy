"""Utilidad para reintentos con backoff exponencial"""
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def retry_on_failure(max_attempts=3, delay=2, backoff=2, exceptions=(Exception,)):
    """
    Decorador para reintentar una función en caso de fallo.
    
    Args:
        max_attempts: Número máximo de intentos
        delay: Delay inicial en segundos
        backoff: Multiplicador del delay en cada reintento
        exceptions: Tupla de excepciones a capturar
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        logger.error(
                            f"Falló {func.__name__} después de {max_attempts} intentos: {str(e)}"
                        )
                        raise
                    
                    logger.warning(
                        f"Intento {attempt}/{max_attempts} falló para {func.__name__}: {str(e)}. "
                        f"Reintentando en {current_delay}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            raise last_exception
        
        return wrapper
    return decorator
