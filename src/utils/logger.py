import logging
import os

# Directorio y archivo para logs
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "pipeline_execution.log")

# Crear carpeta logs si no existe
os.makedirs(LOG_DIR, exist_ok=True)

# Configuración básica del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Logger principal del módulo
logger = logging.getLogger()
