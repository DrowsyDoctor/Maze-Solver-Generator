from generation import * 
from collections import deque

def neighboring_cells(maze, current_row, current_col):
    neighbors = []

    directions = [(1, 0), 
                (-1, 0), 
                (0, -1), 
                (0, 1)]  

    for direction in directions:
        neighbor_row = current_row + direction[0]
        neighbor_col = current_col + direction[1]

        if (0 <= neighbor_row < len(maze)) and (0 <= neighbor_col < len(maze[0])):
            if maze[neighbor_row][neighbor_col] != 1:  # Check if it's a path
                neighbors.append((neighbor_row, neighbor_col))

    return neighbors


def find_goal(maze):
    """Find the goal position (cell with value 2) in the maze"""
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 2:
                return (row, col)
    return None


def floodfill(maze, goal_row, goal_col):
    rows = len(maze)
    cols = len(maze[0])
    distances = [[float('inf')] * cols for _ in range(rows)]

    distances[goal_row][goal_col] = 0 
    queue = deque([(goal_row, goal_col)])
    visited = set()

    while queue: 
        current = queue.popleft()
        
        if current in visited:
            continue
        visited.add(current)

        neighbors = neighboring_cells(maze, current[0], current[1])

        for neighbor in neighbors:
            if distances[neighbor[0]][neighbor[1]] > distances[current[0]][current[1]] + 1:
                distances[neighbor[0]][neighbor[1]] = distances[current[0]][current[1]] + 1
                queue.append(neighbor)

    return distances


def mouse(goal_row, goal_col, start_pos, large_maze):
    current_row, current_col = start_pos
    path = [(current_row, current_col)]

    distances = floodfill(large_maze, goal_row, goal_col)

    while (current_row, current_col) != (goal_row, goal_col):
        min_distance = float('inf')
        next_row = None
        next_col = None

        neighbors = neighboring_cells(large_maze, current_row, current_col)

        for neighbor in neighbors:
            if distances[neighbor[0]][neighbor[1]] < min_distance:
                min_distance = distances[neighbor[0]][neighbor[1]]
                next_row, next_col = neighbor

        if next_row is None:
            print("No path to goal found!")
            return None

        current_row = next_row
        current_col = next_col
        path.append((current_row, current_col))
    
    return path