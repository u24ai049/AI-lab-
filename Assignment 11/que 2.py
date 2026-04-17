"""
Q2: SEND + MORE = MONEY as CSP
Variables: S, E, N, D, M, O, R, Y
Constraints:
  - All digits 0-9, all unique
  - S != 0, M != 0
  - SEND + MORE = MONEY
Method: Backtracking with constraint propagation, column-by-column
"""
from itertools import permutations

# Brute force over all permutations (with pruning for leading zeros)
# SEND + MORE = MONEY
#  S E N D
#  M O R E
# M O N E Y

letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']

def solve():
    for perm in permutations(range(10), 8):
        S, E, N, D, M, O, R, Y = perm
        if S == 0 or M == 0:
            continue
        SEND  = 1000*S + 100*E + 10*N + D
        MORE  = 1000*M + 100*O + 10*R + E
        MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
        if SEND + MORE == MONEY:
            return S, E, N, D, M, O, R, Y
    return None

# CSP with column constraints (more principled)
def solve_csp():
    """
    Process column by column right to left with carry propagation.
    Column 0 (units):  D + E = Y + 10*c1
    Column 1 (tens):   N + R + c1 = E + 10*c2
    Column 2 (hundreds): E + O + c2 = N + 10*c3
    Column 3 (thousands): S + M + c3 = O + 10*c4
    Column 4 (ten-thousands): c4 = M
    => M = 1 (since max carry is 1), c4 = 1
    """
    solutions = []
    # M must be 1 (from c4 = M and c4 in {0,1})
    M = 1
    used = {M}

    for c3 in [0, 1]:
        for c2 in [0, 1]:
            for c1 in [0, 1]:
                for S in range(1, 10):  # S != 0
                    if S in used: continue
                    # col3: S + M + c3 = O + 10*c4, c4=1
                    O = S + M + c3 - 10
                    if O < 0 or O > 9 or O in {S, M}: continue

                    for E in range(0, 10):
                        if E in {S, M, O}: continue
                        # col2: E + O + c2 = N + 10*c3
                        N = E + O + c2 - 10*c3
                        if N < 0 or N > 9 or N in {S, M, O, E}: continue

                        for R in range(0, 10):
                            if R in {S, M, O, E, N}: continue
                            # col1: N + R + c1 = E + 10*c2
                            if (N + R + c1) % 10 != E: continue
                            if (N + R + c1) // 10 != c2: continue

                            for D in range(0, 10):
                                if D in {S, M, O, E, N, R}: continue
                                # col0: D + E = Y + 10*c1
                                Y = D + E - 10*c1
                                if Y < 0 or Y > 9: continue
                                if Y in {S, M, O, E, N, R, D}: continue

                                # Verify full equation
                                SEND  = 1000*S + 100*E + 10*N + D
                                MORE  = 1000*M + 100*O + 10*R + E
                                MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
                                if SEND + MORE == MONEY:
                                    solutions.append((S,E,N,D,M,O,R,Y))
    return solutions

print("=== SEND + MORE = MONEY (CSP - Column Constraint Propagation) ===\n")
solutions = solve_csp()
for S,E,N,D,M,O,R,Y in solutions:
    print(f"  S={S}, E={E}, N={N}, D={D}, M={M}, O={O}, R={R}, Y={Y}")
    print(f"  {1000*S+100*E+10*N+D} + {1000*M+100*O+10*R+E} = {10000*M+1000*O+100*N+10*E+Y}")
    print(f"  Verification: {1000*S+100*E+10*N+D} + {1000*M+100*O+10*R+E} = {1000*S+100*E+10*N+D + 1000*M+100*O+10*R+E}")