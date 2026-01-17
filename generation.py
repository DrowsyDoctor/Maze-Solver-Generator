import numpy as np
import random

# Default values (can be overridden in main.py)
patch_width = 21  # Must be odd
patch_height = 21  # Must be odd
width = 41 
height = 41
num_stitches = 2
num_patches_x = 3
num_patches_y = 3

def grid(width, height):
    """Create a bordered array with all cells as walls"""
    maze = [[1 for x in range(width)] for y in range(height)]
    return maze

def dfs(maze, width, height):
    """Depth-first search maze generation algorithm"""
    stack = [(1, 1)]
    maze[1][1] = 0

    while stack:
        x, y = stack[-1]
        moved = False

        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y + (dy // 2)][x + (dx // 2)] = 0
                maze[ny][nx] = 0
                
                stack.append((nx, ny))
                moved = True
                break 

        if not moved:
            stack.pop()

    return maze

def place_patch(large_maze, patch, start_row, start_col):
    """Copy a patch into the large maze at the specified coordinates"""
    patch_height = len(patch)
    patch_width = len(patch[0])
    for y in range(patch_height):
        for x in range(patch_width):
            large_maze[start_row + y][start_col + x] = patch[y][x]

def find_stitch(large_maze, patch1_bounds, patch2_bounds, direction, search_range):
    """Find possible stitch locations between two patches"""
    stitch_points = []

    if direction == 'horizontal':
        row1, col1 = patch1_bounds
        row2, col2 = patch2_bounds

        for offset in range(-search_range, search_range + 1):
            r = row1 + offset
            if 0 <= r < len(large_maze):
                # Check if both sides have paths
                if large_maze[r][col1] == 0 and large_maze[r][col2] == 0:
                    stitch_points.append((r, col1, col2))
    
    elif direction == 'vertical':
        row1, col1 = patch1_bounds
        row2, col2 = patch2_bounds
        
        for offset in range(-search_range, search_range + 1):
            c = col1 + offset
            if 0 <= c < len(large_maze[0]):
                if large_maze[row1][c] == 0 and large_maze[row2][c] == 0:
                    stitch_points.append((row1, row2, c))
    
    return stitch_points

def create_stitch(large_maze, stitch_point, direction):
    """Create a stitch (opening) between two patches"""
    if direction == "horizontal":
        r, c1, c2 = stitch_point
        # With overlapping patches, c1 and c2 are the same (shared wall)
        # Just carve through that single shared wall
        large_maze[r][c1] = 0
    elif direction == "vertical":
        r1, r2, c = stitch_point
        # With overlapping patches, r1 and r2 are the same (shared wall)
        # Just carve through that single shared wall
        large_maze[r1][c] = 0

def place_random_goal(maze, exclude_positions=None):
    """Place a goal at a random path location in the maze"""
    height = len(maze)
    width = len(maze[0])
    
    if exclude_positions is None:
        exclude_positions = []
    
    valid_positions = []
    
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 0 and (y, x) not in exclude_positions:
                valid_positions.append((y, x))
    
    if valid_positions:
        goal_y, goal_x = random.choice(valid_positions)
        maze[goal_y][goal_x] = 2
        return (goal_y, goal_x)
    
    return None

def finalMaze(patch_width, patch_height, num_patches_x, num_patches_y, num_stitches):
    """
    Create a braided maze from multiple patches
    
    :param patch_width: Width of each patch (must be odd)
    :param patch_height: Height of each patch (must be odd)
    :param num_patches_x: Number of patches horizontally
    :param num_patches_y: Number of patches vertically
    :param num_stitches: Number of stitches between patches
    """
    border = -1  # Negative border makes patches overlap and share their edge walls

    # Calculate base canvas dimensions
    total_width = patch_width * num_patches_x + (num_patches_x - 1) * border 
    total_height = patch_height * num_patches_y + (num_patches_y - 1) * border 

    # Make canvas with dimensions
    large_maze = grid(total_width, total_height)

    # Generate and place the patches
    for py in range(num_patches_y):
        for px in range(num_patches_x):
            patch = grid(patch_width, patch_height)
            patch = dfs(patch, patch_width, patch_height)

            # Place the patch
            start_row = py * (patch_height + border)
            start_col = px * (patch_width + border)
            place_patch(large_maze, patch, start_row, start_col)

    # Create horizontal stitches (between left-right patches)
    for py in range(num_patches_y):
        for px in range(num_patches_x - 1):
            start_row = py * (patch_height + border)
            
            # With border=-1, patches overlap at their shared wall
            # The shared wall column is where patch1 ends = where patch2 starts
            shared_wall_col = px * (patch_width + border) + patch_width - 1
            
            middle_row = start_row + patch_height // 2
            search_range = patch_height // 2
            
            # Find locations where both patches have paths adjacent to the shared wall
            stitch_points = find_stitch(
                large_maze,
                (middle_row, shared_wall_col - 1),  # Check path cell just before wall in patch1
                (middle_row, shared_wall_col + 1),  # Check path cell just after wall in patch2
                'horizontal',
                search_range
            )
            
            # Convert stitch points to carve through the shared wall
            wall_stitches = []
            for r, c1, c2 in stitch_points:
                wall_stitches.append((r, shared_wall_col, shared_wall_col))
            
            if wall_stitches:
                stitches_to_make = min(num_stitches, len(wall_stitches))
                for _ in range(stitches_to_make):
                    stitch = random.choice(wall_stitches)
                    create_stitch(large_maze, stitch, 'horizontal')
                    wall_stitches.remove(stitch)

    # Create vertical stitches (between top-bottom patches)
    for py in range(num_patches_y - 1):
        for px in range(num_patches_x):
            start_col = px * (patch_width + border)
            
            # With border=-1, patches overlap at their shared wall
            # The shared wall row is where patch1 ends = where patch2 starts
            shared_wall_row = py * (patch_height + border) + patch_height - 1
            
            middle_col = start_col + patch_width // 2
            search_range = patch_width // 2
            
            # Find locations where both patches have paths adjacent to the shared wall
            stitch_points = find_stitch(
                large_maze,
                (shared_wall_row - 1, middle_col),  # Check path cell just above wall in patch1
                (shared_wall_row + 1, middle_col),  # Check path cell just below wall in patch2
                'vertical',
                search_range
            )
            
            # Convert stitch points to carve through the shared wall
            wall_stitches = []
            for r1, r2, c in stitch_points:
                wall_stitches.append((shared_wall_row, shared_wall_row, c))
            
            if wall_stitches:
                stitches_to_make = min(num_stitches, len(wall_stitches))
                for _ in range(stitches_to_make):
                    stitch = random.choice(wall_stitches)
                    create_stitch(large_maze, stitch, 'vertical')
                    wall_stitches.remove(stitch)

    # Add entrance and exit
    large_maze[1][0] = 0
    large_maze[total_height - 2][total_width - 1] = 0
    
    # Place random goal
    entrance = (1, 0)
    exit_pos = (total_height - 2, total_width - 1)
    goal_position = place_random_goal(large_maze, exclude_positions=[entrance, exit_pos])
    print(f"Goal placed at: {goal_position}")
    
    return large_maze

def testMaze(maze):
    """Print the maze to the console"""
    for row in maze:
        for cell in row:
            if cell == 1:
                print("#", end="") 
            elif cell == 2:
                print("G", end="")
            else:
                print(" ", end="")
        print("")