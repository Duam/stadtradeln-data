import pandas as pd
from stadtradeln_data_tools.linestring_conversion import (
    get_linestring_from_coordinates,
    get_coordinates_from_linestring
)


def load_csv(
        csv_path: str
) -> pd.DataFrame:
    """Loads a STADTRADELN dataset into a pandas.DataFrame and converts the
    single 'edge_geo' column from LINESTRING-format into four separate columns
    containing latitudes and longitudes of the line's endpoints.
    :param csv_path: The path to the STADTRADELN csv dataset.
    :returns: A pandas.DataFrame containing the data.
    """
    df = pd.read_csv(csv_path)
    lines = [get_coordinates_from_linestring(s) for s in df.edge_geo]
    start_points = [line_vertices[0] for line_vertices in lines]
    end_points = [line_vertices[1] for line_vertices in lines]
    remaining_data = df[set(df.columns).difference({'edge_geo', 'occurences'})]
    return pd.DataFrame({
        'latitude_start': [coord.latitude for coord in start_points],
        'longitude_start': [coord.longitude for coord in start_points],
        'latitude_end': [coord.latitude for coord in end_points],
        'longitude_end': [coord.longitude for coord in end_points],
        'occurences': df.occurrences,
        **dict(remaining_data)
    })


def write_csv(
        df: pd.DataFrame,
        csv_path: str
) -> None:
    """ TODO: Write documentation
    :param df:
    :param csv_path:
    """
    lines = [
        get_linestring_from_coordinates(
            (row["latitude_start"], row["longitude_start"]),
            (row["latitude_end"], row["longitude_end"]))
        for row in df.itertuples()
    ]
    remaining_data = df[set(df.columns).difference(
        {'latitude_start', 'longitude_start', 'latitude_end', 'longitude_end', 'occurences'})]
    pd.DataFrame({
        'edge_geo': lines,
        'occurences': df.occurences,
        **dict(remaining_data)
    }).to_csv(csv_path, index=False)
