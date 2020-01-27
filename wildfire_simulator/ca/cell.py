"""Contains the class defining cells in the CA."""


class Cell:
    """
    Defines a cell in the CA. Cells have the following properties:

    State.
    The state of the cell represents whether it's burning or not, the
    following states are valid:
    0: The cell is not burning
    1: The cell is burning
    2: The cell is burned out

    Position.
    Position of the cell in the grid as an (x, y)-coordinate.

    Altitude.
    The altitude of the cell in meters

    Vegetation.
    The type of vegetation that can be found in this cell, the following
    vegetation types are supported:
    for: Forest
    agr: Agriculture
    shr: Shrubland
    nov: No vegetation

    Vegetation density.
    The density of the vegetation in this cell, the following values are valid:
    den: Dense
    nor: Normal
    spa: Sparse
    nov: No vegetation
    """

    # Diameter of a cell
    diameter = 100

    def __init__(self, state, pos=(-1, -1), alt=0.5, veg='for', dens='nor'):
        """Construct the Cell."""
        self.state = state
        self.pos = pos
        self.alt = alt
        self.veg = veg
        self.dens = dens

    def copy(self):
        """Create a copy of this cell"""

        return Cell(self.state, self.pos, self.alt, self.veg, self.dens)
