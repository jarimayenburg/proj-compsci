#! /usr/bin/env python3
"""Entry point of the wildfire simulation."""

import sys
from simulation import Simulation


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: {} <grid_filename> [interval]".format(sys.argv[0]))
        sys.exit(1)

    if len(sys.argv) > 2:
        interval = int(sys.argv[2])
    else:
        interval = 100

    sim = Simulation(sys.argv[1], interval)
    sim.run()
