from node import Node
from world import World
from worldGUI import WorldGUI


def main():
    # Set up world and nodes
    world = World(10, 10)

    world.create_node(1, "Phone", (1, 1), comm_range=2, base_color="#ff0000") # red
    world.create_node(2, "Tablet", (2, 2), comm_range=2, base_color="#007fff") # blue
    world.create_node(3, "Laptop", (5, 5), comm_range=2, base_color="#24c81e") # green
    world.create_node(4, "SmartWatch", (8, 8), comm_range=2, base_color="#ff9000") # orange

    # Launch GUI, passing the world (all simulation happens through the GUI)
    gui = WorldGUI(world)
    gui.run()


if __name__ == "__main__":
    main()
