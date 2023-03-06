"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

# If you'd like to see better performance at the animation, comment lines 262-288.

import sys, argparse
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]
isFirst = True

# PATTERN TYPES DECLARATION #
##### STILL LIFES #####
block = np.array([
    [0, 0, 0, 0],
    [0, 255, 255, 0],
    [0, 255, 255, 0],
    [0, 0, 0, 0]
])

beehive = np.array([
    [0, 255, 255, 0],
    [255, 0, 0, 255],
    [0, 255, 255, 0]
])

loaf = np.array([
    [0, 255, 255, 0],
    [255, 0, 0, 255],
    [0, 255, 0, 255],
    [0, 0, 255, 0]
])

boat = np.array([
    [255, 255, 0],
    [255, 0, 255],
    [0, 255, 0]
])

tub = np.array([
    [0, 255, 0],
    [255, 0, 255],
    [0, 255, 0]
])

##### OSCILATORS #####

blinker1 = np.array([
    [0, 255, 0],
    [0, 255, 0],
    [0, 255, 0]
])

blinker2 = np.array([
    [0, 255, 0],
    [0, 255, 0],
    [0, 255, 0]
])

toad1 = np.array([
    [0, 0, 255, 0],
    [255, 0, 0, 255],
    [255, 0, 0, 255],
    [0, 255, 0, 0]
])

toad2 = np.array([
    [0, 0, 0, 0],
    [0, 255, 255, 255],
    [255, 255, 255, 0],
    [0, 0, 0, 0]
])

beacon1 = np.array([
    [255, 255, 0, 0],
    [255, 255, 0, 0],
    [0, 0, 255, 255],
    [0, 0, 255, 255]
])

beacon2 = np.array([
    [255, 255, 0, 0],
    [255, 0, 0, 0],
    [0, 0, 0, 255],
    [0, 0, 255, 255]
])

##### SPACESHIPS #####

glider1 = np.array([
    [0, 255, 0], 
    [0, 0, 255], 
    [255, 255, 255]
])

glider2 = np.array([
    [255, 0, 255], 
    [0, 255, 255], 
    [0, 255, 0]
])

glider3 = np.array([
    [0, 0, 255], 
    [255, 0, 255], 
    [0, 255, 255]
])

glider4 = np.array([
    [255, 0, 0], 
    [0, 255, 255], 
    [255, 255, 0]
])

lw_sp1 = np.array([
    [255, 0, 0, 255, 0],
    [0, 0, 0, 0, 255],
    [255, 0, 0, 0, 255],
    [0, 255, 255, 255, 255]
])

lw_sp2 = np.array([
    [0, 0, 255, 255, 0],
    [255, 255, 0, 255, 255],
    [255, 255, 255, 255, 0],
    [0, 255, 255, 0, 0]
])

lw_sp3 = np.array([
    [0, 0, 255, 255, 0],
    [255, 255, 0, 255, 255],
    [255, 255, 255, 255, 0],
    [0, 255, 255, 0, 0]
])

lw_sp4 = np.array([
    [0, 255, 255, 255, 255],
    [255, 0, 0, 0, 255],
    [0, 0, 0, 0, 255],
    [255, 0, 0, 255, 0]
])

def writeSimulationDate():
    # Take actual date
    now = datetime.now()
    
    # Write in file
    f = open("output.txt", "w")
    f.write("Simulation at " + now.strftime("%Y-%m-%d")+"\n")
    f.write("Universe size " + str(width) + " x " + str(height)+"\n")
    f.write("\n")
    f.close()

def readInput():
    file = open("input.txt", "r")

    global width, height, generations, cells
    cells = []

    # Read file
    for index, line in enumerate(file):
        # Take width and height from first line.
        if(index == 0):
            width, height = line.split(" ")
            width = int(width)
            height = int(height)
        
        # Take the generations from second line.
        if(index == 1):
            generations = int(line)

        # Get every cell and add them to a list.
        if(index >= 2):
            x, y = line.split(" ")
            y = y.strip("\n")
            cells.append(str(x) + " " + str(y))

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def createGrid(grid):
    newGrid = grid.copy()
    for cell in cells:
        cell = cell.split(" ")
        x = int(cell[0])
        y = int(cell[1])

        newGrid[x, y] = ON

    return newGrid

def countPatterns(grid, pattern):
    found = 0

    pattern = np.array(pattern)
    height, width = pattern.shape

    for i in range(grid.shape[0] - height + 1):
        for j in range(grid.shape[1] - width + 1):
            if np.all(grid[i:i+height, j:j+width] == pattern):
                found += 1

    return found

