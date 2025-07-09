from typing import List, Tuple
class Node:
    """
       Represents a device/node in the MANET simulation.
       Each node has an ID, name, 2D position, communication range, neighbors, and a message buffer.
       Nodes default to a communication range of 100.
    """
    def __init__(self, node_id: int, node_name: str, position: tuple[int, int], comm_range: int =100, base_color: str = "#ff0000"):
        self._node_id: int = node_id # The node's (Device's) personal identifier, lets other nodes know who they are 'speaking' to.
        self._node_name: str = node_name # The name of the node/"Device" (, e.g, 'Dennis' iPhone)
        self._position: tuple[int, int] = position # A tuple representing the node's position on the 2D Map (x, y)
        self.display_pos = (position[0], position[1]) # GUI position, used for smooth drawing.
        self._comm_range: int = comm_range # How close each node has to be to another node has to be in relation to another to communicate
        self._neighbors: List['Node'] = [] # A dynamic list that stores the nodes within this node's range
        self._messages: List[tuple[int, str]] = [] # A dynamically building list of node_ids (int) paired to messages (str).
        self.adhoc_enabled: bool = True # A boolean member to represent whether or not a device wants to be an adhoc participant
        self.display_color: str = base_color # A string variable to represent the assigned colour of the device for the GUI. (Set at creation)
        self.base_color = base_color


    def move(self, new_position: tuple[int, int]) -> None: # This function sets a new position value for the node that it is called on.
        original_position = self.position # Start by storing the position of the node before it moved
        self._position = new_position # Change the position of this node to its new value
        print(f"\n{self.node_name} moved from {original_position} to {self.position}") # Display updated node location

    def receive_message(self, sender: 'Node', message: str) -> None: # This function makes this node (the node that calls the function) add a message from a declared sender to this node's message list.
        self._messages.append((sender.node_id, message))  # Store the sender's id for tracking and the message they sent as a key and value (tuple) into the message list.
        print(f"\n{self.node_name} received message from {sender.node_name}: {message}") # Display that this node recieved a message from the sender node, and show the message.

    def display_messages(self) -> None: # This function displays all of this node's messages.
        print(f"\n{self.node_name} messages: {self._messages}")

    def display_neighbors(self) -> None:
        print(f"{self.node_name} neighbors: {[n.node_name for n in self.neighbors]}")

    @property
    def node_id(self) -> int:
        return self._node_id

    @property
    def node_name(self) -> str:
        return self._node_name

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @property
    def comm_range(self) -> int:
        return self._comm_range

    @property
    def neighbors(self) -> list['Node']:
        return self._neighbors

    def __repr__(self): #The string representation of a node
        return f"Node: {self._node_id} at position: {self._position}"
