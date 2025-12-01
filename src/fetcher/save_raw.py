import json
import os
from datetime import datetime
from .logger import get_logger

logger = get_logger()

def save_raw(data, name):
    if data is None:
        logger.warning("No se guardó RAW: data es None")
        return

    os.makedirs("data/raw/", exist_ok=True)

    filename = f"data/raw/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    logger.info(f"Archivo RAW guardado como: {filename}")
