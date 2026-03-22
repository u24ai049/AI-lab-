
import collections

# 1. Graph Data (Adjacency List)
graph = {
    "Chicago": {"Detroit": 283, "Cleveland": 345, "Indianapolis": 182},
    "Indianapolis": {"Chicago": 182, "Columbus": 176},
    "Columbus": {"Indianapolis": 176, "Cleveland": 144, "Pittsburgh": 185},
    "Detroit": {"Chicago": 283, "Cleveland": 169, "Buffalo": 256},
    "Cleveland": {
        "Chicago": 345,
        "Detroit": 169,
        "Columbus": 144,
        "Pittsburgh": 134,
        "Buffalo": 189,
    },
    "Buffalo": {"Detroit": 256, "Cleveland": 189, "Pittsburgh": 215, "Syracuse": 150},
    "Pittsburgh": {
        "Columbus": 185,
        "Cleveland": 134,
        "Buffalo": 215,
        "Philadelphia": 305,
        "Baltimore": 247,
    },
    "Syracuse": {"Buffalo": 150, "Philadelphia": 254, "New York": 253, "Boston": 312},
    "Boston": {"Syracuse": 312, "New York": 215, "Portland": 107, "Providence": 50},
    "New York": {"Syracuse": 253, "Philadelphia": 97, "Boston": 215, "Providence": 181},
    "Philadelphia": {
        "Syracuse": 254,
        "New York": 97,
        "Pittsburgh": 305,
        "Baltimore": 101,
    },
    "Baltimore": {"Pittsburgh": 247, "Philadelphia": 101},
    "Portland": {"Boston": 107},
    "Providence": {"Boston": 50, "New York": 181},
}


def calculate_cost(path):
    """Calculates the total mileage of a path list."""
    total = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        total += graph[u][v]
    return total


# 2. BFS to find ALL paths with Exploration Cost
def bfs_all_paths(start, goal):
    queue = collections.deque([[start]])
    paths = []
    
    # Track the total distance "traveled" by the algorithm (visiting nodes)
    exploration_cost = 0

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            # Append path and the exploration cost incurred *up to this point*
            paths.append((path, exploration_cost))
            continue

        # Explore neighbors
        for neighbor in graph[node]:
            # avoid cycles: don't visit neighbor if it's already in this path
            if neighbor not in path:
                # Add mileage for "traveling" to check this neighbor
                exploration_cost += graph[node][neighbor]
                
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return paths


# 3. DFS to find ALL paths with Exploration Cost
# We add a mutable 'stats' dictionary to track cost across recursive calls
def dfs_all_paths(current_node, goal, path, all_paths, stats):
    if current_node == goal:
        all_paths.append((list(path), stats['cost']))
        return

    for neighbor in graph[current_node]:
        if neighbor not in path:  # avoid cycles
            # Add mileage for traveling to neighbor
            stats['cost'] += graph[current_node][neighbor]
            
            path.append(neighbor)
            dfs_all_paths(neighbor, goal, path, all_paths, stats)
            path.pop()


# --- Example Usage ---
if __name__ == "__main__":
    start_city = "Syracuse"
    goal_city = "Chicago"

    print(f"Finding paths from {start_city} to {goal_city}...\n")

    # BFS Paths
    bfs_results = bfs_all_paths(start_city, goal_city)
    print("BFS Paths (sorted by discovery order):")
    for p, exp_cost in bfs_results:
        path_cost = calculate_cost(p)
        print(f"Path: {p}")
        print(f"  - Path Cost (Mileage): {path_cost}")
        print(f"  - Exploration Cost (Search Effort): {exp_cost}")
        print(f"  - Sum: {path_cost + exp_cost}\n")

    print(f"Total BFS paths found: {len(bfs_results)}")
    print("-" * 40 + "\n")

    # DFS Paths
    dfs_results = []
    # Initialize stats with cost 0
    exploration_stats = {'cost': 0}
    dfs_all_paths(start_city, goal_city, [start_city], dfs_results, exploration_stats)

    print("DFS Paths (sorted by discovery order):")
    for p, exp_cost in dfs_results:
        path_cost = calculate_cost(p)
        print(f"Path: {p}")
        print(f"  - Path Cost (Mileage): {path_cost}")
        print(f"  - Exploration Cost (Search Effort): {exp_cost}")
        print(f"  - Sum: {path_cost + exp_cost}\n")

    print(f"Total DFS paths found: {len(dfs_results)}")