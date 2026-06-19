import pandas as pd
import pandas.api.types as ptypes
import sys
import os

# Insertar en sys.path la ruta a src para que pytest pueda importar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pipeline.transform import transform_listings

def test_transform_listings_basic():
    data = {
        'id': [1, 2],
        'name': ['prop1', 'prop2'],
        'host_id': [10, 20],
        'host_name': ['hostA', 'hostB'],
        'neighbourhood': ['N1', 'N2'],
        'price': [100, 150],
        'calculated_host_listings_count': [3, 5]
    }
    df = pd.DataFrame(data)

    transformed_df = transform_listings(df)

    expected_cols = [
        'id', 'name', 'host_id', 'host_name', 'neighbourhood', 'price', 'price_tier',
        'calculated_host_listings_count', 'start_date', 'end_date', 'current_flag'
    ]
    assert all(col in transformed_df.columns for col in expected_cols)

    # Validar que price es numérico
    assert ptypes.is_numeric_dtype(transformed_df['price'])

    # Ver que los precios convertidos se detectan correctamente
    assert transformed_df.loc[transformed_df['price'] == 100.0, 'price_tier'].values[0] == 'medium'
    assert transformed_df.loc[transformed_df['price'] == 150.0, 'price_tier'].values[0] == 'medium'

    # `end_date` debe estar en NULL
    assert transformed_df['end_date'].isnull().all()
