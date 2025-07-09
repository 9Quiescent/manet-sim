import tkinter as tk
from node import Node
from world import World
import time

CELL_SIZE = 60  # The visual size/pixel size of each cell (position) on the 2D space


class WorldGUI:
    def __init__(self, world: World):
        self.world: World = world # A member storing the world instance that the GUI renders.
        self.root: tk.Tk = tk.Tk() # A member storing this worldGUI's instance of a tinker window. Used for modifying the tinker window's attributes.
        self.root.title("MANET Simulator") # Determines the GUI's title
        self.root.geometry("1200x600")  # Determines the GUI's window size (width * length)

        self.canvas: tk.Canvas = tk.Canvas(self.root, width=world.width * CELL_SIZE, height=world.height * CELL_SIZE, bg='white') # The 2D space where all the nodes reside. It must sit inside the tinker window (root). It has the width/height of the GUI's world * the size of each pixel respectively for scale.
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="nsew") # We use a grid system to keep the panes organised, the play area (canvas) will always appear on top left (row 0, column 0) it occupies 2 rows vertically for formatting.

        self.log_text: tk.Text = tk.Text(self.root, height=30, width=65, state='disabled', bg='#f7f7f7', font=("Consolas", 12)) # The pane with all of the log text
        self.log_text.grid(row=0, column=1, sticky="nsew") # Management for the log text pane's location on the grid.

        self.step_button: tk.Button = tk.Button(self.root, text="Step", command=self.do_step) # A button for calling do_step on the passed in world object.
        self.step_button.grid(row=1, column=1, sticky='ew') # Management for the log text pane's position on the grid, currently underneath the log text pane.

        self.root.grid_columnconfigure(0, weight=1) # Management for stretch as the window expands for column 0. (It will grow by the same amount as other columns with a weight of 1)
        self.root.grid_columnconfigure(1, weight=1) # Management for stretch as the window expands, for column 1. (It will grow by the same amount as other columns with a weight of 1)
        self.root.grid_rowconfigure(0, weight=1) # Management for stretch as the window expands, for row 0. (It will grow by the same amount as other rows with a weight of 1)
        self.root.grid_rowconfigure(1, weight=1) # Management for stretch as the window expands, for row 1. (It will grow by the same amount as other rows with a weight of 1)
        self.step_count: int = 0 # A member to keep track of the current step (GUI end)
        self.draw_world() # A member for keeping track of the current world, this member gets updated every time a change is made to the world.

    def log(self, content) -> None: # This function is used for adding a content to the log pane.
        self.log_text.config(state='normal') # Content is initially editable
        self.log_text.insert('end', content + '\n') # It is then added to the pane
        self.log_text.config(state='disabled') # Once added, it cannot be modified
        self.log_text.see('end')

    def draw_world(self, animated: bool = False) -> None: # This function is used for rendering all of the objects on the play area (canvas), currently including nodes and walls.
        self.canvas.delete('all') # We start by clearing out the canvas (graphics, not the actual objects)

        # Draw links between neighbors, representing devices that are in range of each other.
        seen_pairs = set() # Collects pairs of nodes that have already had links drawn between each other.
        for node in self.world.network.nodes:
            x1, y1 = node.display_pos if animated else node.position
            cx1 = x1 * CELL_SIZE + CELL_SIZE // 2
            cy1 = y1 * CELL_SIZE + CELL_SIZE // 2
            for neighbor in node.neighbors:
                # To avoid drawing each connection twice:
                pair = tuple(sorted([id(node), id(neighbor)]))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                x2, y2 = neighbor.display_pos if animated else neighbor.position
                cx2 = x2 * CELL_SIZE + CELL_SIZE // 2
                cy2 = y2 * CELL_SIZE + CELL_SIZE // 2
                self.canvas.create_line(
                    cx1, cy1, cx2, cy2,
                    fill="#3399FF", width=5
                )
        # Draw walls (if any)
        for wx, wy in self.world.walls: # For the world's x-axis and y-axis of each of the world's walls
            x1, y1 = wx * CELL_SIZE, wy * CELL_SIZE # Render the respective dimensions to scale with the size of each cell.
            self.canvas.create_rectangle(x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE, fill='black') # Render walls as black squares based on the above dimensions.
        # Draw nodes
        colors = ['red', 'blue', 'green', 'orange', 'purple'] # A list of the available colors for nodes.
        for index, node in enumerate(self.world.network.nodes): # This loop takes the maps colors to nodes by their respective index. (index 0 in the node list will always be red)
            if animated:
                x, y = node.display_pos
            else:
                x, y = node.position
            x1, y1 = x * CELL_SIZE, y * CELL_SIZE
            color = colors[index % len(colors)]
            self.canvas.create_oval(x1 + 5, y1 + 5, x1 + CELL_SIZE - 5, y1 + CELL_SIZE - 5, fill=color)
            self.canvas.create_text(x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2, text=node.node_name[:3], fill='white',
                                    font=('Arial', 12, 'bold'))

    def do_step(self) -> None: # This function is used for simulating the flow of time in the simulation.
        self.step_count += 1  # Everytime we call this method, increase the step count by 1. (Used for the GUI)
        moves = self.world.step()  # List of (node, old_pos, new_pos) for all nodes gets stored in a variable, moves
        steps = 30  # Int variable for the amount of animation frames for a step (30)
        delay = 1  # Int variable delay between frames (1).

        # Set display_pos to old_pos for all nodes
        for node, old_pos, new_pos in moves:
            node.display_pos = old_pos

        # Animate all nodes moving together
        for frame in range(1, steps + 1):
            for node, old_pos, new_pos in moves:
                interp_x = old_pos[0] + (new_pos[0] - old_pos[0]) * frame / steps
                interp_y = old_pos[1] + (new_pos[1] - old_pos[1]) * frame / steps
                node.display_pos = (interp_x, interp_y)
            self.draw_world(animated=True)
            self.root.update()
            self.root.after(delay)

        # Snap display and logical positions to final value
        for node, old_pos, new_pos in moves:
            node.display_pos = new_pos
            node._position = new_pos

        self.world.network.update_neighbors()
        self.draw_world(animated=False)
        self.log(f"\n==== Step {self.step_count} ====")
        for node in self.world.network.nodes:
            neighbors = [n.node_name for n in node.neighbors]
            self.log(f"{node.node_name} at {node.position} neighbors: {neighbors}")

    def animate_node_move(self, node, new_pos, steps=10, delay=20):
        x0, y0 = node.display_pos
        x1, y1 = new_pos
        for s in range(1, steps + 1):
            interp_x = x0 + (x1 - x0) * s / steps
            interp_y = y0 + (y1 - y0) * s / steps
            node.display_pos = (interp_x, interp_y)
            self.draw_world(animated=True)  # New: pass flag so node draws at display_pos
            self.root.update()
            self.root.after(delay)  # 1 ms delay per frame
        node.display_pos = new_pos  # Snap to grid after anim
        node._position = new_pos  # Snap logic position
        self.draw_world(animated=False)

    def run(self) -> None: # Run the GUI, loop rendering until closed.
        self.root.mainloop()


