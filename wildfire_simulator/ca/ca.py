"""Defines a CA within the context of the simulation."""

import json
import numpy as np
from matplotlib.colors import ListedColormap
from .cell import Cell
from .evolution_rules import NNEvolutionRule
from random import randint


class CA:
    """Defines a CA withing the context of the wildfire simulation."""

    def __init__(self, grid, evolution_rule, max_alt):
        """
        Construct a CA.

        Args:
        - grid: The grid containing the cells
        - evolution rule: Defines how the ca evolves over time
        - max_alt: Maximum altitude in the CA
        """

        self.grid = grid
        self.evolution_rule = evolution_rule
        self.max_alt = max_alt

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

    def grid_as_pixels(self):
        """Return the CA grid as RGB values representing the states."""

        return np.array(
            [[cell.get_color() for cell in row] for row in self.grid]
        )

    def get_altitudes(self):
        """Return the altitudes of the cells."""

        return np.array([[cell.alt for cell in row] for row in self.grid])

    def from_gridfile(filename, evolution_rule=NNEvolutionRule):
        """
        Create a CA using a grid file (JSON).

        Args:
        - filename: Path to the file the read the CA grid from
        - evolution_rule: Class to use as the evolution rule
        """
        with open(filename) as f:
            gridconf = json.loads(f.read())

            p0 = gridconf['p0']
            wind_dir = gridconf['wind_dir']
            wind_speed = gridconf['wind_speed']
            gridraw = gridconf['grid']
            max_alt = gridconf['max_alt']

            grid = CA.build_grid(gridraw, max_alt)
            er = evolution_rule(
                p0=p0, wind_dir=wind_dir, wind_speed=wind_speed
            )

            return CA(grid, er, max_alt)

    def build_grid(rawgrid, max_alt):
        """
        Import and validate the grid from the gridfile.

        Args:
        - rawgrid: The raw grid as found in the gridfile JSON
        - max_alt: Maximum altitude
        """
        try:
            grid = []
            for y, line in enumerate(rawgrid, 1):
                row = []
                for x, rawcell in enumerate(line, 1):
                    state = rawcell['sta']
                    veg = rawcell['veg']
                    dens = rawcell['den']
                    alt = rawcell['alt'] * max_alt

                    cell = Cell(
                        pos=(x, y), state=state, veg=veg, dens=dens, alt=alt
                    )

                    row.append(cell)

                grid.append(row)

            # make it into a numpy array for faster accessing
            grid = np.array(grid)

            # Validate that what's been read is a valid CA grid
            CA.validate(grid)

            return grid
        except Exception as e:
            raise ValueError("Invalid grid file") from e

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
