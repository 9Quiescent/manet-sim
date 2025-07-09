import tkinter as tk
from node import Node
from world import World

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

    def draw_world(self) -> None: # This function is used for rendering all of the objects on the play area (canvas), currently including nodes and walls.
        self.canvas.delete('all') # We start by clearing out the canvas (graphics, not the actual objects)
        # Draw walls (if any)
        for wx, wy in self.world.walls: # For the world's x-axis and y-axis of each of the world's walls
            x1, y1 = wx * CELL_SIZE, wy * CELL_SIZE # Render the respective dimensions to scale with the size of each cell.
            self.canvas.create_rectangle(x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE, fill='black') # Render walls as black squares based on the above dimensions.
        # Draw nodes
        colors = ['red', 'blue', 'green', 'orange', 'purple'] # A list of the available colors for nodes.
        for index, node in enumerate(self.world.network.nodes): # This loop takes the maps colors to nodes by their respective index. (index 0 in the node list will always be red)
            x, y = node.position
            x1, y1 = x * CELL_SIZE, y * CELL_SIZE
            color = colors[index % len(colors)]
            self.canvas.create_oval(x1 + 5, y1 + 5, x1 + CELL_SIZE - 5, y1 + CELL_SIZE - 5, fill=color)
            self.canvas.create_text(x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2, text=node.node_name[:3], fill='white',
                                    font=('Arial', 12, 'bold'))

    def do_step(self) -> None: # This function is used for simulating the flow of time in the simulation.
        self.step_count += 1 # Everytime we call this method, increase the step count by 1. (Used for the GUI)
        self.world.step() # Call the actual world's step function.
        self.draw_world() # Update the GUI
        self.log(f"\n==== Step {self.step_count} ====") # Display the current step to the user end
        for node in self.world.network.nodes: # For every node in the world
            neighbors = [n.node_name for n in node.neighbors] # Assign a node name to in range nodes as "neighbors".
            self.log(f"{node.node_name} at {node.position} neighbors: {neighbors}") # Display a device name and its neighbors.

    def run(self) -> None: # Run the GUI, loop rendering until closed.
        self.root.mainloop()


