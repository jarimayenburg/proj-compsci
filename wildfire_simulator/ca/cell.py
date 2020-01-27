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

    def get_color(self):
        if self.veg == 'nov' or self.dens == 'nov':
            # Blue
            return 0, 105, 148, 255

        if self.state == 2:
            # Black
            return 0, 0, 0, 255
        elif self.state == 1:
            # Flame orange
            return 230, 41, 44, 255

        if self.veg == 'for':
            # Forest green
            return 13, 72, 13, self.density_as_int()
        elif self.veg == 'agr':
            # Wheat yellow
            return 243, 231, 169, self.density_as_int()
        elif self.veg == 'shr':
            # Shrubland green
            return 105, 200, 105, self.density_as_int()
        elif self.veg == 'nov':
            return 255, 255, 255, 255

    def density_as_int(self):
        """Return the vegetation density as an integer."""

        if self.dens == 'den':
            return 255
        elif self.dens == 'nor':
            return 170
        elif self.dens == 'spa':
            return 85
        else:
            return 0

