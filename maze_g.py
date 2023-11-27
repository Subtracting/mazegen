# This algorithm is a randomized version of Prim's algorithm.

#     Start with a grid full of walls.
#     Pick a cell, mark it as part of the maze. Add the walls of the cell to the wall list.
#     While there are walls in the list:
#         Pick a random wall from the list. If only one of the cells that the wall divides is visited, then:
#             Make the wall a passage and mark the unvisited cell as part of the maze.
#             Add the neighboring walls of the cell to the wall list.
#         Remove the wall from the list.


import imageio
from matplotlib import pyplot as plt
import numpy as np
from random import randint, choice

GIF_GENERATOR = False

n = 100
m = 100

shape = (n, m)
maze = np.ones(shape, dtype=int)

wall_list = set()


def get_walls_cell(x, y, add):
    cell_walls = []
    visited = 0
    diag_visited = 0
    visited_coord = []

    # bottom neighbours
    if x - 1 >= 0 and y + 1 < m:
        if maze[x - 1, y + 1] == 1:
            cell_walls.append((x - 1, y + 1))
        else:
            diag_visited += 1
    if y + 1 < m:
        if maze[x, y + 1] == 1:
            cell_walls.append((x, y + 1))
        else:
            visited += 1
            visited_coord.append((x, y + 1))
    if x + 1 < n and y + 1 < m:
        if maze[x + 1, y + 1] == 1:
            cell_walls.append((x + 1, y + 1))
        else:
            diag_visited += 1

    # top neighbours
    if x - 1 >= 0 and y - 1 >= 0:
        if maze[x - 1, y - 1] == 1:
            cell_walls.append((x - 1, y - 1))
        else:
            diag_visited += 1
    if y - 1 >= 0:
        if maze[x, y - 1] == 1:
            cell_walls.append((x, y - 1))
        else:
            visited += 1
            visited_coord.append((x, y - 1))

    if x + 1 < n and y - 1 >= 0:
        if maze[x + 1, y - 1] == 1:
            cell_walls.append((x + 1, y - 1))
        else:
            diag_visited += 1

    # left neighbour
    if x - 1 >= 0:
        if maze[x - 1, y] == 1:
            cell_walls.append((x - 1, y))
        else:
            visited += 1
            visited_coord.append((x - 1, y))

    # right neighbour
    if x + 1 < n:
        if maze[x + 1, y] == 1:
            cell_walls.append((x + 1, y))
        else:
            visited += 1
            visited_coord.append((x + 1, y))

    if add == True:
        for wall in cell_walls:
            wall_list.add(wall)
    elif add == False and visited == 1 and diag_visited <= 1:
        maze[x, y] = 0

        visited_x, visited_y = visited_coord[0]
        direction_x = x - visited_x
        direction_y = y - visited_y
        if (
            0 <= visited_x + 2 * direction_x < n
            and 0 <= visited_y + 2 * direction_y < m
        ):
            unvisited_x = visited_x + 2 * direction_x
            unvisited_y = visited_y + 2 * direction_y
            maze[unvisited_x, unvisited_y] = 0
            try:
                wall_list.remove((unvisited_x, unvisited_y))
            except:
                pass

            get_walls_cell(unvisited_x, unvisited_y, True)
        get_walls_cell(x, y, True)


x, y = randint(0, n - 1), randint(0, m - 1)
maze[x, y] = 0

get_walls_cell(x, y, True)

i = 0
filenames = []
images = []

while wall_list != set():
    i += 1
    wall_x, wall_y = choice(list(wall_list))
    get_walls_cell(wall_x, wall_y, False)
    wall_list.remove((wall_x, wall_y))

    if i % 5 == 0 and GIF_GENERATOR == True:
        fig = plt.imshow(maze, cmap="binary")
        plt.axis("off")
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.savefig(f"maze{i}.png", bbox_inches="tight", dpi=300, pad_inches=0)
        plt.close()
        filenames.append(f"maze{i}.png")

np.savetxt(f"maze.out_{m}_{n}", maze, delimiter=",")

if GIF_GENERATOR == True:
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave("algo.gif", images)
else:
    fig = plt.imshow(maze, cmap="binary")
    plt.axis("off")
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig(f"maze_{m}_{n}.png", bbox_inches="tight", dpi=300, pad_inches=0)
