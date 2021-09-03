import pytest
import pandas as pd
import copy
from stadtradeln_data.dataset_clipper import clip_to_rectangle
from typing import Tuple


def clip(
        df: pd.DataFrame,
        latitude_lim: Tuple[float, float],
        longitude_lim: Tuple[float, float],
) -> pd.DataFrame:
    """Clips the given STADTRADELN dataset to a desired rectangular geographic region.
    :param df: The STADTRADELN dataset.
    :param latitude_lim: A tuple containing minimum and maximum allowed latitude values.
    :param longitude_lim: A tuple containing minimum and maximum allowed longitude values.
    :returns: The clipped dataset.
    """
    df = df[df.latitude_start.between(latitude_lim[0], latitude_lim[1])]
    df = df[df.latitude_end.between(latitude_lim[0], latitude_lim[1])]
    df = df[df.longitude_start.between(longitude_lim[0], longitude_lim[1])]
    df = df[df.longitude_end.between(longitude_lim[0], longitude_lim[1])]
    return df


def create_dataset():
    return pd.DataFrame({
        'latitude_start': [0, 1, 1, 2, 2, 3, 3, 0],
        'longitude_start': [0, 0, 1, 1, 2, 2, 3, 3],
        'latitude_end': [1, 1, 2, 2, 3, 3, 0, 0],
        'longitude_end': [0, 1, 1, 2, 2, 3, 3, 0],
        'occurences': [1, 2, 3, 4, 5, 6, 7, 8]
    })


@pytest.mark.parametrize(
    "dataset, latitude_lim, longitude_lim",
    [
        (create_dataset(), (0, 3), (0, 3)),
        (create_dataset(), (0, 1), (0, 3)),
        (create_dataset(), (0, 0), (0, 1)),
        (create_dataset(), (0, -1), (1, 2)),
    ]
)
def test_get_linestring_from_coordinates(
        dataset: pd.DataFrame,
        latitude_lim: Tuple[float, float],
        longitude_lim: Tuple[float, float],
):
    dataset_copy = copy.deepcopy(dataset)  # Some pandas methods modify the original DataFrame
    clipped_dataset = clip_to_rectangle(dataset, latitude_lim, longitude_lim)
    expected_clipped_dataset = clip(dataset_copy, latitude_lim, longitude_lim)
    assert expected_clipped_dataset.equals(clipped_dataset)
