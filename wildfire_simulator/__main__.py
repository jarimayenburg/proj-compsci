#! /usr/bin/env python3
"""Entry point of the wildfire simulation."""

import sys
from simulation import Simulation


if __name__ == '__main__':
    if not (len(sys.argv) > 1 and len(sys.argv) < 4):
        print("Usage: {} <grid_filename> [seed]".format(sys.argv[0]))
        sys.exit(1)

    # Default seed if not specified
    if len(sys.argv) < 3:
        seed = 1
    else:
        seed = int(sys.argv[2])

    sim = Simulation(sys.argv[1], seed=seed)
    sim.run()
