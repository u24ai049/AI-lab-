# -----------------------------
# Maze Definition (5x5)
# -----------------------------

maze = [
    [2,0,0,0,1],
    [0,1,0,0,3],
    [0,3,0,1,1],
    [0,1,0,0,1],
    [3,0,0,0,3]
]

ROWS = 5
COLS = 5


# -----------------------------
# Find Start and Rewards
# -----------------------------
start = None
rewards = set()

for i in range(ROWS):
    for j in range(COLS):
        if maze[i][j] == 2:
            start = (i,j)
        if maze[i][j] == 3:
            rewards.add((i,j))


# -----------------------------
# Node Class
# -----------------------------
class Node:
    def __init__(self, position, remaining_rewards, parent=None, g=0, f=0):
        self.position = position
        self.remaining_rewards = remaining_rewards
        self.parent = parent
        self.g = g
        self.f = f


# -----------------------------
# Manhattan Distance
# -----------------------------
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# -----------------------------
# Heuristic (Nearest Reward)
# -----------------------------
def heuristic(position, remaining_rewards):

    if not remaining_rewards:
        return 0

    return min(manhattan(position, r) for r in remaining_rewards)


# -----------------------------
# Remove Node with Minimum f
# -----------------------------
def pop_min(frontier):
    min_index = 0
    for i in range(1, len(frontier)):
        if frontier[i].f < frontier[min_index].f:
            min_index = i
    return frontier.pop(min_index)


# -----------------------------
# Reconstruct Path
# -----------------------------
def print_path(goal_node):

    path = []

    while goal_node:
        path.append(goal_node.position)
        goal_node = goal_node.parent

    path.reverse()

    print("\nFinal Optimal Path:")
    for p in path:
        print(p, end=" ")
    print("\nTotal Steps:", len(path)-1)


# -----------------------------
# A* Algorithm with Step Printing
# -----------------------------
def astar_multi_goal():

    frontier = []
    explored = set()
    step = 0

    h_start = heuristic(start, rewards)

    print("Starting at:", start)
    print(f"Initial g=0, h={h_start}, f={h_start}\n")

    start_node = Node(start, frozenset(rewards), None, 0, h_start)
    frontier.append(start_node)

    while frontier:

        current = pop_min(frontier)
        step += 1

        state_id = (current.position, current.remaining_rewards)

        if state_id in explored:
            continue

        explored.add(state_id)

        print(f"\n---------------- Step {step} ----------------")
        print(f"Expanding: {current.position}")
        print(f"g(n) = {current.g}")
        print(f"h(n) = {current.f - current.g}")
        print(f"f(n) = {current.f}")
        print(f"Remaining Rewards: {current.remaining_rewards}")

        remaining = set(current.remaining_rewards)

        if current.position in remaining:
            print("Collected reward at", current.position)
            remaining.remove(current.position)

        if not remaining:
            print("\nAll Rewards Collected!")
            print_path(current)
            print("States Explored:", len(explored))
            return

        print("\nGenerating Children:")

        x, y = current.position
        moves = [(x,y-1), (x,y+1), (x-1,y), (x+1,y)]

        for nx, ny in moves:

            if 0 <= nx < ROWS and 0 <= ny < COLS:
                if maze[nx][ny] != 1:

                    g_new = current.g + 1
                    h_new = heuristic((nx,ny), remaining)
                    f_new = g_new + h_new

                    print(f"Child {(nx,ny)} → g={g_new}, h={h_new}, f={f_new}")

                    child = Node((nx,ny),
                                 frozenset(remaining),
                                 current,
                                 g_new,
                                 f_new)

                    frontier.append(child)

        print("\nCurrent Frontier:")
        for node in frontier:
            print(f"{node.position} (f={node.f})")


# -----------------------------
# Run
# -----------------------------
astar_multi_goal()