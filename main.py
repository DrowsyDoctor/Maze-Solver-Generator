from generation import grid, dfs, finalMaze, testMaze
from gui import display_maze
from solver import floodfill, mouse, find_goal

# ==========================================
# CONFIGURATION - EDIT THESE VALUES
# ==========================================

# Simple maze settings
SIMPLE_WIDTH = 41
SIMPLE_HEIGHT = 41

# Braided maze settings
PATCH_WIDTH = 21      # Must be odd
PATCH_HEIGHT = 21     # Must be odd
NUM_PATCHES_X = 3     # Number of patches horizontally
NUM_PATCHES_Y = 3     # Number of patches vertically
NUM_STITCHES = 4      # Number of connections between patches

# Display settings
CELL_SIZE = 9        # Size of each cell in pixels (smaller = more fits on screen)

# Choose which maze to generate: 'simple' or 'braided'
MAZE_TYPE = 'braided'

# Solver settings
RUN_SOLVER = True    # Set to True to run the solver
ANIMATION_SPEED = 50  # Milliseconds between animation steps (lower = faster)

# ==========================================
# END CONFIGURATION
# ==========================================

def main():
    # Store configuration for the GUI to use when regenerating
    config = {
        'width': SIMPLE_WIDTH,
        'height': SIMPLE_HEIGHT,
        'patch_width': PATCH_WIDTH,
        'patch_height': PATCH_HEIGHT,
        'num_patches_x': NUM_PATCHES_X,
        'num_patches_y': NUM_PATCHES_Y,
        'num_stitches': NUM_STITCHES,
        'animation_speed': ANIMATION_SPEED
    }
    
    if MAZE_TYPE == 'simple':
        # Generate a simple maze
        print(f"Generating simple maze: {SIMPLE_WIDTH}x{SIMPLE_HEIGHT}")
        my_maze = grid(SIMPLE_WIDTH, SIMPLE_HEIGHT) 
        my_maze = dfs(my_maze, SIMPLE_WIDTH, SIMPLE_HEIGHT)
        my_maze[1][0] = 0  # Entrance
        my_maze[SIMPLE_HEIGHT - 2][SIMPLE_WIDTH - 1] = 0  # Exit
        entrance = (1, 0)
        exit_pos = (SIMPLE_HEIGHT - 2, SIMPLE_WIDTH - 1)
        
    else:  # 'braided'
        # Generate a braided maze
        print(f"Generating braided maze:")
        print(f"  Patch size: {PATCH_WIDTH}x{PATCH_HEIGHT}")
        print(f"  Grid: {NUM_PATCHES_X}x{NUM_PATCHES_Y} patches")
        print(f"  Stitches per connection: {NUM_STITCHES}")
        
        my_maze = finalMaze(
            patch_width=PATCH_WIDTH,
            patch_height=PATCH_HEIGHT,
            num_patches_x=NUM_PATCHES_X,
            num_patches_y=NUM_PATCHES_Y,
            num_stitches=NUM_STITCHES
        )
        entrance = (1, 0)
        exit_pos = (len(my_maze) - 2, len(my_maze[0]) - 1)
    
    goal_pos = find_goal(my_maze)
    
    # Print to console (REMOVE DUPLICATE)
    print("Maze generated!")
    print(f"Final size: {len(my_maze[0])}x{len(my_maze)}")
    print(f"Entrance: {entrance}")
    print(f"Exit: {exit_pos}")
    print(f"Goal: {goal_pos}")  # ADD THIS LINE
    
    # Optionally print to console (comment out for large mazes)
    if len(my_maze) <= 50 and len(my_maze[0]) <= 50:
        testMaze(my_maze)
    else:
        print("(Maze too large to print to console)")
    
    # Run solver if enabled
    solution_path = None
    distances = None
    if RUN_SOLVER and goal_pos:
        print("\nRunning solver to goal...")
        distances = floodfill(my_maze, goal_pos[0], goal_pos[1])
        solution_path = mouse(goal_pos[0], goal_pos[1], entrance, my_maze)
        
        if solution_path:
            print(f"Solution found! Path length: {len(solution_path)} steps")
        else:
            print("No solution found!")
    
    # Display in Tkinter
    display_maze(my_maze, cell_size=CELL_SIZE, maze_type=MAZE_TYPE, config=config, 
                entrance=entrance, exit_pos=exit_pos, goal_pos=goal_pos,
                solution_path=solution_path, distances=distances)

if __name__ == "__main__":
    main()