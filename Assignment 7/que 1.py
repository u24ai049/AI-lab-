import random

# Heuristic: number of attacking pairs (lower is better, 0 = solved)
def heuristic(board):
    attacks = 0
    n = len(board)
    for i in range(n):
        for j in range(i+1, n):
            if board[i] == board[j]:
                attacks += 1
            if abs(board[i] - board[j]) == abs(i - j):
                attacks += 1
    return attacks

def random_board():
    return [random.randint(0, 7) for _ in range(8)]

def get_best_neighbor(board):
    best_h = heuristic(board)
    best_board = board[:]
    for col in range(8):
        for row in range(8):
            if row == board[col]:
                continue
            neighbor = board[:]
            neighbor[col] = row
            h = heuristic(neighbor)
            if h < best_h:
                best_h = h
                best_board = neighbor[:]
    return best_board, best_h

def steepest_ascent(board):
    current = board[:]
    initial_h = heuristic(current)
    steps = 0
    while True:
        neighbor, neighbor_h = get_best_neighbor(current)
        current_h = heuristic(current)
        if neighbor_h >= current_h:
            break  # local minimum reached
        current = neighbor
        steps += 1
    final_h = heuristic(current)
    return initial_h, final_h, steps

# Generate 50 random boards and run steepest ascent on each
random.seed(42)

print("Board | Initial H | Final H | Steps | Status")
print("-" * 50)

solved_count = 0
local_min_example = None

for i in range(50):
    board = random_board()
    initial_h, final_h, steps = steepest_ascent(board)
    status = "Solved" if final_h == 0 else "Fail"
    if final_h == 0:
        solved_count += 1
    if final_h > 0 and local_min_example is None:
        local_min_example = (board[:], final_h)
    print(f"  {i+1:<5} {initial_h:<11} {final_h:<9} {steps:<7} {status}")

print("-" * 50)
print(f"Total Solved: {solved_count}/50")
print(f"Total Failed (Local Minima): {50 - solved_count}/50")

# Prove the presence of a local minimum
print("\n--- Proof of Local Minimum ---")
board, stuck_h = local_min_example
print(f"Board: {board}")
print(f"Heuristic value at this board: {stuck_h}")
print("Checking all neighbors...")

all_worse_or_equal = True
for col in range(8):
    for row in range(8):
        if row == board[col]:
            continue
        neighbor = board[:]
        neighbor[col] = row
        nh = heuristic(neighbor)
        if nh < stuck_h:
            all_worse_or_equal = False
            print(f"  Better neighbor found at col={col} row={row} h={nh}")

if all_worse_or_equal:
    print("No neighbor has a lower heuristic value.")
    print("=> This is a confirmed LOCAL MINIMUM.")