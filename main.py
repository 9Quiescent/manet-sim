from node import Node
from world import World

def main():
    # Create a 10x10 world
    world = World(10, 10)

    # Add some walls
    world.add_wall((3, 3))
    world.add_wall((4, 4))
    world.add_wall((5, 2))
    print("Walls added.")

    # Add nodes/devices
    n1 = Node(1, "Phone", (1, 1), comm_range=2)
    n2 = Node(2, "Tablet", (2, 2), comm_range=2)
    n3 = Node(3, "Laptop", (5, 5), comm_range=2)
    n4 = Node(4, "SmartWatch", (8, 8), comm_range=2)

    print("Spawning nodes.")
    assert world.add_node(n1)
    assert world.add_node(n2)
    assert world.add_node(n3)
    assert world.add_node(n4)


    # Display initial state
    print("\nInitial world state:")
    world.display()

    # Simulate several steps
    STEPS = 5
    for t in range(1, STEPS + 1):
        print(f"\n--- Step {t} ---")
        world.step()
        world.display()
        print("Neighbor lists:")
        world.network.display_all_neighbors()
        print("-" * 40)

    # Demonstrate messaging between nodes that are neighbors
    print("\nMessaging demonstration:")
    world.network.send_message(n1, n2, "Hello from Phone to Tablet!")
    world.network.send_message(n2, n3, "Tablet here, Laptop!")
    world.network.send_message(n4, n1, "SmartWatch ping!")  # Might fail if not neighbors

    print("\nAll messages:")
    world.network.display_all_messages()

if __name__ == "__main__":
    main()
