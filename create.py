import random
import numpy as np

grid_size = 10
grid = np.zeros((grid_size, grid_size), dtype=int)

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def is_valid_placement(grid, x, y):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[nx, ny] == 1:
            return False
    return True


def gm(grid_size):
    stack = []
    start_x, start_y = (
        random.randint(1, grid_size // 2) * 2,
        random.randint(1, grid_size // 2) * 2,
    )
    grid[start_x, start_y] = 1

    stack.append((start_x, start_y))

    # While there are still positions to visit (DFS)
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[nx, ny] == 0:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            grid[nx, ny] = 1
            grid[x + (nx - x) // 2, y + (ny - y) // 2] = 1
            stack.append((nx, ny))
        else:
            stack.pop()

    return grid
