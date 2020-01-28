"""Contains a class defining how to evolve a CA."""
from .cell import Cell
import random
import numpy as np
import math


class NNEvolutionRule:
    """Defines how to evolve a CA using nearest neighbor."""

    def __init__(self, p0=0.58, wind_dir=np.array([1, 1]), wind_speed=5):
        """
        Construct the NNEvolutionRule.

        Params:
        - p0: Base probability of a cell igniting.
        - wind_dir: Direction of the wild, note that this is a vector. We do
                    this because later, we have to calculate the angle between
                    a burning cell, its neighbor and the wind
        - wind_speed: The wind speed in meters per second
        """
        self.p0 = p0
        self.wind_dir = wind_dir / np.linalg.norm(wind_dir)
        self.wind_speed = wind_speed

    def evolve(self, orig_cell, neighborhood):
        """Evolve a cell in a CA."""

        # Create a copy of the original cell
        cell = orig_cell.copy()

        #  if the cell is burning, it will have died out in the next frame
        if cell.state == 1:
            cell.state = 2
        elif cell.state == 0:
            # Check for each cell in the neighborhood
            for y in range(len(neighborhood)):
                for x in range(len(neighborhood[y])):

                    # Skip if we are looking at the current cell
                    if x == 1 and y == 1:
                        continue
                    # If the neighbor is not burning, we skip
                    if not neighborhood[y, x].state == 1:
                        continue

                    # Get the probability that the current cell will ignite
                    p = self.pburn(cell, neighborhood[y, x])

                    rand = random.random()
                    if rand < p:
                        cell.state = 1
                        return cell

        # we are done
        return cell

    def pburn(self, cell, neighbor_cell):
        """Probability that a cell will start buring."""
        pv = self.pveg(cell)
        pd = self.pdens(cell)
        pw = self.pwind(cell, neighbor_cell)
        ps = self.pslope(cell, neighbor_cell)

        return self.p0 * (1 + pv) * (1 + pd) * pw * ps

    def pwind(self, cell, neighbor_cell, c1=0.045, c2=0.131):
        """Wind coeffiecient of fire spread."""

        x, y = cell.pos
        nx, ny = neighbor_cell.pos

        # The burn direction is the vector from the burning
        # neighbor to the cell.
        burn_dir = np.array([x - nx, y - ny])
        burn_dir = burn_dir / np.linalg.norm(burn_dir)

        # Get the angle between the burn direction and the wind direction
        theta_w = np.arccos(np.dot(burn_dir, self.wind_dir))

        return np.exp(self.wind_speed * (c1 * c2 * (np.cos(theta_w - 1))))

    def pslope(self, cell, neighbor_cell, a_s=0.078):
        """Slope coefficient of fire spread."""

        # Difference in altitude
        alt_diff = neighbor_cell.alt - cell.alt

        # Horizontal distance between the cells.
        x, y = cell.pos
        nx, ny = neighbor_cell.pos
        dx, dy = nx - x, ny - y
        cell_dist = np.sqrt(dx**2 + dy**2) * Cell.diameter

        # Slope angle of the terrain.
        theta_s = np.arctan(alt_diff / cell_dist)

        return np.exp(theta_s * a_s)

    def pveg(self, cell):
        """Vegitation coeffiecient of fire spread."""
        veg = cell.veg

        if veg == 'nov':
            return -1
        elif veg == 'agr':
            return -0.4
        elif veg == 'for' or veg == 'shr':
            return 0.4
        else:
            raise ValueError('Invalid vegitation type')

    def pdens(self, cell):
        """Density coefficient for the spread of forest fires."""
        dens = cell.dens

        if dens == 'nov':
            return -1
        elif dens == 'spa':
            return -0.3
        elif dens == 'nor':
            return 0
        elif dens == 'den':
            return 0.3
        else:
            raise ValueError('Invalid vegitation density')
