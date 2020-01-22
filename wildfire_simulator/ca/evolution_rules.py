"""Contains a class defining how to evolve a CA."""


class NNEvolutionRule:
    """Defines how to evolve a CA using nearest neighbor."""

    def evolve(self, cell, neighborhood):
        """Evolve a cell in a CA."""

    def pburn(self):
        """Probability that a cell will start buring"""
        # TODO: Implementation

    def pveg(self, veg):
        """ """
        if veg is noveg:
            return -1
        elif veg is agriculture:
            return -0.4
        elif veg is forest or veg is Shrubland:
            return 0.4
        else:
            raise Error

    def pdens(self, veg):
        """Density coefficient for the spread of forest fires"""
        if veg is noveg:
                return -1
        elif veg is sparse:
            return -0.3
        elif veg is normal:
            return 0
        elif veg is dense:
            return 0.3
        else:
            raise Error
