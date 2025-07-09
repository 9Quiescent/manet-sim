import random
from typing import List, Tuple
from node import Node
from network import Network

class World:
    """
    Represents the simulation world (arena) for MANET nodes.
    Handles spatial logic: boundaries, collision, movement.
    """

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.network: Network = Network()
        self.walls: List[Tuple[int, int]] = []  # Each wall is a coordinate (x, y)

    def add_node(self, node: Node) -> bool:
        """Add node if space is free and within bounds. Returns True if successful."""
        if self.is_occupied(node.position) or not self.in_bounds(node.position):
            print(f"Failed to add node {node.node_name} at {node.position}: space occupied or out of bounds.")
            return False
        self.network.add_node(node)
        return True

    def add_wall(self, pos: Tuple[int, int]):
        """Add a wall (impassable space) at given coordinate."""
        if self.in_bounds(pos):
            self.walls.append(pos)

    def in_bounds(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def is_occupied(self, pos: Tuple[int, int]) -> bool:
        """Check if the position is occupied by a node or a wall."""
        for node in self.network.nodes:
            if node.position == pos:
                return True
        if pos in self.walls:
            return True
        return False

    def move_node_random(self, node: Node, max_step: int = 1):
        """Move node to a random adjacent square, avoiding collisions and walls."""
        possible_moves = [
            (node.position[0] + dx, node.position[1] + dy)
            for dx in [-max_step, 0, max_step]
            for dy in [-max_step, 0, max_step]
            if not (dx == 0 and dy == 0)
        ]
        random.shuffle(possible_moves)
        for new_pos in possible_moves:
            if self.in_bounds(new_pos) and not self.is_occupied(new_pos):
                node.move(new_pos)
                return
        # If no move possible, stay in place

    def step(self) -> List:
        """
        For each node in the network, plan a move to a random neighboring cell (if possible),
        while ensuring that:
          - No two nodes plan to move to the same cell (this simulates atomic, simultaneous movement).
          - No node moves into a wall or already occupied cell.
        Returns:
          - List of tuples: (node, original_position, new_position), used for GUI animation.
        """
        moves = []  # Stores each node's planned move as (node, old_pos, new_pos).

        # 'reserved' keeps track of all cells that are either already occupied,
        # or claimed as a destination by another node for this step.
        reserved = set(node.position for node in self.network.nodes)  # Start with all current node locations.

        for node in self.network.nodes:
            found = False  # Flag to check if a valid move is found for this node.
            # Generate all adjacent positions (including diagonals, excluding staying still).
            possible_moves = [
                (node.position[0] + dx, node.position[1] + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if not (dx == 0 and dy == 0)
            ]
            random.shuffle(possible_moves)  # Shuffle to ensure random movement.
            for new_pos in possible_moves:
                # Only allow a move if:
                #   1. It's inside the world boundaries.
                #   2. The cell isn't currently occupied (wall or node).
                #   3. No other node has already reserved this cell as a destination this step.
                if self.in_bounds(new_pos) and not self.is_occupied(new_pos) and new_pos not in reserved:
                    moves.append((node, node.position, new_pos))  # Store this planned move.
                    reserved.add(new_pos)  # Mark destination as reserved so no other node uses it this tick.
                    found = True
                    break  # No need to check further; we found a valid move.
            if not found:
                # If no valid move, the node stays in place (can't overlap others or move into a wall).
                moves.append((node, node.position, node.position))
                reserved.add(node.position)  # Still reserve its current cell so others can't overlap it either.
        return moves
    def display(self):
        """Text display of world state (for CLI/demo)."""
        print(f"World {self.width}x{self.height}")
        for node in self.network.nodes:
            print(f"- {node.node_name} at {node.position}")
        if self.walls:
            print(f"Walls at: {self.walls}")

