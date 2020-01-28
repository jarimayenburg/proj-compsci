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
        """Color to use for this cell"""

        if self.state == 2:
            # Black
            color = 0, 0, 0
        elif self.state == 1:
            # Flame orange
            color = 230, 41, 44
        elif self.veg == 'nov':
            # Blue
            color = 0, 105, 148
        elif self.dens == 'nov':
            # Gray
            color = 188, 188, 188
        elif self.veg == 'for':
            # Forest green
            if self.dens == 'den':
                color = 13, 72, 13
            elif self.dens == 'nor':
                color = 59, 128, 59
            else:
                color = 149, 193, 149
        elif self.veg == 'agr':
            # Wheat yellow
            if self.dens == 'den':
                color = 242, 210, 50
            elif self.dens == 'nor':
                color = 236, 221, 147
            else:
                color = 210, 205, 178
        elif self.veg == 'shr':
            # Shrubland green
            if self.dens == 'den':
                color = 105, 200, 105
            elif self.dens == 'nor':
                color = 162, 220, 162
            else:
                color = 192, 220, 192
        else:
            raise ValueError("Invalid vegetation type")

        # Convert to 0-1
        color = tuple([c / 255 for c in color])

        return color

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

