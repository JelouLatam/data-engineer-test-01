from utils.logger import logger

def validate_columns(df, expected_columns):
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        logger.error(f"Columnas faltantes: {missing}")
        return False
    return True

def validate_unique_id(df, id_column):
    duplicated = df[df[id_column].duplicated()]
    if not duplicated.empty:
        logger.error(f"IDs duplicados en columna {id_column}: {duplicated[id_column].tolist()}")
        return False
    return True

def validate_no_nulls(df, critical_columns):
    nulls = df[critical_columns].isnull().sum()
    cols_with_nulls = nulls[nulls > 0].index.tolist()
    if cols_with_nulls:
        logger.error(f"Campos críticos con nulos: {cols_with_nulls}")
        return False
    return True

def validate_positive_values(df, column):
    negatives = df[df[column] <= 0]
    if not negatives.empty:
        logger.error(f"Valores no positivos en columna {column}:")
        logger.error(negatives)
        return False
    return True

def validate_price_range(df, column, min_price=10, max_price=10000):
    out_of_range = df[(df[column] < min_price) | (df[column] > max_price)]
    if not out_of_range.empty:
        logger.warning(f"Valores fuera de rango en columna {column}:")
        logger.warning(f"{out_of_range[[column]]}")
        return False
    return True
