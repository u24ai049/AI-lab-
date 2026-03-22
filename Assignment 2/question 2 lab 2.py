# DFS for 8-puzzle
# 0 = blank

def get_neighbors(state):
    neigh = []

    z = state.index(0)
    r = z // 3
    c = z % 3

    # You can change move order here:
    # L, R, U, D
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for dr, dc in moves:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nz = nr * 3 + nc
            new_state = list(state)
            new_state[z], new_state[nz] = new_state[nz], new_state[z]
            neigh.append(tuple(new_state))

    return neigh


def dfs_8_puzzle(start, goal, depth_limit=150):
    # Stack stores (state, depth)
    stack = [(start, 0)]
    visited = set([start])

    parent = {start: None}
    explored = 0

    while len(stack) > 0:
        cur, depth = stack.pop()   # DFS pop from end
        explored += 1

        if cur == goal:
            # reconstruct path
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path, explored

        if depth >= depth_limit:
            continue

        neighbors = get_neighbors(cur)

        # IMPORTANT:
        # DFS stack me last neighbor pehle explore hota hai
        # So same order maintain karne ke liye reverse push karte hain
        for nxt in reversed(neighbors):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                stack.append((nxt, depth + 1))

    return None, explored


def print_state(s):
    for i in range(0, 9, 3):
        row = s[i:i+3]
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()


# --------- GIVEN PUZZLE ----------
start = (7, 2, 4,
         5, 0, 6,
         8, 3, 1)

goal = (0, 1, 2,
        3, 4, 5,
        6, 7, 8)

path, explored = dfs_8_puzzle(start, goal, depth_limit=80)

if path is None:
    print("No solution found within depth limit.")
    print("States explored:", explored)
else:
    print("✅ DFS found a solution!")
    print("Moves in DFS solution:", len(path) - 1)
    print("States explored (DFS):", explored)

    # Uncomment to print full path
    # for step, st in enumerate(path):
    #     print("Step", step)
    #     print_state(st)
