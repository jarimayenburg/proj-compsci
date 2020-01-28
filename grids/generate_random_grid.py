#! /usr/bin/env python3
#
# Generates a random gridfile for the simulation to use

import json, argparse, random, sys
import numpy as np
from opensimplex import OpenSimplex

parser = argparse.ArgumentParser(description='Uses noise maps to generate a random landscape grid for the simulation to use. Outputs a gridfile as JSON to stdout.')

parser.add_argument("-W", "--width", type=int, help="Width of the grid", default=400)
parser.add_argument("-H", "--height", type=int, help="Height of the grid", default=400)
parser.add_argument("-w", "--wind-speed", type=int, help="Wind speed in m/s", default=5)
parser.add_argument("-d", "--wind-dir", help="Wind direction as a vector x,y", default='1,1')
parser.add_argument("-s", "--seed", type=int, help="Seed for terrain generation", default=random.random())
parser.add_argument("-f", "--frequency", type=float, help="Base terrain generation frequency (defines zoom level)", default=2.0)
parser.add_argument("-e", "--alt_exp", type=float, help="Exponential for altitude generation (defines how 'hilly' the terrain is)", default=0.20)
parser.add_argument("-a", "--max-alt", type=int, help="Maximum altitude of the terrain", default=1500)
parser.add_argument("-l", "--water-level", type=float, help="Height of water (0-1)", default=0.05)
parser.add_argument("-p", "--p0", type=float, help="Base probability of cell ignition", default=0.58)

# Parse the arguments
args = parser.parse_args()

# Argument formatting
width = args.width
height = args.height
wind_speed = args.wind_speed
wind_dir = tuple(map(int, args.wind_dir.split(',')))
seed = args.seed
base_freq = args.frequency
alt_exp = args.alt_exp
max_alt = args.max_alt
water_level = args.water_level
p0 = args.p0

def plot_map(altmap, vegmap, densmap):
    """Plot the map using matplotlib"""
    global width, height, max_alt

    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = get_colormap(vegmap, densmap)

    x, y = range(width), range(height)
    X, Y = np.meshgrid(x, y)

    ax.plot_surface(X, Y, altmap, facecolors=colors)
    ax.set_zlim(0, 1)

    plt.show()

def noise(gen, x, y, fx=1, fy=1):
    """
    Generate a noise value between 0.0 and 1.0.

    Params:
    - gen: The noise generator to use
    - x: X-coordinate in the grid
    - y: Y-coordinate in the grid
    - fx: X-frequency, relative to base frequency
    - fy: Y-frequency, relative to base frequency
    """
    global width, height, base_freq

    # Apply base frequencies
    fx, fy = fx * base_freq, fy * base_freq

    nx, ny = x / width - 0.5, y / height - 0.5
    return gen.noise2d(fx * nx, fx * ny) / 2.0 + 0.5

# Seed the random number generator
random.seed(seed)

# Create the noise generators
alt_gen = OpenSimplex(seed=random.randint(-sys.maxsize, sys.maxsize))
veg_gen = OpenSimplex(seed=random.randint(-sys.maxsize, sys.maxsize))
dens_gen = OpenSimplex(seed=random.randint(-sys.maxsize, sys.maxsize))

def gen_alts():
    """Generate the altitude map"""
    global width, height, max_alt, water_level, alt_gen, alt_exp
    
    alts = np.empty((height, width), dtype=float)
    for y in range(height):
        for x in range(width):
            alt = noise(alt_gen, x, y)

            # Flatten
            alt = 1 - alt**alt_exp

            # Limit until water level
            if alt < water_level:
                alt = water_level

            alts[y, x] = alt

    return alts

def gen_vegs(altmap):
    """Generate the vegetation map"""
    global width, height, water_level, veg_gen, max_alt

    vegs = np.empty((height, width), dtype=object)
    for y in range(height):
        for x in range(width):
            alt = altmap[y, x]
            veg_mod = noise(veg_gen, x, y)

            # Water at the water level
            if alt <= water_level:
                vegs[y, x] = 'nov'
            elif alt * max_alt < 400:
                if veg_mod < 0.4:
                    vegs[y, x] = 'agr'
                elif veg_mod < 0.8:
                    vegs[y, x] = 'for'
                else:
                    vegs[y, x] = 'shr'
            elif alt * max_alt < 1000:
                if veg_mod < 0.1:
                    vegs[y, x] = 'agr'
                elif veg_mod < 0.6:
                    vegs[y, x] = 'for'
                else:
                    vegs[y, x] = 'shr'
            elif alt * max_alt < 1400:
                if veg_mod < 0.7:
                    vegs[y, x] = 'shr'
                else:
                    vegs[y, x] = 'for'
            else:
                vegs[y, x] = 'shr'

    return vegs

