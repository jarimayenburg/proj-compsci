"""Contains a class defining how to evolve a CA."""


class NNEvolutionRule:
    """Defines how to evolve a CA using nearest neighbor."""

    def evolve(self, cell, neighborhood):
        """Evolve a cell in a CA."""
        
        return cell

    def pburn(self, cell):
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
        #  TODO: get veg index
        veg = 'for'
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
        # TODO: get dens index
        dens = 'nor'
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
