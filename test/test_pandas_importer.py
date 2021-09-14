import os
import pytest
import pandas as pd
from stadtradeln_data_tools.pandas_importer import load_csv, write_csv


@pytest.fixture
def csv_filename():
    filename = "test.csv"
    df = pd.DataFrame({'edge_geo': ['LINESTRING(0 0,0 1)',
                                    'LINESTRING(0 1,1 1)',
                                    'LINESTRING(1 1,1 0)',
                                    'LINESTRING(1 0,0 0)'],
                       'occurences': [3, 4, 5, 6]})
    df.to_csv(filename, index=False)
    yield filename
    os.remove(filename)


def test_load_csv(csv_filename):
    df = load_csv(csv_filename)
    assert (df.latitude_start == [0.0, 0.0, 1.0, 1.0]).all()
    assert (df.longitude_start == [0.0, 1.0, 1.0, 0.0]).all()
    assert (df.latitude_end == [0.0, 1.0, 1.0, 0.0]).all()
    assert (df.longitude_end == [1.0, 1.0, 0.0, 0.0]).all()
    assert (df.occurences == [3, 4, 5, 6]).all()


@pytest.fixture
def dataframe():
    return pd.DataFrame({
        'latitude_start': [0., 1., 1., 2., 2., 3., 3., 0.],
        'longitude_start': [0., 0., 1., 1., 2., 2., 3., 3.],
        'latitude_end': [1., 1., 2., 2., 3., 3., 0., 0.],
        'longitude_end': [0., 1., 1., 2., 2., 3., 3., 0.],
        'occurences': [1, 2, 3, 4, 5, 6, 7, 8],
        'additional_data': ['a', 'b', "c", "d", "e", "f", "g", "h"]
    })


def test_write_and_load_csv(dataframe):
    filename = "test.csv"
    write_csv(dataframe, filename)
    loaded_dataframe = load_csv(filename)
    os.remove(filename)
    assert dataframe.equals(loaded_dataframe)
