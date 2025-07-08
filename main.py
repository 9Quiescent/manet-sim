from node import Node
from network import Network

def main():
    # 1. Create a new network
    net = Network()

    # 2. Create three nodes/devices
    node1 = Node(1, "Dennis' iPhone", (100, 200))
    node2 = Node(2, "Laptop", (150, 210))
    node3 = Node(3, "Tablet", (400, 220))

    # 3. Add nodes to the network
    net.add_node(node1)
    net.add_node(node2)
    net.add_node(node3)

    # 4. Detect neighbors based on initial positions
    net.update_neighbors()
    net.display_all_neighbors()

    # 5. Move Tablet closer to the other devices
    net.move_node(node3, (130, 205))
    net.display_all_neighbors()

    # 6. Attempt messaging
    net.send_message(node1, node2, "Hey, Laptop! This is Dennis.")
    net.send_message(node1, node3, "Hello Tablet, can you hear me?")

    # 7. Remove the Laptop from the network and try messaging again
    net.remove_node(node2)
    net.send_message(node1, node2, "Are you still there, Laptop?")

    # 8. Display all messages stored at each node
    net.display_all_messages()

if __name__ == "__main__":
    main()
