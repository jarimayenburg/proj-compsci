"""Defines a CA within the context of the simulation."""


class CA:
    """Defines a CA withing the context of the wildfire simulation."""

    # Possible states of a cell in the CA:
    #  0: Flammable
    #  1: Burning
    #  2: Burned out
    #  3: Inflammable
    STATES = [0, 1, 2, 3]

    def __init__(self, grid):
        """Construct a CA."""
        self.grid = grid

    def step(self):
        """Evolve the CA to the next step."""
        pass

    def from_file(filename):
        """
        Create a CA using a grid file.

        Args:
        - filenme: Path to the file the read the CA grid from
        """
        grid = CA.read_from_file(filename)

        return CA(grid)

    def read_from_file(filename):
        """
        Read a CA from a file.

        Args:
        - filename: Path to the file to read the CA grid from
        """
        grid = []

        try:
            with open(filename, "r") as grid_file:
                for line in grid_file:
                    # Strip of any leading and trailing whitespace
                    line = line.strip()

                    # Ignore empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    grid.append(list(map(int, list(line))))

            # Validate that what's been read is a valid CA grid
            CA.validate(grid)
        except Exception as e:
            raise ValueError("Invalid grid file") from e

        return grid

    def validate(grid):
        """
        Validate whether a CA grid is valid.

        A CA grid is valid if it's:
         1. Rectangular
         2. Contains only valid states

        Args:
        - grid: The grid to validate
        """
        if not type(grid) is list or not type(grid[0]) is list:
            raise CAGridInvalidError("Grid should be a 2D list")

        if not all(isinstance(cell, int) for line in grid for cell in line):
            raise CAGridInvalidError("Grid should contain only digits.")

        if not all(len(line) == len(grid[0]) for line in grid):
            raise CAGridInvalidError("Grid should be rectangular")

        if not all(cell in CA.STATES for line in grid for cell in line):
            raise CAGridInvalidError(
                "Grid cell values should be one of {}".format(CA.STATES)
            )


class CAGridInvalidError(ValueError):
    """Raised when a CA grid is invalid."""

    pass
