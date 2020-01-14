#
# Defines a CA within the context of the simulation
#

class CA:
    def __init__(self, grid_size):
        self.grid_size = grid_size

    def init_grid(self, size):
        # TODO build the initial grid from a file

        return [[0] * size] * size
