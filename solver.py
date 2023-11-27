from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict, deque

#  1  procedure BFS(G, root) is
#  2      let Q be a queue
#  3      label root as explored
#  4      Q.enqueue(root)
#  5      while Q is not empty do
#  6          v := Q.dequeue()
#  7          if v is the goal then
#  8              return v
#  9          for all edges from v to w in G.adjacentEdges(v) do
# 10              if w is not labeled as explored then
# 11                  label w as explored
# 12                  w.parent := v
# 13                  Q.enqueue(w)


def adjacent_paths(maze, cell, n, m):
    x, y = cell
    cell_path = []

    # bottom neighbours
    if y + 1 < m:
        if maze[x, y + 1] == 0:
            cell_path.append((x, y + 1))

    # top neighbours
    if y - 1 >= 0:
        if maze[x, y - 1] == 0:
            cell_path.append((x, y - 1))

    # left neighbour
    if x - 1 >= 0:
        if maze[x - 1, y] == 0:
            cell_path.append((x - 1, y))

    # right neighbour
    if x + 1 < n:
        if maze[x + 1, y] == 0:
            cell_path.append((x + 1, y))

    return cell_path


maze = np.loadtxt("maze.out", delimiter=",")
width, height = maze.shape


def maze_BFS(maze, root, goal):
    queue = deque()
    visited = set(root)
    parents = defaultdict(tuple)

    queue.append(root)

    while queue != deque():
        cell = queue.popleft()

        if cell == goal:
            return cell

        for edge in adjacent_paths(maze, cell, width, height):
            if edge not in visited:
                visited.add(edge)
                parents[edge] = cell
                queue.append(edge)

    return parents


maze_path = maze

goal = (width, height)
root = (0, 0)
paths = maze_BFS(maze, root, goal)

end = (39, 39)

shortest_path = []
cell_path = end

while cell_path != root:
    cell_path = paths[cell_path]
    path_x, path_y = cell_path
    maze_path[path_x, path_y] = -1

    shortest_path.append(cell_path)

print(shortest_path)

fig = plt.imshow(maze_path, cmap="gist_gray_r")
plt.axis("off")
fig.axes.get_xaxis().set_visible(False)
fig.axes.get_yaxis().set_visible(False)
plt.savefig(f"maze_solved_2.png", bbox_inches="tight", dpi=300, pad_inches=0)
