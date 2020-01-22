"""Defines a CA within the context of the simulation."""

from matplotlib.colors import ListedColormap
from .state import State
from .evolution_rules import NNEvolutionRule

class CA:
    """Defines a CA withing the context of the wildfire simulation."""

    STATE_COLORMAP = ListedColormap(['green', 'orange', 'black', 'grey'])

    def __init__(self, grid, evolution_rule):
        """Construct a CA."""
        self.grid = grid
        self.evolution_rule = evolution_rule

    def step(self):
        """Evolve the CA to the next step."""

    def from_file(filename, evolution_rule=NNEvolutionRule):
        """
        Create a CA using a grid file.

        Args:
        - filenme: Path to the file the read the CA grid from
        """
        grid = CA.read_from_file(filename)

        return CA(grid, evolution_rule())

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

                    state_ints = list(map(int, list(line)))

                    grid.append(state_ints)

            # make it into a numpy array for faster accessing
            grid = np.array(grid)

            # Validate that what's been read is a valid CA grid
            # CA.validate(grid)
        except Exception as e:
            # raise e
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

        if not all(isinstance(cell, State) for line in grid for cell in line):
            raise CAGridInvalidError("Grid should contain State objects.")

        if not all(len(line) == len(grid[0]) for line in grid):
            raise CAGridInvalidError("Grid should be rectangular")


class CAGridInvalidError(ValueError):
    """Raised when a CA grid is invalid."""

    pass