def gen_dens(altmap, vegmap):
    """Generate the density map"""
    global width, height, dens_gen

    dens = np.empty((height, width), dtype=object)
    for y in range(height):
        for x in range(width):
            alt = altmap[y, x]
            veg = vegmap[y, x]
            dens_mod = noise(dens_gen, x, y)

            if veg == 'nov':
                dens[y, x] = 'nov'
            elif veg == 'agr':
                dens[y, x] = 'nor'
            elif alt * max_alt < 500:
                if dens_mod < 0.4:
                    dens[y, x] = 'den'
                elif dens_mod < 0.7:
                    dens[y, x] = 'nor'
                else:
                    dens[y, x] = 'spa'
            elif alt * max_alt < 1000:
                if dens_mod < 0.2:
                    dens[y, x] = 'den'
                elif dens_mod < 0.5:
                    dens[y, x] = 'nor'
                else:
                    dens[y, x] = 'spa'
            elif alt * max_alt < 1400:
                if dens_mod < 0.05:
                    dens[y, x] = 'den'
                elif dens_mod < 0.3:
                    dens[y, x] = 'nor'
                elif dens_mod < 0.8:
                    dens[y, x] = 'spa'
                else:
                    dens[y, x] = 'nov'
            else:
                if dens_mod < 0.2:
                    dens[y, x] = 'spa'
                else:
                    dens[y, x] = 'nov'

    return dens

def gen_states(vegmap):
    """Generate initial states"""
    global width, height

    states = np.zeros((height, width), dtype=int)

    # Primitive way of finding a flammable cell
    x, y = int(width / 2), int(height / 2)
    while vegmap[y, x] == 'nov':
        x += 1

    # Ignite one cell
    states[y, x] = 1

    return states


def get_colormap(vegmap, dens_map):
    """Generate colors for vegetation map"""
    colors = np.empty((height, width), dtype=tuple)

    for y in range(height):
        for x in range(width):
            veg = vegmap[y, x]
            dens = densmap[y, x]

            if veg == 'nov':
                # Blue
                colors[y, x] = 0, 105, 148
            elif dens == 'nov':
                # Gray
                colors[y, x] = 188, 188, 188
            elif veg == 'for':
                # Forest green
                if dens == 'den':
                    colors[y, x] = 13, 72, 13
                elif dens == 'nor':
                    colors[y, x] = 59, 128, 59
                else:
                    colors[y, x] = 149, 193, 149
            elif veg == 'agr':
                # Wheat yellow
                if dens == 'den':
                    colors[y, x] = 242, 210, 50
                elif dens == 'nor':
                    colors[y, x] = 236, 221, 147
                else:
                    colors[y, x] = 210, 205, 178
            elif veg == 'shr':
                # Shrubland green
                if dens == 'den':
                    colors[y, x] = 105, 200, 105
                elif dens == 'nor':
                    colors[y, x] = 162, 220, 162
                else:
                    colors[y, x] = 192, 220, 192

            colors[y, x] = tuple([c / 255 for c in colors[y, x]])

    return colors

def build_grid(altmap, vegmap, densmap, statesmap):
    """Build the grid"""
    global width, height

    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            cell = {}
            cell['alt'] = float(altmap[y, x])
            cell['veg'] = str(vegmap[y, x])
            cell['den'] = str(densmap[y, x])
            cell['sta'] = int(statesmap[y, x])
            
            row.append(cell)
        grid.append(row)

    return grid


# Generate altitudes
altmap = gen_alts()

# Generate vegetation biomes
vegmap = gen_vegs(altmap)

# Generate density map
densmap = gen_dens(altmap, vegmap)

# Generate states map
statesmap = gen_states(vegmap)

# Build the grid
grid = build_grid(altmap, vegmap, densmap, statesmap)

retval = {}
retval['wind_dir'] = wind_dir
retval['wind_speed'] = wind_speed
retval['max_alt'] = max_alt
retval['p0'] = p0
retval['grid'] = grid

print(json.dumps(retval))
