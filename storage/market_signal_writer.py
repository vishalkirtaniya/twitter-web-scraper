import json
import os
from utils.logger import get_logger

logger = get_logger(__name__)

def write_market_signal(signal: dict, path="data/signals"):
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, "market_signal.json")

    with open(file_path, "w") as f:
        json.dump(signal, f, indent=2)

    logger.info(f"Market signal written to {file_path}")
