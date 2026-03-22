# 1. Define the Graph
graph = {
    "Raj": ["Priya", "Akash", "Sunil"],
    "Priya": ["Raj", "Aarav", "Neha (Center)", "Akash"],
    "Aarav": ["Priya", "Neha (Right)", "Arjun (Right)"],
    "Sunil": ["Raj", "Akash", "Sneha", "Maya"],
    "Akash": ["Raj", "Priya", "Sunil", "Neha (Center)"],
    "Neha (Center)": ["Priya", "Akash", "Sneha", "Rahul", "Neha (Right)"],
    "Sneha": ["Sunil", "Neha (Center)", "Rahul", "Maya"],
    "Rahul": [
        "Neha (Center)",
        "Neha (Right)",
        "Sneha",
        "Arjun (Right)",
        "Pooja",
        "Arjun (Bottom)",
        "Maya",
    ],
    "Maya": ["Sunil", "Sneha", "Rahul", "Arjun (Bottom)"],
    "Neha (Right)": ["Aarav", "Neha (Center)", "Rahul", "Arjun (Right)"],
    "Arjun (Right)": ["Aarav", "Neha (Right)", "Rahul", "Pooja"],
    "Arjun (Bottom)": ["Maya", "Rahul", "Pooja"],
    "Pooja": ["Rahul", "Arjun (Bottom)", "Arjun (Right)"],
}


def get_bfs_tree_edges(graph, start_node):
    """Generates edges for a BFS Tree."""
    visited = {start_node}
    queue = [start_node]   # normal list as queue
    bfs_edges = []

    while len(queue) > 0:
        parent = queue.pop(0)   # pop from front (like popleft)

        for neighbor in graph[parent]:
            if neighbor not in visited:
                visited.add(neighbor)
                bfs_edges.append(f"{parent} -> {neighbor}")
                queue.append(neighbor)

    return bfs_edges


def get_dfs_tree_edges(graph, start_node, visited=None, dfs_edges=None):
    """Generates edges for a DFS Tree (Recursive)."""
    if visited is None:
        visited = set()
    if dfs_edges is None:
        dfs_edges = []

    visited.add(start_node)

    for neighbor in graph[start_node]:
        if neighbor not in visited:
            dfs_edges.append(f"{start_node} -> {neighbor}")
            get_dfs_tree_edges(graph, neighbor, visited, dfs_edges)

    return dfs_edges


# --- Execute ---
start_node = "Raj"

print(f"--- BFS Tree (Starting at {start_node}) ---")
bfs_tree = get_bfs_tree_edges(graph, start_node)
for edge in bfs_tree:
    print(edge)

print(f"\n--- DFS Tree (Starting at {start_node}) ---")
dfs_tree = get_dfs_tree_edges(graph, start_node)
for edge in dfs_tree:
    print(edge)
