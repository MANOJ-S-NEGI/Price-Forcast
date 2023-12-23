import logging
import os
from datetime import datetime
from Variable_artifects.artifact import LOG_ENTRY_DIR


LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(LOG_ENTRY_DIR, LOG_FILE)
os.makedirs(logs_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(filename=LOG_FILE_PATH,
                    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
