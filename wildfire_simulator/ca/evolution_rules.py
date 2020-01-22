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
        else if veg is agriculture:
            return -0.4
        else if veg is forest or veg is Shrubland:
            return 0.4
        else:
            raise Error
    def pdens(self, veg):
        if veg is noveg:
                return -1
        else if veg is sparse:
            return -0.3
        else if veg is normal:
            return 0
        else if veg is dense:
            return 0.3
        else:
            raise Error
