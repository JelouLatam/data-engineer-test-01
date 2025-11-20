import pandas as pd
from datetime import datetime
from utils.logger import logger

def remove_null_critical_fields(df, critical_columns):
    df_null = df[df[critical_columns].isnull().any(axis=1)]
    if not df_null.empty:
        logger.warning(f"Registros con valores nulos en campos críticos: {len(df_null)}. Guardando en output/listings_null_critical.csv")
        df_null.to_csv('output/listings_null_critical.csv', index=False)
    return df.dropna(subset=critical_columns)

def transform_listings(df):
    logger.info(f"Iniciando transformación de listings con {len(df)} registros")
    df = remove_null_critical_fields(df, ['id', 'price'])
    df = df.copy()

    df.loc[:, 'price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)

    bins = [0, 50, 150, 5000]
    labels = ['low', 'medium', 'high']
    df.loc[:, 'price_tier'] = pd.cut(df['price'], bins=bins, labels=labels)

    today_date = datetime.today().date()
    df.loc[:, 'start_date'] = today_date
    df.loc[:, 'end_date'] = pd.NaT
    df.loc[:, 'current_flag'] = True

    cols = ['id', 'name', 'host_id', 'host_name', 'neighbourhood', 'price', 'price_tier',
            'calculated_host_listings_count', 'start_date', 'end_date', 'current_flag']

    df_transformed = df[cols].copy()

    # Convertir end_date a object y reemplazar NaT por None para evitar error MySQL
    df_transformed['end_date'] = df_transformed['end_date'].astype(object).where(
        pd.notnull(df_transformed['end_date']), None)

    # Reemplazar NaN en todo el dataframe por None
    df_transformed = df_transformed.where(pd.notnull(df_transformed), None)

    logger.info(f"Transformación de listings completada: {len(df_transformed)} registros transformados")
    return df_transformed

def transform_reviews(df):
    logger.info(f"Iniciando transformación de reviews con {len(df)} registros")
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['listing_id', 'date'])
    df = df.reset_index(drop=True)
    df['review_id'] = df.index + 1
    df.loc[:, 'is_recent'] = df['date'] >= pd.Timestamp.now() - pd.Timedelta(days=365)

    cols = ['review_id', 'listing_id', 'date', 'is_recent']
    df_transformed = df[cols].copy()

    df_transformed['date'] = df_transformed['date'].astype(object).where(
        pd.notnull(df_transformed['date']), None)

    df_transformed = df_transformed.where(pd.notnull(df_transformed), None)

    logger.info(f"Transformación de reviews completada: {len(df_transformed)} registros transformados")
    return df_transformed
