import math

def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != '.':
            return board[a]
    return None

def is_full(board):
    return '.' not in board

# Plain minimax - counts nodes
def minimax(board, is_max, depth=0, counter=None):
    if counter is None:
        counter = [0]
    counter[0] += 1

    winner = check_winner(board)
    if winner == 'X': return 10 - depth, counter
    if winner == 'O': return depth - 10, counter
    if is_full(board): return 0, counter

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == '.':
                board[i] = 'X'
                val, _ = minimax(board, False, depth+1, counter)
                best = max(best, val)
                board[i] = '.'
        return best, counter
    else:
        best = math.inf
        for i in range(9):
            if board[i] == '.':
                board[i] = 'O'
                val, _ = minimax(board, True, depth+1, counter)
                best = min(best, val)
                board[i] = '.'
        return best, counter

# Alpha-Beta pruning - counts nodes
def alphabeta(board, is_max, alpha=-math.inf, beta=math.inf, depth=0, counter=None):
    if counter is None:
        counter = [0]
    counter[0] += 1

    winner = check_winner(board)
    if winner == 'X': return 10 - depth, counter
    if winner == 'O': return depth - 10, counter
    if is_full(board): return 0, counter

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == '.':
                board[i] = 'X'
                val, _ = alphabeta(board, False, alpha, beta, depth+1, counter)
                best = max(best, val)
                alpha = max(alpha, best)
                board[i] = '.'
                if beta <= alpha:
                    break
        return best, counter
    else:
        best = math.inf
        for i in range(9):
            if board[i] == '.':
                board[i] = 'O'
                val, _ = alphabeta(board, True, alpha, beta, depth+1, counter)
                best = min(best, val)
                beta = min(beta, best)
                board[i] = '.'
                if beta <= alpha:
                    break
        return best, counter

def best_move_ab(board):
    best_val = -math.inf
    move = -1
    for i in range(9):
        if board[i] == '.':
            board[i] = 'X'
            val, _ = alphabeta(board, False)
            board[i] = '.'
            if val > best_val:
                best_val = val
                move = i
    return move

def compare(board):
    print("Board state:", board)
    _, c1 = minimax(list(board), True, counter=[0])
    _, c2 = alphabeta(list(board), True, counter=[0])
    print(f"Minimax nodes evaluated : {c1[0]}")
    print(f"Alpha-Beta nodes evaluated: {c2[0]}")
    pruned = c1[0] - c2[0]
    pct = (pruned / c1[0]) * 100 if c1[0] else 0
    print(f"Nodes pruned: {pruned} ({pct:.1f}%)\n")

def print_board(board):
    for i in range(0, 9, 3):
        print(board[i], board[i+1], board[i+2])
    print()

def play():
    board = ['.'] * 9
    print("You are O, AI is X (Alpha-Beta)\n")
    print_board(board)

    while True:
        move = best_move_ab(board)
        board[move] = 'X'
        print(f"AI plays at {move}")
        print_board(board)

        if check_winner(board):
            print("AI wins!")
            break
        if is_full(board):
            print("Draw!")
            break

        while True:
            try:
                pos = int(input("Your move (0-8): "))
                if board[pos] == '.':
                    board[pos] = 'O'
                    break
                else:
                    print("Cell taken.")
            except (ValueError, IndexError):
                print("Invalid.")

        print_board(board)

        if check_winner(board):
            print("You win!")
            break
        if is_full(board):
            print("Draw!")
            break

if __name__ == "__main__":
    # Compare efficiency on a few board states
    print("=== Efficiency Comparison ===\n")
    compare(['.'] * 9)                                      # empty board
    compare(['X','O','X', '.','O','.', '.','.','.'])        # mid-game
    compare(['X','O','X', 'O','X','.', '.','O','.'])        # near end

    print("\n=== Play vs AI ===\n")
    play()