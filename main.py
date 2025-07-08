from node import Node

def main():
    # Create some simple nodes
    node1 = Node(1, "Dennis' iPhone", (100, 200))
    node2 = Node(2, "Laptop", (150, 210))
    node3 = Node(3, "Tablet", (400, 220))

    print("Initial nodes:")
    print(node1)
    print(node2)
    print(node3)


if __name__ == "__main__":
    main()
