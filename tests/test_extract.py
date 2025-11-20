import sys
import os

# Insertar ruta al src antes de importar tus módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pipeline.extract import extract_listings, extract_reviews


def test_extract_listings_file_exists():
    df = extract_listings()
    assert not df.empty

def test_extract_reviews_file_exists():
    df = extract_reviews()
    assert not df.empty

def test_extract_listings_columns():
    df = extract_listings()
    expected_cols = ['id', 'name', 'host_id', 'host_name', 'neighbourhood', 'price']
    for col in expected_cols:
        assert col in df.columns
