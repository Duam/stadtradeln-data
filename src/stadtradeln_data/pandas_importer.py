import pandas as pd
from stadtradeln_data.linestring_conversion import (
    get_coordinates_from_linestring
)


def load_to_pandas(
        csv_path: str
) -> pd.DataFrame:
    """Loads a STADTRADELN dataset into a pandas.DataFrame and converts the
    single 'edge_geo' column from LINESTRING-format into four separate columns
    containing latitudes and longitudes of the line's endpoints.
    :param csv_path: The path to the STADTRADELN csv dataset.
    :returns: A pandas.DataFrame containing the data.
    """
    df = pd.read_csv(csv_path)
    # TODO: Can this conversion be made more elegant?
    df.edge_geo = [get_coordinates_from_linestring(s) for s in df.edge_geo]
    latitude_start = [tpl[0][0] for tpl in df.edge_geo]
    longitude_start = [tpl[0][1] for tpl in df.edge_geo]
    latitude_end = [tpl[1][0] for tpl in df.edge_geo]
    longitude_end = [tpl[1][1] for tpl in df.edge_geo]
    return pd.DataFrame({
        'latitude_start': latitude_start,
        'longitude_start': longitude_start,
        'latitude_end': latitude_end,
        'longitude_end': longitude_end,
        'occurences': df.occurences
    })
