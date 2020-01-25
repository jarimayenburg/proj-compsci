"""Contains the class defining cells in the CA."""


class Cell:
    """Defines a cell in the CA."""

    def __init__(self, state, veg='for', dens='nor'):
        """Construct the Cell."""
        self.state = state
        self.veg = veg
        self.dens = dens
