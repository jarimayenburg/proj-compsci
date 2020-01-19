"""Contains the cell state enum."""

from enum import Enum, unique


@unique
class State(Enum):
    """Cell state enum."""

    FLAMMABLE = 0
    BURNING = 1
    BURNED_OUT = 2
    NON_FLAMMABLE = 3
