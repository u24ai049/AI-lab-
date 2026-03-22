# -----------------------------
# Node Definition
# -----------------------------
class Node:
    def __init__(self, state, parent=None, g=0, f=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.f = f


# -----------------------------
# Graph Representation
# -----------------------------
graph = {
    "Chicago": [("Detroit", 283), ("Cleveland", 345), ("Indianapolis", 182)],
    "Detroit": [("Chicago", 283), ("Buffalo", 256), ("Cleveland", 169)],
    "Cleveland": [("Chicago", 345), ("Detroit", 169), ("Buffalo", 189),
                  ("Pittsburgh", 134), ("Columbus", 144)],
    "Indianapolis": [("Chicago", 182), ("Columbus", 176)],
    "Columbus": [("Indianapolis", 176), ("Cleveland", 144), ("Pittsburgh", 185)],
    "Pittsburgh": [("Cleveland", 134), ("Columbus", 185), ("Buffalo", 215),
                   ("Philadelphia", 305), ("Baltimore", 247)],
    "Buffalo": [("Detroit", 256), ("Cleveland", 189), ("Pittsburgh", 215),
                ("Syracuse", 150)],
    "Syracuse": [("Buffalo", 150), ("Boston", 312), ("New York", 254),
                 ("Philadelphia", 253)],
    "New York": [("Syracuse", 254), ("Boston", 215), ("Providence", 181),
                 ("Philadelphia", 97)],
    "Philadelphia": [("Pittsburgh", 305), ("Syracuse", 253),
                     ("New York", 97), ("Baltimore", 101)],
    "Baltimore": [("Pittsburgh", 247), ("Philadelphia", 101)],
    "Boston": [("Syracuse", 312), ("New York", 215),
               ("Providence", 50), ("Portland", 107)],
    "Providence": [("Boston", 50), ("New York", 181)],
    "Portland": [("Boston", 107)]
}


# -----------------------------
# Heuristic Values (to Boston)
# -----------------------------
heuristic = {
    "Boston": 0,
    "Providence": 50,
    "Portland": 107,
    "New York": 215,
    "Philadelphia": 270,
    "Baltimore": 360,
    "Syracuse": 260,
    "Buffalo": 400,
    "Pittsburgh": 470,
    "Cleveland": 550,
    "Columbus": 640,
    "Detroit": 610,
    "Indianapolis": 780,
    "Chicago": 860
}


# -----------------------------
# Remove node with minimum f(n)
# -----------------------------
def pop_min(frontier):
    min_index = 0
    for i in range(1, len(frontier)):
        if frontier[i].f < frontier[min_index].f:
            min_index = i
    return frontier.pop(min_index)


# -----------------------------
# Print Final Path
# -----------------------------
def print_solution(goal_node):
    path = []
    total_cost = goal_node.g

    while goal_node:
        path.append(goal_node.state)
        goal_node = goal_node.parent

    path.reverse()

    print("\nFinal Path:", " -> ".join(path))
    print("Total Cost:", total_cost)


# -----------------------------
# Best First Search (Greedy / A*)
# -----------------------------
def best_first_search(start, goal, use_astar=False):

    frontier = []
    explored = set()
    step = 0
    explored_count = 0

    start_node = Node(start, None, 0, heuristic[start])
    frontier.append(start_node)

    print("\n=================================================")
    if use_astar:
        print("A* SEARCH")
    else:
        print("GREEDY BEST-FIRST SEARCH")
    print("=================================================")

    print(f"\nStart at {start}")
    print(f"Initial h(n) = {heuristic[start]}")

    while frontier:

        current = pop_min(frontier)
        step += 1

        if current.state in explored:
            continue

        explored.add(current.state)
        explored_count += 1

        print(f"\nStep {step}: Expanding {current.state}")
        print(f"g(n) = {current.g}")
        print(f"h(n) = {heuristic[current.state]}")
        print(f"f(n) = {current.f}")

        if current.state == goal:
            print("\nGoal Reached!")
            print_solution(current)
            print("Cities Explored:", explored_count)
            return

        print("\nGenerating Children:")

        for neighbor, cost in graph[current.state]:

            if neighbor not in explored:

                g_new = current.g + cost

                if use_astar:
                    f_new = g_new + heuristic[neighbor]
                else:
                    f_new = heuristic[neighbor]

                print(f"{neighbor}: g={g_new}, h={heuristic[neighbor]}, f={f_new}")

                child = Node(neighbor, current, g_new, f_new)
                frontier.append(child)

        print("\nFrontier:")
        for node in frontier:
            print(f"{node.state} (f={node.f})")

    print("No Path Found.")


# -----------------------------
# RUN BOTH
# -----------------------------
best_first_search("Chicago", "Boston", use_astar=False)
best_first_search("Chicago", "Boston", use_astar=True)