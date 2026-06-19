import sys
import os
import json
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extract import extract_listings, extract_reviews
from validate import (
    validate_columns, validate_unique_id, validate_no_nulls, validate_positive_values, validate_price_range
)
from transform import transform_listings, transform_reviews
from load import load_dimensions, load_facts
from utils.logger import logger


def convert_types(obj):
    if isinstance(obj, dict):
        return {k: convert_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def save_data_quality_report(report_dict, filepath='output/data_quality_report.json'):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    converted_report = convert_types(report_dict)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(converted_report, f, indent=4)
    logger.info(f"Reporte de calidad de datos guardado en {filepath}")


def main():
    os.makedirs('logs', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    logger.info("Inicio del pipeline")

    data_quality_report = {}

    try:
        # Extracción
        listings = extract_listings()
        reviews = extract_reviews()
        logger.info("Extracción completada")

        # Transformación
        listings_t = transform_listings(listings)
        reviews_t = transform_reviews(reviews)
        logger.info("Transformación completada")

        # Validaciones listings
        data_quality_report['null_counts'] = {
            "listings_id": listings_t['id'].isnull().sum(),
            "listings_price": listings_t['price'].isnull().sum()
        }
        logger.info(f"Nulos en id listings: {data_quality_report['null_counts']['listings_id']}")
        logger.info(f"Nulos en price listings: {data_quality_report['null_counts']['listings_price']}")
        if not validate_no_nulls(listings_t, ['id', 'price']):
            raise Exception("Campos críticos nulos en listings después de transformaciones")

        expected_listing_cols = [
            'id', 'name', 'host_id', 'neighbourhood', 'price', 'price_tier',
            'start_date', 'end_date', 'current_flag'
        ]
        if not validate_columns(listings_t, expected_listing_cols):
            raise Exception("Columnas faltantes en listings")
        if not validate_unique_id(listings_t, 'id'):
            raise Exception("IDs duplicados en listings")
        if not validate_positive_values(listings_t, 'price'):
            raise Exception("Precios negativos o cero en listings")

        duplicates_count = len(listings_t[listings_t['id'].duplicated()])
        data_quality_report['duplicates'] = {
            "listings_id_duplicates": duplicates_count
        }

        min_price, max_price = 10, 10000
        out_of_range = listings_t[(listings_t['price'] < min_price) | (listings_t['price'] > max_price)]
        data_quality_report['price_range_warnings'] = len(out_of_range)
        if len(out_of_range) > 0:
            logger.warning(f"Existen precios fuera del rango {min_price}-{max_price}: {len(out_of_range)} casos")

        logger.info("Validación listings exitosa")

        # Validaciones reviews
        expected_review_cols = ['review_id', 'listing_id', 'date', 'is_recent']
        if not validate_columns(reviews_t, expected_review_cols):
            raise Exception("Columnas faltantes en reviews")
        if not validate_unique_id(reviews_t, 'review_id'):
            raise Exception("IDs duplicados en reviews")
        logger.info("Validación reviews exitosa")

        valid_listing_ids = set(listings_t['id'])
        invalid_reviews = reviews_t[~reviews_t['listing_id'].isin(valid_listing_ids)]
        count_invalid = len(invalid_reviews)
        data_quality_report['invalid_reviews_filtered'] = count_invalid

        if count_invalid > 0:
            logger.warning(f"Se eliminaron {count_invalid} reviews con listing_id inválido")
            invalid_reviews.to_csv('output/invalid_reviews.csv', index=False)
        reviews_t_valid = reviews_t[reviews_t['listing_id'].isin(valid_listing_ids)].copy()

        # Guardar reporte de calidad
        save_data_quality_report(data_quality_report)

        # Carga
        load_dimensions(listings_t)
        load_facts(reviews_t_valid)
        logger.info("Carga completada")

    except Exception as e:
        logger.error(f"Pipeline detenido con error: {e}")
        logger.error(f"Error en pipeline: {e}")

    logger.info("Pipeline finalizado")


if __name__ == '__main__':
    main()