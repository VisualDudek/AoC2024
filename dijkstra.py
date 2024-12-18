# type: ignore
import heapq


def dijkstra(graph, start):
    """
    Implements Dijkstra's algorithm using a min-heap.

    Parameters:
        graph (dict): A dictionary where keys are nodes and values are lists of (neighbor, weight).
        start: The starting node for Dijkstra's algorithm.

    Returns:
        distances (dict): The shortest distances from the start node to all other nodes.
    """
    # Initialize distances with infinity, except the start node
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    # Min-heap to store (distance, node)
    min_heap = [(0, start)]

    # Track visited nodes
    visited = set()

    while min_heap:
        # Pop the node with the smallest distance
        current_distance, current_node = heapq.heappop(min_heap)

        # Skip if this node has been visited
        if current_node in visited:
            continue
        visited.add(current_node)

        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            # If a shorter path to neighbor is found, update it
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(min_heap, (distance, neighbor))

    return distances


# Example usage:
if __name__ == "__main__":
    # Graph represented as an adjacency list
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("A", 1), ("C", 2), ("D", 5)],
        "C": [("A", 4), ("B", 2), ("D", 1)],
        "D": [("B", 5), ("C", 1)],
    }
    start_node = "A"
    shortest_distances = dijkstra(graph, start_node)

    print("Shortest distances from start node:", start_node)
    for node, distance in shortest_distances.items():
        print(f"Distance to {node}: {distance}")
