import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pipeline.validate import validate_no_nulls, validate_unique_id, validate_positive_values


def test_validate_no_nulls_pass():
    df = pd.DataFrame({'id': [1, 2], 'price': [10, 20]})
    assert validate_no_nulls(df, ['id', 'price']) is True


def test_validate_no_nulls_fail():
    df = pd.DataFrame({'id': [1, None], 'price': [10, 20]})
    assert validate_no_nulls(df, ['id', 'price']) is False


def test_validate_unique_id_pass():
    df = pd.DataFrame({'id': [1, 2, 3]})
    assert validate_unique_id(df, 'id') is True


def test_validate_unique_id_fail():
    df = pd.DataFrame({'id': [1, 1, 2]})
    assert validate_unique_id(df, 'id') is False


def test_validate_positive_values_pass():
    df = pd.DataFrame({'price': [10, 20, 30]})
    assert validate_positive_values(df, 'price') is True


def test_validate_positive_values_fail():
    df = pd.DataFrame({'price': [10, -5, 30]})
    assert validate_positive_values(df, 'price') is False