def getTotalCount(grid):
    blocks = countPatterns(grid, block)
    beehives = countPatterns(grid, beehive)
    loaves = countPatterns(grid, loaf)
    boats = countPatterns(grid, boat)
    tubs = countPatterns(grid, tub)
    blinkers = countPatterns(grid, blinker1) + countPatterns(grid, blinker2)
    toads = countPatterns(grid, toad1) + countPatterns(grid, toad2)
    beacons = countPatterns(grid, beacon1) + countPatterns(grid, beacon2)
    gliders = countPatterns(grid, glider1) + countPatterns(grid, glider2) + countPatterns(grid, glider3) + countPatterns(grid, glider4)
    lw_sp = countPatterns(grid, lw_sp1) + countPatterns(grid, lw_sp2) + countPatterns(grid, lw_sp3) + countPatterns(grid, lw_sp4)
    
    t = blocks + beehives + loaves + boats + tubs + blinkers + toads + beacons + gliders + lw_sp
    count = [blocks, beehives, loaves, boats, tubs, blinkers, toads, beacons, gliders, lw_sp, t]
    percentages = [percent(blocks, t), percent(beehives, t), percent(loaves, t), percent(boats, t), percent(tubs, t),
                   percent(blinkers, t), percent(toads, t), percent(beacons, t), percent(gliders, t), percent(lw_sp, t)]

    return count, percentages

def percent(num, total):
    if total == 0:
        return 0
    
    return (num*100)/total

def update(frameNum, img, grid, N):
    # Stop animation when max generations are reached
    if frameNum == generations-1:
        animation.pause()

    # Apply GoL rules.
    newGrid = grid.copy()

    for i in range(height):
        for j in range(width):
            neighbours = (grid[i, (j-1)%width] + grid[i, (j+1)%width] + 
                    grid[(i-1)%height, j] + grid[(i+1)%width, j] + 
                    grid[(i-1)%height, (j-1)%width] + grid[(i-1)%height, (j+1)%width] + 
                    grid[(i+1)%height, (j-1)%width] + grid[(i+1)%height, (j+1)%width])/255
            
            if grid[i, j]  == ON:
                # Any cell with less than 2 neighbours will die as underpopulation.
                # Any cell with more than 3 neighbours will die as overpopulation.
                if (neighbours < 2) or (neighbours > 3):
                    newGrid[i, j] = OFF
            else:
                # Any cell with 3 living neighbours becomes a living cell as in reproduction.
                if neighbours == 3:
                    newGrid[i, j] = ON
    
    count, percent = getTotalCount(newGrid)

    global isFirst

    # Write in file.
    if not isFirst:
        f = open("output.txt", "a")
        f.write("Iteration: " + str(frameNum)+"\n")
        f.write("---------------------------------\n")
        f.write("              | Count | Percent |\n")
        f.write(" Block        |  " + str(count[0]) + "    |  " + str(percent[0]) + "      |\n")
        f.write(" Beehive      |  " + str(count[1]) + "    |  " + str(percent[1]) + "      |\n")
        f.write(" Loaf         |  " + str(count[2]) + "    |  " + str(percent[2]) + "      |\n")
        f.write(" Boat         |  " + str(count[3]) + "    |  " + str(percent[3]) + "      |\n")
        f.write(" Tub          |  " + str(count[4]) + "    |  " + str(percent[4]) + "      |\n")
        f.write(" Blinker      |  " + str(count[5]) + "    |  " + str(percent[5]) + "      |\n")
        f.write(" Toad         |  " + str(count[6]) + "    |  " + str(percent[6]) + "      |\n")
        f.write(" Beacon       |  " + str(count[7]) + "    |  " + str(percent[7]) + "      |\n")
        f.write(" Glider       |  " + str(count[8]) + "    |  " + str(percent[8]) + "      |\n")
        f.write(" LG sp ship   |  " + str(count[9]) + "    |  " + str(percent[9]) + "      |\n")
        f.write("---------------------------------\n")
        f.write(" TOTAL        |  " + str(count[10]) + "    |         |\n")
        f.write("---------------------------------\n")
        f.write("\n")
        f.close()
    else:
        isFirst = False

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # Will fix a bug where 1st iteration is printed twice
    global isFirst 
    isFirst = True

    # Read input file and set program.
    readInput()
    
    # set grid size
    N = width if width > height else height
        
    # set animation update interval
    updateInterval = 50

    # declare grid
    grid = np.array([])
    # Create grid with the correct dimensions
    grid = np.random.choice(vals, width*height, p=[0.2, 0.8]).reshape(height, width)
    # Fix grid and clean it
    grid = np.zeros_like(grid)
    # Populate grid with input on/off
    grid = createGrid(grid)
    
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames = generations,
                                  interval=updateInterval,
                                  save_count=50)

    writeSimulationDate()

    plt.show()

# call main
if __name__ == '__main__':
    main()