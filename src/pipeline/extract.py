import pandas as pd
from utils.logger import logger

def extract_listings(filepath='data/listings.csv'):
    try:
        logger.info(f"Iniciando lectura de listings desde {filepath}")
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        logger.info(f"Lectura de listings completada: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"Error leyendo listings: {e}")
        raise

def extract_reviews(filepath='data/reviews.csv'):
    try:
        logger.info(f"Iniciando lectura de reviews desde {filepath}")
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        logger.info(f"Lectura de reviews completada: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"Error leyendo reviews: {e}")
        raise
