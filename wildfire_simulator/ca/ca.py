"""Defines a CA within the context of the simulation."""

import numpy as np
from matplotlib.colors import ListedColormap
from .cell import Cell
from .evolution_rules import NNEvolutionRule
from random import randint
from opensimplex import OpenSimplex


class CA:
    """Defines a CA withing the context of the wildfire simulation."""

    STATE_COLORMAP = ListedColormap(['green', 'orange', 'black', 'grey'])

    def __init__(self, grid, evolution_rule, alt_seed=1):
        """
        Construct a CA.

        Args:
        - grid: The grid containing the cells
        - evolution rule: Defines how the ca evolves over time
        """

        self.grid = grid
        self.evolution_rule = evolution_rule
        self.gen = OpenSimplex(seed=alt_seed)

        # Generate altitudes for all the cells and set them
        self.generate_altitudes()

    def step(self):
        """Evolve the CA to the next step."""

        # For the purpose of creating a grid with proper borders, we pad it
        # with non-flammable cells
        grid = np.pad(self.grid, 1, 'constant', constant_values=Cell(3))

        new_grid = []
        height, width = grid.shape
        for y in range(1, height-1):
            row = []
            for x in range(1, width-1):
                cell = self.evolution_rule.evolve(
                    grid[y, x], grid[y-1:y+2, x-1:x+2]
                )
                row.append(cell)

            new_grid.append(row)
        self.grid = np.array(new_grid)

    def grid_as_ints(self):
        """Return the CA grid as integers representing the states"""

        return np.array([[cell.state for cell in row] for row in self.grid])

    def generate_altitudes(self):
        for y, row in enumerate(self.grid, 1):
            for x, cell in enumerate(row, 1):
                cell.alt = self.generate_altitude(x, y, 3)

    def generate_altitude(self, x, y, freq=1):
        """Generate an altitude for a coordinate."""
        h, w = self.grid.shape
        nx, ny = x / w - 0.5, y / h - 0.5

        return self.gen.noise2d(freq * nx, freq * ny) / 2.0 + 0.5

    def from_file(filename, evolution_rule, alt_seed=1):
        """
        Create a CA using a grid file.

        Args:
        - filenme: Path to the file the read the CA grid from
        - evolution_rule: Evolution rule to use to evolve the cells
        - alt_seed: Seed for the altitude generator
        """
        grid = CA.read_from_file(filename)

        return CA(grid, evolution_rule, alt_seed)

    def read_from_file(filename):
        """
        Read a CA from a file.

        Args:
        - filename: Path to the file to read the CA grid from
        """
        grid = []

        try:
            with open(filename, "r") as grid_file:
                for y, line in enumerate(grid_file, 1):
                    # Strip of any leading and trailing whitespace
                    line = line.strip()

                    # Ignore empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    cells = [Cell(int(s), (x, y)) for x, s in enumerate(line)]
                    grid.append(cells)

            # make it into a numpy array for faster accessing
            grid = np.array(grid)

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
        if not type(grid) is np.ndarray or not grid.ndim == 2:
            raise CAGridInvalidError("Grid should be a 2D Numpy array")

        if not all(isinstance(cell, Cell) for line in grid for cell in line):
            raise CAGridInvalidError("Grid should contain State objects.")

        if not all(len(line) == len(grid[0]) for line in grid):
            raise CAGridInvalidError("Grid should be rectangular")


class CAGridInvalidError(ValueError):
    """Raised when a CA grid is invalid."""

    pass
