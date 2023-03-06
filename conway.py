"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

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
]),

loaf = np.array([
    [0, 255, 255, 0],
    [255, 0, 0, 255],
    [0, 255, 0, 255],
    [0, 0, 255, 0]
]),

boat = np.array([
    [255, 255, 0],
    [255, 0, 255],
    [0, 255, 0]
]),

tub = np.array([
    [0, 255, 0],
    [255, 0, 255],
    [0, 255, 0]
]),

##### OSCILATORS #####

blinker1 = np.array([
    [0, 255, 0],
    [0, 255, 0],
    [0, 255, 0]
]),

blinker2 = np.array([
    [0, 255, 0],
    [0, 255, 0],
    [0, 255, 0]
]),

toad1 = np.array([
    [0, 0, 255, 0],
    [255, 0, 0, 255],
    [255, 0, 0, 255],
    [0, 255, 0, 0]
]),

toad2 = np.array([
    [0, 0, 0, 0],
    [0, 255, 255, 255],
    [255, 255, 255, 0],
    [0, 0, 0, 0]
]),

beacon1 = np.array([
    [255, 255, 0, 0],
    [255, 255, 0, 0],
    [0, 0, 255, 255],
    [0, 0, 255, 255]
]),

beacon2 = np.array([
    [255, 255, 0, 0],
    [255, 0, 0, 0],
    [0, 0, 0, 255],
    [0, 0, 255, 255]
]),

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

def update(frameNum, img, grid, N):
    # Write in file.
    f = open("output.txt", "a")
    f.write("Iteration: " + str(frameNum)+"\n")
    f.write("---------------------------------\n")
    f.write(" Block        | Count | Percent |\n")
    f.write(" Beehive      |  0    |  0      |\n")
    f.write(" Loaf         |  0    |  0      |\n")
    f.write(" Boat         |  0    |  0      |\n")
    f.write(" Tub          |  0    |  0      |\n")
    f.write(" Blinker      |  0    |  0      |\n")
    f.write(" Toad         |  0    |  0      |\n")
    f.write(" Beacon       |  0    |  0      |\n")
    f.write(" Glider       |  0    |  0      |\n")
    f.write(" LG sp ship   |  0    |  0      |\n")
    f.write("---------------------------------\n")
    f.write(" TOTAL        |  0    |         |\n")
    f.write("---------------------------------\n")
    f.write("\n")
    f.close()

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

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
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