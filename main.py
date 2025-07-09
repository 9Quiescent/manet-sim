from node import Node
from world import World
from worldGUI import WorldGUI  # This is your Tkinter GUI class as sketched above


def main():
    # Set up world and nodes
    world = World(10, 10)

    n1 = Node(1, "Phone", (1, 1), comm_range=2)
    n2 = Node(2, "Tablet", (2, 2), comm_range=2)
    n3 = Node(3, "Laptop", (5, 5), comm_range=2)
    n4 = Node(4, "SmartWatch", (8, 8), comm_range=2)

    world.add_node(n1)
    world.add_node(n2)
    world.add_node(n3)
    world.add_node(n4)

    # Launch GUI, passing the world (all simulation happens through the GUI)
    gui = WorldGUI(world)
    gui.run()


if __name__ == "__main__":
    main()
