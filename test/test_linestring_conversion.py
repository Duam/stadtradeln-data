import pytest
from typing import Tuple
from stadtradeln_data_tools.linestring_conversion import (
    get_linestring_from_coordinates,
    get_coordinates_from_linestring
)


@pytest.mark.parametrize(
    "start_coordinate, end_coordinate, expected_linestring",
    [
        ((1, 2), (3, 4), "LINESTRING(1 2,3 4)"),
        ((1.1, 2.2), (3.3, 4.4), "LINESTRING(1.1 2.2,3.3 4.4)")
    ]
)
def test_get_linestring_from_coordinates(
        start_coordinate: Tuple[float, float],
        end_coordinate: Tuple[float, float],
        expected_linestring: str,
):
    assert get_linestring_from_coordinates(start_coordinate, end_coordinate) == expected_linestring


@pytest.mark.parametrize(
    "linestring, expected_start_coordinate, expected_end_coordinate",
    [
        ("LINESTRING(1 2,3 4)", (1, 2), (3, 4)),
        ("LINESTRING(1.1 2.2,3.3 4.4)", (1.1, 2.2), (3.3, 4.4))
    ]
)
def test_get_linestring_from_coordinates(
        linestring: str,
        expected_start_coordinate: Tuple[float, float],
        expected_end_coordinate: Tuple[float, float],
):
    assert get_coordinates_from_linestring(linestring) ==\
           (expected_start_coordinate, expected_end_coordinate)


