from typing import Tuple
from collections import namedtuple

Coordinate = namedtuple('Coordinate', ['latitude', 'longitude'])


def get_coordinates_from_linestring(
        linestring: str
) -> Tuple[Coordinate, Coordinate]:
    """Converts a GIS-readable linestring into two coordinate-pairs describing the line's endpoints.
    :param linestring: A string formatted like "LINESTRING(<latitude1> <longitude2>,<latitude2> <longitude2>)".
    :returns: Two coordinate-pairs having latitude and longitude, each.
    """
    endpoints = linestring.replace("LINESTRING(", "").replace(")", "").split(",")
    start_coordinate = Coordinate(*[float(coord) for coord in endpoints[0].split(" ")])
    end_coordinate = Coordinate(*[float(coord) for coord in endpoints[1].split(" ")])
    return start_coordinate, end_coordinate


def get_linestring_from_coordinates(
        start: Coordinate,
        end: Coordinate
) -> str:
    """Converts two coordinate-pairs into a GIS-readable linestring-format.
    :param start: Latitude and longitude of the line's start point.
    :param end: Latitude and longitude of the line's end point.
    :returns: A string formatted like "LINESTRING(<latitude1> <longitude2>,<latitude2> <longitude2>)".
    """
    start = Coordinate(float(start[0]), float(start[1]))
    end = Coordinate(float(end[0]), float(end[1]))
    return f'LINESTRING({start.latitude} {start.longitude},{end.latitude} {end.longitude})'
