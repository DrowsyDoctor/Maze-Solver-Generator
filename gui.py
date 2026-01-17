import tkinter as tk
from generation import finalMaze, grid, dfs

class MazeGUI:
    def __init__(self, root, maze, cell_size, maze_type, config, entrance, exit_pos, 
            goal_pos=None, solution_path=None, distances=None):
        self.root = root
        self.maze = maze
        self.cell_size = cell_size
        self.maze_type = maze_type
        self.config = config
        self.entrance = entrance
        self.exit_pos = exit_pos
        self.goal_pos = goal_pos  # MOVE THIS UP before using it
        self.solution_path = solution_path
        self.distances = distances
        
        self.height = len(maze)
        self.width = len(maze[0])
        
        # Animation state
        self.current_step = 0
        self.animation_running = False
        self.animation_speed = config.get('animation_speed', 50)
        
        # Create window
        self.root.title("Maze Solver Visualization")
        
        # Create control frame
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Add buttons
        self.regenerate_btn = tk.Button(self.control_frame, text="Regenerate Maze", 
                                        command=self.regenerate_maze)
        self.regenerate_btn.pack(side=tk.LEFT, padx=5)
        
        if solution_path:
            self.solve_btn = tk.Button(self.control_frame, text="Show Solution (Animated)", 
                                    command=self.start_animation)
            self.solve_btn.pack(side=tk.LEFT, padx=5)
            
            self.instant_btn = tk.Button(self.control_frame, text="Show Full Solution", 
                                        command=self.show_full_solution)
            self.instant_btn.pack(side=tk.LEFT, padx=5)
            
            self.reset_btn = tk.Button(self.control_frame, text="Reset View", 
                                    command=self.reset_view)
            self.reset_btn.pack(side=tk.LEFT, padx=5)
            
            self.show_distances_btn = tk.Button(self.control_frame, text="Toggle Distance Map", 
                                            command=self.toggle_distances)
            self.show_distances_btn.pack(side=tk.LEFT, padx=5)
        
        # Info label
        self.info_label = tk.Label(self.control_frame, text="", fg="blue")
        self.info_label.pack(side=tk.LEFT, padx=20)
        
        # Create canvas
        canvas_width = self.width * cell_size
        canvas_height = self.height * cell_size
        
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, 
                            bg='white', highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        
        # State for visualization
        self.show_distance_map = False
        self.show_full_path = False
        
        # Draw initial maze
        self.draw_maze()
        
    def draw_maze(self):
        """Draw the maze on the canvas"""
        self.canvas.delete("all")
        
        for y in range(self.height):
            for x in range(self.width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell_value = self.maze[y][x]
                
                # Determine cell color
                if cell_value == 1:  # Wall
                    color = 'black'
                elif self.show_distance_map and self.distances and \
                    self.distances[y][x] != float('inf'):
                    # Color by distance (gradient from blue to red)
                    max_dist = max(max(row) for row in self.distances 
                                if any(d != float('inf') for d in row))
                    if max_dist > 0:
                        ratio = self.distances[y][x] / max_dist
                        # Blue (close to exit) to Red (far from exit)
                        r = int(255 * ratio)
                        b = int(255 * (1 - ratio))
                        color = f'#{r:02x}40{b:02x}'
                    else:
                        color = 'white'
                elif cell_value == 2:  # Goal
                    color = 'gold'
                else:  # Path
                    color = 'white'
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
        
        # Draw entrance
        if self.entrance:
            ey, ex = self.entrance
            self.canvas.create_oval(
                ex * self.cell_size + self.cell_size//4,
                ey * self.cell_size + self.cell_size//4,
                (ex + 1) * self.cell_size - self.cell_size//4,
                (ey + 1) * self.cell_size - self.cell_size//4,
                fill='green', outline='darkgreen', width=2
            )
        
        # Draw exit
        if self.exit_pos:
            ey, ex = self.exit_pos
            self.canvas.create_oval(
                ex * self.cell_size + self.cell_size//4,
                ey * self.cell_size + self.cell_size//4,
                (ex + 1) * self.cell_size - self.cell_size//4,
                (ey + 1) * self.cell_size - self.cell_size//4,
                fill='red', outline='darkred', width=2
            )
        
        # Draw solution path if showing
        if self.show_full_path and self.solution_path:
            self.draw_path(0, len(self.solution_path))
        elif self.animation_running and self.solution_path:
            self.draw_path(0, self.current_step + 1)
    
    def draw_path(self, start_idx, end_idx):
        """Draw the solution path from start_idx to end_idx"""
        if not self.solution_path or end_idx <= start_idx:
            return
        
        # Draw path segments
        for i in range(start_idx, min(end_idx - 1, len(self.solution_path) - 1)):
            y1, x1 = self.solution_path[i]
            y2, x2 = self.solution_path[i + 1]
            
            cx1 = x1 * self.cell_size + self.cell_size // 2
            cy1 = y1 * self.cell_size + self.cell_size // 2
            cx2 = x2 * self.cell_size + self.cell_size // 2
            cy2 = y2 * self.cell_size + self.cell_size // 2
            
            self.canvas.create_line(cx1, cy1, cx2, cy2, fill='blue', width=3, 
                                tags="path")
        
        # Draw current mouse position (animated)
        if self.animation_running and end_idx > 0 and end_idx <= len(self.solution_path):
            y, x = self.solution_path[end_idx - 1]
            self.canvas.create_oval(
                x * self.cell_size + self.cell_size//3,
                y * self.cell_size + self.cell_size//3,
                (x + 1) * self.cell_size - self.cell_size//3,
                (y + 1) * self.cell_size - self.cell_size//3,
                fill='purple', outline='darkviolet', width=2, tags="mouse"
            )
    
    def start_animation(self):
        """Start the animated solution"""
        if not self.solution_path:
            return
        
        self.animation_running = True
        self.current_step = 0
        self.show_full_path = False
        self.animate_step()
    
    def animate_step(self):
        """Animate one step of the solution"""
        if not self.animation_running:
            return
        
        if self.current_step < len(self.solution_path):
            self.draw_maze()
            self.info_label.config(text=f"Step {self.current_step + 1} / {len(self.solution_path)}")
            self.current_step += 1
            self.root.after(self.animation_speed, self.animate_step)
        else:
            self.animation_running = False
            self.info_label.config(text=f"Solution complete! Total steps: {len(self.solution_path)}")
    
    def show_full_solution(self):
        """Show the complete solution instantly"""
        self.animation_running = False
        self.show_full_path = True
        self.current_step = len(self.solution_path) if self.solution_path else 0
        self.draw_maze()
        if self.solution_path:
            self.info_label.config(text=f"Full solution shown. Path length: {len(self.solution_path)}")
    
    def reset_view(self):
        """Reset the view to show just the maze"""
        self.animation_running = False
        self.show_full_path = False
        self.current_step = 0
        self.draw_maze()
        self.info_label.config(text="View reset")
    
    def toggle_distances(self):
        """Toggle the distance map visualization"""
        self.show_distance_map = not self.show_distance_map
        self.draw_maze()
        if self.show_distance_map:
            self.info_label.config(text="Distance map shown (blue=close, red=far)")
        else:
            self.info_label.config(text="Distance map hidden")
    
    def regenerate_maze(self):
        """Generate a new maze and solve it"""
        from solver import floodfill, mouse
        
        print("Regenerating maze...")
        
        if self.maze_type == 'simple':
            new_maze = grid(self.config['width'], self.config['height'])
            new_maze = dfs(new_maze, self.config['width'], self.config['height'])
            new_maze[1][0] = 0
            new_maze[self.config['height'] - 2][self.config['width'] - 1] = 0
            entrance = (1, 0)
            exit_pos = (self.config['height'] - 2, self.config['width'] - 1)
        else:
            new_maze = finalMaze(
                patch_width=self.config['patch_width'],
                patch_height=self.config['patch_height'],
                num_patches_x=self.config['num_patches_x'],
                num_patches_y=self.config['num_patches_y'],
                num_stitches=self.config['num_stitches']
            )
            entrance = (1, 0)
            exit_pos = (len(new_maze) - 2, len(new_maze[0]) - 1)
        
        # Solve the new maze
        distances = floodfill(new_maze, exit_pos[0], exit_pos[1])
        solution_path = mouse(exit_pos[0], exit_pos[1], entrance, new_maze)
        
        # Update state
        self.maze = new_maze
        self.entrance = entrance
        self.exit_pos = exit_pos
        self.solution_path = solution_path
        self.distances = distances
        self.height = len(new_maze)
        self.width = len(new_maze[0])
        
        # Reset view
        self.animation_running = False
        self.show_full_path = False
        self.show_distance_map = False
        self.current_step = 0
        
        # Redraw
        self.draw_maze()
        self.info_label.config(text=f"New maze generated! Solution: {len(solution_path)} steps")
        
        print(f"New maze generated with solution length: {len(solution_path)}")

def display_maze(maze, cell_size=10, maze_type='simple', config=None, entrance=None, 
                exit_pos=None, goal_pos=None, solution_path=None, distances=None):
    """Create and display the maze GUI"""
    root = tk.Tk()
    gui = MazeGUI(root, maze, cell_size, maze_type, config, entrance, exit_pos, 
                goal_pos, solution_path, distances)
    root.mainloop()