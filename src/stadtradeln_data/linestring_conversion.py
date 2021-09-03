from typing import Tuple


def get_coordinates_from_linestring(
        linestring: str
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Converts a GIS-readable linestring into two coordinate-pairs describing the line's endpoints.
    :param linestring: A string formatted like "LINESTRING(<latitude1> <longitude2>, <latitude2> <longitude2>)".
    :returns: Two coordinate-pairs having latitude and longitude, each.
    """
    endpoints = linestring.replace("LINESTRING(", "").replace(")", "").split(",")
    start_coordinate = tuple([float(coord) for coord in endpoints[0].split(" ")])
    end_coordinate = tuple([float(coord) for coord in endpoints[1].split(" ")])
    return start_coordinate, end_coordinate


def get_linestring_from_coordinates(
        start_coordinate: Tuple[float, float],
        end_coordinate: Tuple[float, float]
) -> str:
    """Converts two coordinate-pairs into a GIS-readable linestring-format.
    :param start_coordinate: Latitude and longitude of the line's start point.
    :param end_coordinate: Latitude and longitude of the line's end point.
    :returns: A string formatted like "LINESTRING(<latitude1> <longitude2>,<latitude2> <longitude2>)".
    """
    return f'LINESTRING({start_coordinate[0]} {start_coordinate[1]},{end_coordinate[0]} {end_coordinate[1]})'
