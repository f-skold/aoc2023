import collections
from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


Coord = collections.namedtuple("Coord", ["x", "y"])
Coord2 = collections.namedtuple("Coord2", ["x", "y"])
Coord3 = collections.namedtuple("Coord3", ["x", "y", "z"])

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


def add2(c1: Coord2, c2: Coord2) -> Coord2:
    return Coord(c1.x + c2.x, c1.y + c2.y)


# Add add 3D coords below


def add3(c1: Coord3, c2: Coord3) -> Coord3:
    return Coord3(c1.x + c2.x, c1.y + c2.y, c1.z + c2.z)


def sub3(c1: Coord3, c2: Coord3) -> Coord3:
    return Coord3(c1.x - c2.x, c1.y - c2.y, c1.z - c2.z)


def copy3(c1: Coord3) -> Coord3:
    return Coord3(c1.x, c1.y, c1.z)


def sign3(c1: Coord3) -> Coord3:
    sx = min(1, max(-1, c1.x))
    sy = min(1, max(-1, c1.y))
    sz = min(1, max(-1, c1.z))
    return Coord3(sx, sy, sz)
