from typing import List, Tuple
from node import Node

class Network:
    """
    Represents an ad hoc network of nodes/devices.
    Handles neighbor relationships, message delivery, and node management.
    """

    def __init__(self):
        self.nodes: List[Node] = []

    def add_node(self, new_neighbor: Node) -> None: #This function adds a node to this network's list of nodes (neighbors)
        self.nodes.append(new_neighbor)
        print(f"Node added to network: {new_neighbor.node_name} at position {new_neighbor.position}")

    def remove_node(self, node: Node) -> None: #This function removes a node from this network's list of neighbor
        if node in self.nodes: # Check if the node is already in the network's list of registered nodes.
            self.nodes.remove(node) # If it is, we remove the node from the network.
            print(f"\nNode removed from network: {node.node_name}")
        else:
            print(f"Tried to remove node not in network: {node.node_name}") # Otherwise, explain that we cannot remove nodes from the network that arent in the network.

    def update_neighbors(self) -> None: # This function updates the neighbor list of every node within this network.
        print("\nUpdating neighbor lists for all nodes in the network...")
        for node in self.nodes:
            node._neighbors = []
            for other in self.nodes:
                if node is not other and self.in_range(node, other): # If the node is not in a node that is inside this network's neighbor list, add it.
                    node._neighbors.append(other)
        print("Neighbor lists updated.")

    @staticmethod
    def in_range(node1: Node, node2: Node) -> bool: # This function checks if two nodes are within communication range of each other.
        dx = node1.position[0] - node2.position[0] # First, calculate the difference between the x-axis value of both ndoes
        dy = node1.position[1] - node2.position[1] # Do the same for the y-axis
        distance = (dx ** 2 + dy ** 2) ** 0.5 # Then produce a distance value by finding the square root of both distances added together squred.
        return distance <= node1.comm_range # If the communication range of either node is greater than or equal to the distance between the two nodes, the nodes are in range.

    def move_node(self, node: Node, new_position: Tuple[int, int]) -> None: # This function moves the location of a node, then updates the neighbors for each node.
        print(f"\nMoving node: {node.node_name} from {node.position} to {new_position}")
        node.move(new_position)
        self.update_neighbors()


    def send_message(self, sender: Node, target: Node, message: str) -> None: # This function sends a message from a sender node to a target node.
        print(f"\nAttempting to send message from {sender.node_name} to {target.node_name}...")
        if sender not in self.nodes or target not in self.nodes: # Only allow this if the sender and target are within this network (nodes list).
            print("Error: Sender or target is not in this network.")
            return
        if target in sender.neighbors: # Otherwise, add the sender's message to their target's message list, and display this interaction.
            print(f"SUCCESS: {sender.node_name} sends message to {target.node_name}: \"{message}\"")
            target.receive_message(sender, message)
        else:
            print(f"FAIL: {target.node_name} is not a neighbor of {sender.node_name}! Message not delivered.") # If sender attempts to deliver a message from an out of range node, display an error.

    def display_all_neighbors(self) -> None: # This function displays all neighbours for all nodes.
        for node in self.nodes:
            node.display_neighbors()

    def display_all_messages(self) -> None: # This function displays all messsages for all nodes.
        for node in self.nodes:
            node.display_messages()



