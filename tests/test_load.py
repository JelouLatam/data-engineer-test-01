import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pipeline.load import load_dimensions, load_facts


def test_load_dimensions_runs():
    df = pd.DataFrame({
        'id': [1],
        'name': ['prop1'],
        'host_id': [100],
        'host_name': ['hostA'],
        'neighbourhood': ['Neigh1'],
        'price': [150.0],
        'price_tier': ['medium'],
        'calculated_host_listings_count': [2],
        'start_date': ['2025-01-01'],
        'end_date': [None],
        'current_flag': [True]
    })
    # Ejecuta la carga (asegúrate de tener base de datos de prueba o mock para que no afectes datos reales)
    load_dimensions(df)


def test_load_facts_runs():
    df = pd.DataFrame({
        'review_id': [1],
        'listing_id': [1],
        'date': ['2025-01-01'],
        'is_recent': [True]
    })
    load_facts(df)
