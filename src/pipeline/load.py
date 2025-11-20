from utils.db_connector import get_connection
from utils.logger import logger

def load_dimensions(df_listings):
    conn = get_connection()
    cursor = conn.cursor()

    upsert_query = """
        INSERT INTO dim_listings (id, name, host_id, host_name, neighbourhood, price,
                                  price_tier, calculated_host_listings_count,
                                  start_date, end_date, current_flag)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            host_id = VALUES(host_id),
            host_name = VALUES(host_name),
            neighbourhood = VALUES(neighbourhood),
            price = VALUES(price),
            price_tier = VALUES(price_tier),
            calculated_host_listings_count = VALUES(calculated_host_listings_count),
            start_date = VALUES(start_date),
            end_date = VALUES(end_date),
            current_flag = VALUES(current_flag)
    """

    values = [tuple(row) for row in df_listings.itertuples(index=False)]

    try:
        logger.info(f"Iniciando carga de dim_listings con {len(values)} registros")
        cursor.executemany(upsert_query, values)
        conn.commit()
        logger.info("Carga de dim_listings completada exitosamente")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error cargando dim_listings: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def load_facts(df_reviews):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO fact_reviews (review_id, listing_id, date, is_recent)
        VALUES (%s, %s, %s, %s)
    """

    values = [tuple(row) for row in df_reviews.itertuples(index=False)]

    try:
        logger.info(f"Iniciando carga de fact_reviews con {len(values)} registros")
        cursor.executemany(insert_query, values)
        conn.commit()
        logger.info("Carga de fact_reviews completada exitosamente")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error cargando fact_reviews: {e}")