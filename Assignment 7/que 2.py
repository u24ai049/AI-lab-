import random
import math

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

# Steepest ascent (used inside random restart)
def steepest_ascent(board):
    current = board[:]
    steps = 0
    while True:
        best_h = heuristic(current)
        best_board = current[:]
        for col in range(8):
            for row in range(8):
                if row == current[col]:
                    continue
                neighbor = current[:]
                neighbor[col] = row
                h = heuristic(neighbor)
                if h < best_h:
                    best_h = h
                    best_board = neighbor[:]
        if heuristic(best_board) >= heuristic(current):
            break
        current = best_board
        steps += 1
    return current, heuristic(current), steps

# First-choice hill climbing
def first_choice(board):
    current = board[:]
    steps = 0
    while True:
        current_h = heuristic(current)
        if current_h == 0:
            break
        improved = False
        cols = list(range(8))
        random.shuffle(cols)
        for col in cols:
            rows = list(range(8))
            random.shuffle(rows)
            for row in rows:
                if row == current[col]:
                    continue
                neighbor = current[:]
                neighbor[col] = row
                if heuristic(neighbor) < current_h:
                    current = neighbor
                    steps += 1
                    improved = True
                    break
            if improved:
                break
        if not improved:
            break
    return heuristic(current), steps

# Random restart hill climbing
def random_restart(max_restarts=20):
    total_steps = 0
    restarts = 0
    for _ in range(max_restarts):
        board = random_board()
        result, final_h, steps = steepest_ascent(board)
        total_steps += steps
        restarts += 1
        if final_h == 0:
            return 0, total_steps, restarts
    return final_h, total_steps, restarts

# Simulated annealing
def simulated_annealing(board, T=30.0, cooling=0.95, min_T=0.01):
    current = board[:]
    steps = 0
    while T > min_T:
        current_h = heuristic(current)
        if current_h == 0:
            break
        col = random.randint(0, 7)
        row = random.randint(0, 7)
        neighbor = current[:]
        neighbor[col] = row
        nh = heuristic(neighbor)
        delta = nh - current_h
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
        T *= cooling
        steps += 1
    return heuristic(current), steps

# ─── Run all 3 variants on 50 boards ───
random.seed(42)
boards = [random_board() for _ in range(50)]

# First-Choice
print("=== First-Choice Hill Climbing ===")
print("Board | Initial H | Final H | Steps | Status")
print("-" * 50)
fc_solved = 0
fc_total_steps = 0
for i, b in enumerate(boards):
    init_h = heuristic(b)
    final_h, steps = first_choice(b[:])
    status = "Solved" if final_h == 0 else "Fail"
    if final_h == 0:
        fc_solved += 1
    fc_total_steps += steps
    print(f"  {i+1:<5} {init_h:<11} {final_h:<9} {steps:<7} {status}")
print(f"Solved: {fc_solved}/50 | Avg Steps: {fc_total_steps/50:.1f}")

# Random Restart
print("\n=== Random Restart Hill Climbing ===")
print("Board | Final H | Total Steps | Restarts | Status")
print("-" * 55)
rr_solved = 0
rr_total_steps = 0
for i, b in enumerate(boards):
    final_h, steps, restarts = random_restart(max_restarts=20)
    status = "Solved" if final_h == 0 else "Fail"
    if final_h == 0:
        rr_solved += 1
    rr_total_steps += steps
    print(f"  {i+1:<5} {final_h:<9} {steps:<13} {restarts:<10} {status}")
print(f"Solved: {rr_solved}/50 | Avg Steps: {rr_total_steps/50:.1f}")

# Simulated Annealing
print("\n=== Simulated Annealing ===")
print("Board | Initial H | Final H | Steps | Status")
print("-" * 50)
sa_solved = 0
sa_total_steps = 0
for i, b in enumerate(boards):
    init_h = heuristic(b)
    final_h, steps = simulated_annealing(b[:])
    status = "Solved" if final_h == 0 else "Fail"
    if final_h == 0:
        sa_solved += 1
    sa_total_steps += steps
    print(f"  {i+1:<5} {init_h:<11} {final_h:<9} {steps:<7} {status}")
print(f"Solved: {sa_solved}/50 | Avg Steps: {sa_total_steps/50:.1f}")

# Comparison Summary
print("\n=== Comparison Summary ===")
print(f"{'Algorithm':<25} {'Solved':>8} {'Avg Steps':>12}")
print("-" * 47)
print(f"{'First-Choice':<25} {fc_solved:>6}/50 {fc_total_steps/50:>12.1f}")
print(f"{'Random Restart':<25} {rr_solved:>6}/50 {rr_total_steps/50:>12.1f}")
print(f"{'Simulated Annealing':<25} {sa_solved:>6}/50 {sa_total_steps/50:>12.1f}")