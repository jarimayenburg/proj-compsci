#! /usr/bin/env python3
"""Entry point of the wildfire simulation."""

import sys
from simulation import Simulation


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print("Usage: {} <grid_filename>".format(sys.argv[0]))
        sys.exit(1)

    sim = Simulation(sys.argv[1])
    sim.run()
