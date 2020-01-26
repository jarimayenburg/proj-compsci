"""Contains a class defining how to evolve a CA."""
from .cell import Cell
import random
import numpy as np
import math
# FLAMMABLE = 0
# BURNING = 1
# BURNED_OUT = 2
# NON_FLAMMABLE = 3

class NNEvolutionRule:
    """Defines how to evolve a CA using nearest neighbor."""

    def evolve(self, cell, neighborhood, wind_dir, wind_speed):
        """Evolve a cell in a CA."""

        ret_cell = Cell(cell.state, cell.veg, cell.dens)

        if cell.state is 1:
            ret_cell.state = 2
        elif cell.state is 0:
            p = 1
            burningneighbors = 0

            for x in range(len(neighborhood)):
                for y in range(len(neighborhood[x])):

                    # skip if we are lookng at the current cell
                    if x is 1 and y is 1:
                        continue
                    if not neighborhood[x,y].state is 1:
                        continue

                    burningneighbors += 1

                    old_pos = np.array([x-1, y-1])

                    pos = old_pos / np.linalg.norm(old_pos)

                    theta_w = np.arccos(np.dot(pos, wind_dir))

                    p *= self.pburn(cell, theta_w, wind_speed)

            if burningneighbors > 0:
                rand = random.random()

                if rand < p:
                    ret_cell.state = 1

        return ret_cell

    def pburn(self, cell, theta_w, wind_speed):
        """Probability that a cell will start buring."""
        p0 = 0.58
        pv = self.pveg(cell)
        pd = self.pdens(cell)
        pw = self.pwind(theta_w, wind_speed)
        ps = self.pslope()

        return p0 * (1 + pv) * (1 + pd) * pw * ps

    def pwind(self, theta_w, wind_speed, c1=0.045, c2=0.131):
        """Wind coeffiecient of fire spread."""
        return np.exp(wind_speed * (c1 *c2 * (np.cos(theta_w - 1))))

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
