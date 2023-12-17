import collections
from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


Coord = collections.namedtuple("Coord", ["x", "y"])

MOVEMENT = {
    Direction.NORTH: Coord(0, -1),
    Direction.SOUTH: Coord(0, 1),
    Direction.EAST: Coord(1, 0),
    Direction.WEST: Coord(-1, 0),
}


def add(c1: Coord, c2: Coord) -> Coord:
    return Coord(c1.x + c2.x, c1.y + c2.y)


def sub(c1: Coord, c2: Coord) -> Coord:
    return Coord(c1.x - c2.x, c1.y - c2.y)


def mult_scalar(scale: int, c1: Coord) -> Coord:
    return Coord(scale * c1.x, scale * c1.y)


def coord_abs(coord: Coord) -> int:
    return abs(coord.x) + abs(coord.y)


def coord_max(c1: Coord, c2: Coord) -> Coord:
    return Coord(max(c1.x, c2.x), max(c1.y, c2.y))


def coord_min(c1: Coord, c2: Coord) -> Coord:
    return Coord(min(c1.x, c2.x), min(c1.y, c2.y))
