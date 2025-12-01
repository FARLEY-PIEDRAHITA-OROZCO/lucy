import logging
import os
from datetime import datetime

def get_logger(name="cleaner"):
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)

    # Crear directorio de logs si no existe
    os.makedirs("logs", exist_ok=True)

    # Handler para archivo
    file_handler = logging.FileHandler(
        f"logs/cleaner_{datetime.now().strftime('%Y_%m_%d')}.log"
    )
    file_handler.setLevel(logging.INFO)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
