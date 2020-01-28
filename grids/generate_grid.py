#! /usr/bin/env python3
#
# Generates a gridfile for the simulation to use

import json, argparse
import numpy as np

def read_gridfile(gridfile_name):
    grid = []
    with open(gridfile_name) as f:
        for line in f:
            line = line.strip()

            # Comments and white lines
            if not line or line.startswith('#'):
                continue

            grid.append(line.split(' '))

    return np.array(grid)

parser = argparse.ArgumentParser(description='Generate a file for the simulation to use. Outputs this file as JSON to stdout')
parser.add_argument("-w", "--wind-speed", type=int, help="wind speed in m/s", default='5')
parser.add_argument("-d", "--wind-dir", help="wind direction as a vector x,y", default='1,1')
parser.add_argument("-s", "--seed", type=int, help="seed for terrain generation", default='20')
parser.add_argument("vegitation_gridfile", help="grid file with vegitation information")
parser.add_argument("density_gridfile", help="grid file with density information")
parser.add_argument("state_gridfile", help="grid file with state information")

# Parse the arguments
args = parser.parse_args()

# Format the wind direction vector
wind_dir = tuple(map(int, args.wind_dir.split(',')))

# Read the files into numpy arrays
vegs = read_gridfile(args.vegitation_gridfile)
dens = read_gridfile(args.density_gridfile)
states = read_gridfile(args.state_gridfile)

if not (vegs.shape == dens.shape == states.shape):
    raise ValueError("Invalid grid files, should be equal shape")

# Build the grid
grid = []
h, w = vegs.shape
for y in range(h):
    row = []
    for x in range(w):
        cell = {}
        cell['veg'] = vegs[y, x]
        cell['den'] = dens[y, x]
        cell['sta'] = states[y, x]
        
        row.append(cell)
    grid.append(row)

retval = {}
retval['wind_dir'] = wind_dir
retval['wind_speed'] = args.wind_speed
retval['seed'] = args.seed
retval['grid'] = grid

# Print JSON to stdout
print(json.dumps(retval))
