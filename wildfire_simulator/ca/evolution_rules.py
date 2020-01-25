"""Contains a class defining how to evolve a CA."""
from .cell import Cell
import random
# FLAMMABLE = 0
# BURNING = 1
# BURNED_OUT = 2
# NON_FLAMMABLE = 3

class NNEvolutionRule:
    """Defines how to evolve a CA using nearest neighbor."""

    def evolve(self, cell, neighborhood):
        """Evolve a cell in a CA."""

        ret_cell = Cell(cell.state, cell.veg, cell.dens)

        if cell.state is 1:
            ret_cell.state = 2
        elif cell.state is 0:
            burning = 0

            for row in neighborhood:
                for elem in row:
                    if elem.state is 1:
                        burning += 1

            p = self.pburn(cell, neighborhood)**burning

            rand = random.random()

            if p < rand:
                ret_cell.state = 1

        return ret_cell

    def pburn(self, cell, neighborhood):
        """Probability that a cell will start buring."""
        p0 = 0.58
        pv = self.pveg(cell)
        pd = self.pdens(cell)
        pw = self.pwind()
        ps = self.pslope()
        return p0 * (1 + pv) * (1 + pd) * pw * ps

    def pwind(self):
        """Wind coeffiecient of fire spread."""
        return 1

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
