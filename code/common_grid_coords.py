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
