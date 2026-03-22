# 0 = blank

def get_neighbors(state):
    neighbors_list = []

    z = state.index(0)   # blank position (0..8) 0-indexing ki hai

    # convert index -> (row, col) 
    r = z // 3
    c = z % 3

    # possible moves: Left, Right, Up, Down
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for dr, dc in moves:
        nr = r + dr
        nc = c + dc

        if 0 <= nr < 3 and 0 <= nc < 3:
            nz = nr * 3 + nc

            new_state = list(state)
            new_state[z], new_state[nz] = new_state[nz], new_state[z]

            neighbors_list.append(tuple(new_state))

    return neighbors_list


def bfs_8_puzzle(start, goal):
    # queue using list 
    queue = [start]

    visited = set([start])
    parent = {start: None}

    explored = 0  # number of expanded states

    while len(queue) > 0:
        cur = queue.pop(0)   # pop front
        explored += 1

        if cur == goal:
            break

        for nxt in get_neighbors(cur):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                queue.append(nxt)

    if goal not in parent:
        return None, explored

    # reconstruct path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path, explored


def print_state(state):
    for i in range(0, 9, 3):
        row = state[i:i+3]
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()


# ---- Run on the given image puzzle ----
start = (7, 2, 4,
         5, 0, 6,
         8, 3, 1)

goal = (0, 1, 2,
        3, 4, 5,
        6, 7, 8)

path, explored = bfs_8_puzzle(start, goal)

if path is None:
    print("No solution found.")
    print("States explored:", explored-1)
else:
    print("✅ Solution found")
    print("Moves needed:", len(path) - 1)
    print("States explored before reaching goal:", explored-1)























    # Uncomment to print full path
    #for step, st in enumerate(path):
    #     print("Step", step)
    #     print_state(st)

#explanation = """https://chatgpt.com/c/696ce76a-e1a8-8333-b3d1-967ab36b66be"""
