#
# Contains the simulation class, the outermost class of the whole simulation.
#

from ca import CA

class Simulation:
    def __init__(self, grid_size=100):
        self.ca = CA(grid_size)

    def run(self):
        pass
