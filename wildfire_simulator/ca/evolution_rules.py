"""Contains a class defining how to evolve a CA."""


class NNEvolutionRule:
    """Defines how to evolve a CA using nearest neighbor."""

    def evolve(self, cell, neighborhood):
        """Evolve a cell in a CA."""

    def pburn(self, cell):
        """Probability that a cell will start buring"""
        p0 = 0.58
        pv = self.pveg(cell)
        pd = self.pdens(cell)
        pw = self.pwind()
        ps = self.pslope()
        return p0 * (1 + pv) * (1 + pd) * pw * ps

    def pwind(self):
        """Wind coeffiecient of fire spread:"""
        return 1

    def pslope(self):
        """Slope coefficient of fire spread"""
        return 1

    def pveg(self, cell):
        """vegitation coeffiecient of fire spread"""
        #  TODO: get veg index
        veg = 'forst'
        if veg is 'noveg':
            return -1
        elif veg is 'agriculture':
            return -0.4
        elif veg is 'forest' or veg is 'Shrubland':
            return 0.4
        else:
            raise Exception('invalid vegitation type')

    def pdens(self, cell):
        """Density coefficient for the spread of forest fires"""
        # TODO: get dens index
        dens = 'normal'
        if dens is 'noveg':
                return -1
        elif dens is 'sparse':
            return -0.3
        elif dens is 'normal':
            return 0
        elif dens is 'dense':
            return 0.3
        else:
            raise Exception('invalid vegitation density')
