# 'E' = Entry
# 'X' = Exit
# '.' = Free hallway space
# 'W' / 'w' = Wall (blocked)

grid = [
    ['W','W','w','.','W','W','W','w'],
    ['.','.','.','.','W','w','w','w'],
    ['W','W','.','.','.','.','.','x'],
    ['W','W','w','.','w','.','W','W'],
    ['W','W','W','E','W','W','W','W']
]

start = (4, 3)   # Entry (E)
goal  = (2, 7)   # Exit (x)


# ---------------- Priority Queue ----------------
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def push(self, item):
        self.elements.append(item)
        self.elements.sort(key=lambda x: x[0])  # sort by cost

    def pop(self):
        return self.elements.pop(0)

    def empty(self):
        return len(self.elements) == 0


# ---------------- Uniform Cost Search ----------------
def uniform_cost_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = set()

    pq = PriorityQueue()
    pq.push((0, start, [start]))  # (cost, (row,col), path)

    while not pq.empty():
        cost, (x, y), path = pq.pop()

        if (x, y) == goal:
            return path, cost

        if (x, y) in visited:
            continue
        visited.add((x, y))

        # 4-direction me  movement
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x + dx, y + dy

            if (0 <= nx < rows and
                0 <= ny < cols and
                grid[nx][ny] not in ['W', 'w']):
                
                pq.push((cost + 1, (nx, ny), path + [(nx, ny)]))

    return None, float('inf')


# chale chalake dekhte hai maja ayega
path, cost = uniform_cost_search(grid, start, goal)

print("Evacuation Path:", path)
print("Total Cost:", cost)
