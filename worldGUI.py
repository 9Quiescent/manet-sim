import tkinter as tk
from world import World
from tkinter import ttk

CELL_SIZE = 60  # The visual size/pixel size of each cell (position) on the 2D space
PICTO_BG      = "#eaf1fb"  # Primary background colour
PICTO_BUBBLE  = "#b4e0ff"  # Colour of "bubbles"
PICTO_BUBBLE2 = "#ffffff"  # Alternate bubble colour
PICTO_BORDER  = "#aad0ee" # Primary border colour
PICTO_BTN     = "#5db9ff" # Primary button colour
PICTO_FONT    = "Helvetica" # Primary font


class WorldGUI:
    def __init__(self, world: World):
        self.world: World = world # A member storing the world instance that the GUI renders.
        self.root: tk.Tk = tk.Tk() # A member storing this worldGUI's instance of a tinker window. Used for modifying the tinker window's attributes.
        self.root.title("MANET Simulator") # Determines the GUI's title
        style = ttk.Style(self.root)
        style.configure('.', font=('Segoe UI', 11))
        self.root.geometry("1200x600")  # Determines the GUI's window size (width * length)

        self.canvas: tk.Canvas = tk.Canvas(self.root, width=world.width * CELL_SIZE, height=world.height * CELL_SIZE, bg=PICTO_BG) # The 2D space where all the nodes reside. It must sit inside the tinker window (root). It has the width/height of the GUI's world * the size of each pixel respectively for scale.
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="nsew") # We use a grid system to keep the panes organised, the play area (canvas) will always appear on top left (row 0, column 0) it occupies 2 rows vertically for formatting.
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.log_text: tk.Text = tk.Text(self.root, height=30, width=65, state='disabled', bg='#f7f7f7', font=("Consolas", 12)) # The pane with all of the log text
        self.log_text.grid(row=0, column=1, sticky="nsew") # Management for the log text pane's location on the grid.

        self.step_button: tk.Button = tk.Button(
            self.root,
            text="▶ SIMULATE STEP",
            command=self.do_step,
            bg=PICTO_BTN,
            fg="Black",
            font=(PICTO_FONT, 16, "bold"),
            width=2,  # Small, square-ish
            height=1,
            activebackground=PICTO_BORDER,
            bd=0,  # No border for flat look
            relief="flat",
            highlightthickness=0
        ) # A button for calling do_step on the passed in world object.
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
            color = node.display_color if node.adhoc_enabled else "#808080"
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

    def interpolate_color(self, color1: str, color2: str, t: float) -> str:
        """
        Linearly interpolate between two hex colors (e.g., '#FF0000' to '#808080').
        t=0 gives color1, t=1 gives color2.
        """
        c1 = [int(color1[i:i + 2], 16) for i in (1, 3, 5)]
        c2 = [int(color2[i:i + 2], 16) for i in (1, 3, 5)]
        interp = [int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)]
        return f'#{interp[0]:02x}{interp[1]:02x}{interp[2]:02x}'

    def animate_node_color(self, node, fade_to_gray: bool, steps=15, delay=20): # This function is for fading between gray or the node's assigned color.
        start_color = node.display_color
        end_color = '#808080' if fade_to_gray else node.base_color
        for i in range(steps + 1):
            t = i / steps
            color = self.interpolate_color(start_color, end_color, t)
            node.display_color = color
            self.draw_world()
            self.root.update()
            self.root.after(delay)
        node.display_color = end_color
        self.draw_world()

    def on_canvas_click(self, event):
        # Convert click to cell coords
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        for node in self.world.network.nodes:
            nx, ny = node.position
            if abs(nx - x) < 1 and abs(ny - y) < 1:  # Click is in node cell
                self.show_node_menu(event, node)
                break

    def show_node_menu(self, event, node): # This function is for rendering a drop down on the click of a node.
        menu = tk.Menu(self.root, tearoff=0, font=(PICTO_FONT, 11))
        menu.add_command(
            label="Toggle Adhoc Mode",
            command=lambda: self.toggle_adhoc_status(node)
        )
        menu.add_command(label="View Inbox", command=lambda: self.show_inbox(node))
        menu.add_command(label="Send Message", command=lambda: self.send_message_dialog(node))
        menu.tk_popup(event.x_root, event.y_root)

    def toggle_adhoc_status(self, node): # This function is for toggling between a node's adhoc participation status.
        old_status = node.adhoc_enabled # First, store the original status
        node.adhoc_enabled = not old_status # If the status was false
        self.animate_node_color(node, fade_to_gray=not node.adhoc_enabled) # Call the fade animation to for gray
        self.world.network.update_neighbors() # Update the world's neighbors
        self.draw_world() # Update the GUI representation.
        # Compose new log message
        state = "enabled" if node.adhoc_enabled else "disabled"
        self.log(f"\n{node.node_name} {state} ad-hoc mode, updating neighbors...\n")
        # Now, show the current neighbor view for all nodes
        for node in self.world.network.nodes:
            neighbors = [n.node_name for n in node.neighbors]
            self.log(f"{node.node_name} at {node.position} neighbors: {neighbors}")

    def show_inbox(self, node):
        # Retrieve the messages stored on the node (these are tuples of sender_id and text)
        messages = node._messages

        # Create a new window (child of root) to display the inbox
        win = tk.Toplevel(self.root)
        win.title(f"{node.node_name}'s Inbox")  # Title bar shows which node's inbox it is
        win.configure(bg=PICTO_BG)  # Set window background color to match app
        win.geometry("680x440")  # Set window size (wider than tall for chat feel)

        # The main frame holds all inbox UI content, keeps padding off window edges
        frame = tk.Frame(win, bg=PICTO_BG)
        frame.pack(fill="both", expand=True, padx=18, pady=10)

        # Create a canvas to enable scrolling for long inboxes (messages)
        canvas = tk.Canvas(frame, bg=PICTO_BG, highlightthickness=0)
        # Add a vertical scrollbar linked to the canvas (classic chat UI)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        # Frame inside canvas to actually hold each message "bubble"
        message_frame = tk.Frame(canvas, bg=PICTO_BG)

        # Whenever messages are added/removed, update scroll region to fit all content
        message_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        # Embed the message frame into the canvas (acts like a scrollable "window")
        canvas.create_window((0, 0), window=message_frame, anchor="nw")
        # Configure canvas to be scrollable with scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        # Lay out the canvas and scrollbar side by side
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # If there are no messages, display a centered "No messages" label
        if not messages:
            tk.Label(
                message_frame,
                text="No messages.",
                bg=PICTO_BG,
                font=(PICTO_FONT, 16)
            ).pack(anchor="w", pady=(16, 0), padx=6)
        else:
            # For each message in the inbox...
            for sender_id, text in messages:
                # Look up sender's name using sender_id for display (fallback to ID if not found)
                sender_name = next((n.node_name for n in self.world.network.nodes if n.node_id == sender_id),
                                   f"ID {sender_id}")
                # Select color for bubble: own messages are blue, others are white
                bubble_color = PICTO_BUBBLE if sender_name == node.node_name else PICTO_BUBBLE2
                # Messages you sent are right-aligned, others left (classic chat look)
                align = "e" if sender_name == node.node_name else "w"
                # Create the actual "bubble" label to show the message and sender
                bubble = tk.Label(
                    message_frame,
                    text=f"{sender_name} said:\n{text}",
                    bg=bubble_color,
                    fg="#222",
                    font=(PICTO_FONT, 16),
                    padx=16, pady=12,
                    bd=2, relief="solid",
                    wraplength=340, anchor=align, justify="left"
                )
                # Pack each message bubble with vertical spacing and proper side padding
                bubble.pack(anchor=align, pady=7, padx=8, fill=None, ipadx=4)

        tk.Button(
            win,
            text="← BACK",
            command=win.destroy,
            bg=PICTO_BTN,
            fg="Black",
            font=(PICTO_FONT, 16, "bold"),
            activebackground=PICTO_BORDER
        ).pack(pady=8)

    def picto_info(self, message): # This function is for wrapping a content (string) around reusable gui styling.
        win = tk.Toplevel(self.root)
        win.configure(bg=PICTO_BG)
        win.geometry("340x120")
        tk.Label(
            win,
            text=message,
            bg=PICTO_BG,
            font=(PICTO_FONT, 15),
            padx=20,
            pady=18,
            wraplength=300,
            justify="left"
        ).pack()
        tk.Button(win, text="OK", command=win.destroy, bg=PICTO_BTN, fg="Black", font=(PICTO_FONT, 13, "bold"),
                  activebackground=PICTO_BORDER).pack(pady=8)
        win.grab_set()

    def send_message_dialog(self, node):  # Called when user chooses to send a message from a node
        # Filter this node's neighbors to only those with ad-hoc enabled (can actually receive messages)
        neighbors = [n for n in node.neighbors if n.adhoc_enabled]
        # If there are no available neighbors, show a message and exit early (nothing to send to)
        if not neighbors:
            self.picto_info("No neighbors available to send message.")
            return

        # Create a pop-up window for composing the message (child of main window)
        win = tk.Toplevel(self.root)
        win.title(f"{node.node_name}: Compose a Message.")  # Show which node is sending
        win.configure(bg=PICTO_BG)  # Match the app's visual theme

        # Label for the recipient selection field.
        tk.Label(
            win,
            text="Select recipient:",
            bg=PICTO_BG,
            font=(PICTO_FONT, 13, "bold")
        ).pack(anchor="w", padx=18, pady=(12, 0))

        # Radio buttons for the available recipients (neighbors)
        # Variable to store the selected recipient's name (defaults to first neighbor)
        recipient_var = tk.StringVar(value=neighbors[0].node_name)
        # For every neighbor, create a radio button so user can choose who to send to
        for n in neighbors:
            ttk.Radiobutton(
                win,
                text=f"{n.node_name} (id {n.node_id})",
                variable=recipient_var,
                value=n.node_name
            ).pack(anchor="w", padx=32, pady=1)

        # Message entry label
        tk.Label(
            win,
            text="Message:",
            bg=PICTO_BG,
            font=(PICTO_FONT, 13)
        ).pack(anchor="w", padx=18, pady=(12, 0))

        # Text box for message entries.
        msg_entry = tk.Entry(win, width=38, font=(PICTO_FONT, 14))
        msg_entry.pack(padx=18, pady=(2, 10))

        def send_now():      # This function is a send handler, which handles actually delivering the message when the Send button is clicked
            # Get selected neighbor's name from the radio group
            selected_name = recipient_var.get()
            # Find the actual neighbor node instance that matches the chosen name
            recipient = next((n for n in neighbors if n.node_name == selected_name), None)
            # Get the user's typed message, trimming any whitespace
            msg = msg_entry.get().strip()
            # Only send if both a recipient was found and the message isn't empty
            if recipient and msg:
                self.world.network.send_message(node, recipient, msg)  # Passes message through the network
                # Log the event as an E2EE-style delivery (no message content)
                self.log(
                    f"[SECURE MESSAGE] {node.node_name} → {recipient.node_name}: Message sent securely using E2EE protocol.")
                self.picto_info(f"Sent to {recipient.node_name}: {msg}")  # Show confirmation dialog
            win.destroy()  # Always close the dialog after attempting to send

        # Send and cancel buttons
        btn = tk.Button(
            win,
            text="Send",
            command=send_now,
            bg=PICTO_BTN,
            fg="black",
            font=(PICTO_FONT, 13, "bold"),
            activebackground=PICTO_BORDER
        )
        btn.pack(side="left", padx=20, pady=(2, 16))

        # Cancel button closes the dialog with no further action
        ttk.Button(win, text="Cancel", command=win.destroy).pack(side="right", padx=20, pady=(2, 16))





    def run(self) -> None: # Run the GUI, loop rendering until closed.
        self.root.mainloop()


