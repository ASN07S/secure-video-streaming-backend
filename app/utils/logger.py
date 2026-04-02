import logging
import os
import json
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "access.log"),
    level=logging.INFO
)

def log_request(ip, path, status):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": ip,
        "endpoint": path,
        "status": status
    }

    logging.info(json.dumps(log_data))