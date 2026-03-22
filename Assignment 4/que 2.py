# 'E' = Entry
# 'x' = Exit
# '.' = Free space
# 'W' / 'w' = Wall (blocked)

grid = [
    ['W','W','w','.','W','W','W','w'],
    ['.','.','.','.','W','w','w','w'],
    ['W','W','.','.','.','.','.','x'],
    ['W','W','w','.','w','.','W','W'],
    ['W','W','W','E','W','W','W','W']
]

start = (4, 3)   # Entry
goal  = (2, 7)   # Exit


def best_first_search_no_heuristic(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = set()

    queue = []                     # simple list as queue
    queue.append((start, [start])) # (node, path)

    while queue:
        (x, y), path = queue.pop(0)  # FIFO behavior

        print(f"Expanding: {(x, y)}")

        if (x, y) == goal:
            return path

        if (x, y) in visited:
            continue
        visited.add((x, y))

        # 4-directional movement
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x + dx, y + dy

            if (0 <= nx < rows and
                0 <= ny < cols and
                grid[nx][ny] not in ['W', 'w'] and
                (nx, ny) not in visited):

                queue.append(((nx, ny), path + [(nx, ny)]))

    return None


# Run
path = best_first_search_no_heuristic(grid, start, goal)

print("\nEvacuation Path:")
print(path)
