graph = {
    "Chicago": [
        ("Detroit", 283),
        ("Cleveland", 345),
        ("Indianapolis", 182)
    ],

    "Detroit": [
        ("Chicago", 283),
        ("Cleveland", 169),
        ("Buffalo", 256)
    ],

    "Cleveland": [
        ("Chicago", 345),
        ("Detroit", 169),
        ("Buffalo", 189),
        ("Pittsburgh", 134),
        ("Columbus", 144)
    ],

    "Indianapolis": [
        ("Chicago", 182),
        ("Columbus", 176)
    ],

    "Columbus": [
        ("Indianapolis", 176),
        ("Cleveland", 144),
        ("Pittsburgh", 185)
    ],

    "Buffalo": [
        ("Detroit", 256),
        ("Cleveland", 189),
        ("Syracuse", 150)
    ],

    "Pittsburgh": [
        ("Cleveland", 134),
        ("Columbus", 185),
        ("Philadelphia", 305),
        ("Baltimore", 247)
    ],

    "Syracuse": [
        ("Buffalo", 150),
        ("Boston", 312),
        ("New York", 254)
    ],

    "New York": [
        ("Syracuse", 254),
        ("Boston", 215),
        ("Philadelphia", 97),
        ("Providence", 181)
    ],

    "Philadelphia": [
        ("New York", 97),
        ("Pittsburgh", 305),
        ("Baltimore", 101)
    ],

    "Baltimore": [
        ("Philadelphia", 101),
        ("Pittsburgh", 247)
    ],

    "Boston": [
        ("Syracuse", 312),
        ("New York", 215),
        ("Providence", 50),
        ("Portland", 107)
    ],

    "Providence": [
        ("Boston", 50),
        ("New York", 181)
    ],

    "Portland": [
        ("Boston", 107)
    ]
}


# ---------------- Node ----------------
class Node:
    def __init__(self, state, parent=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost

    def solution_path(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

# ---------------- Priority Queue (by path cost) ----------------
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def push(self, item):
        self.elements.append(item)
        self.elements.sort(key=lambda x: x[0])  # sort by g(n)

    def pop(self):
        return self.elements.pop(0)

    def empty(self):
        return len(self.elements) == 0

# ---------------- EXPAND ----------------
def EXPAND(problem_graph, node):
    for neighbor, step_cost in problem_graph[node.state]:
        yield Node(
            state=neighbor,
            parent=node,
            path_cost=node.path_cost + step_cost
        )

# ---------------- Best-First (Uninformed / UCS) ----------------
def BEST_FIRST_SEARCH(problem_graph, start, goal):
    start_node = Node(start)

    frontier = PriorityQueue()
    frontier.push((0, start_node))  # (path_cost, node)

    reached = {start: start_node}

    while not frontier.empty():
        cost, node = frontier.pop()

        print(f"Expanding: {node.state}, g(n) = {node.path_cost}")

        if node.state == goal:
            return node

        for child in EXPAND(problem_graph, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.push((child.path_cost, child))

    return None

# ---------------- Run ----------------
goal_node = BEST_FIRST_SEARCH(graph, "Syracuse", "Chicago")

print("\nSolution Path:")
print(" -> ".join(goal_node.solution_path()))
print("Total Path Cost:", goal_node.path_cost)
