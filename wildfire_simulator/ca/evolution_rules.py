"""Contains a class defining how to evolve a CA."""
from .cell import Cell
import random
import numpy as np
import math


class NNEvolutionRule:
    """Defines how to evolve a CA using nearest neighbor."""
    
    # Base probability of a cell igniting
    p0 = 0.50

    def evolve(self, orig_cell, neighborhood, wind_dir, wind_speed):
        """Evolve a cell in a CA."""

        # Create a copy of the original cell
        cell = orig_cell.copy()

        if cell.state == 1:
            cell.state = 2
        elif cell.state == 0:
            # check for each cell in the neighborhood
            for y in range(len(neighborhood)):
                for x in range(len(neighborhood[y])):

                    # skip if we are lookng at the current cell
                    if x == 1 and y == 1:
                        continue
                    # if the neighbor is not burning, we skip
                    if not neighborhood[y, x].state == 1:
                        continue

                    # get the angle between the burning neightbour and the wind
                    # direction
                    pos = np.array([y-1, x-1])
                    pos = pos / np.linalg.norm(pos)
                    theta_w = np.arccos(np.dot(pos, wind_dir))

                    # get the probability that the current cell will ignite
                    p = self.pburn(cell, theta_w, wind_speed)

                    rand = random.random()

                    if p < rand:
                        cell.state = 1
                        return cell

        # we are done
        return cell

    def pburn(self, cell, theta_w, wind_speed):
        """Probability that a cell will start buring."""
        pv = self.pveg(cell)
        pd = self.pdens(cell)
        pw = self.pwind(theta_w, wind_speed)
        ps = self.pslope()

        return NNEvolutionRule.p0 * (1 + pv) * (1 + pd) * pw * ps

    def pwind(self, theta_w, wind_speed, c1=0.045, c2=0.131):
        """Wind coeffiecient of fire spread."""
        return np.exp(wind_speed * (c1 * c2 * (np.cos(theta_w - 1))))

    def pslope(self):
        """Slope coefficient of fire spread."""
        return 1

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
