import os
import pytest
import pandas as pd
from stadtradeln_data.pandas_importer import load_to_pandas


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


def test_load_to_pandas(csv_filename):
    df = load_to_pandas(csv_filename)
    print(df)
    assert (df.latitude_start == [0.0, 0.0, 1.0, 1.0]).all()
    assert (df.longitude_start == [0.0, 1.0, 1.0, 0.0]).all()
    assert (df.latitude_end == [0.0, 1.0, 1.0, 0.0]).all()
    assert (df.longitude_end == [1.0, 1.0, 0.0, 0.0]).all()
    assert (df.occurences == [3, 4, 5, 6]).all()

