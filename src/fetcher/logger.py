import logging
from datetime import datetime

def get_logger(name="fetcher"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(
        f"logs/fetch_{datetime.now().strftime('%Y_%m_%d')}.log"
    )
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
