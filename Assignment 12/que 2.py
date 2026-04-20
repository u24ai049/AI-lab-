import collections

# Input Data
grid_str = """
0 0 0 0 0 6 0 0 0
0 5 9 0 0 0 0 0 8
2 0 0 0 0 8 0 0 0
0 4 5 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 6 0 0 3 0 5 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 2
"""

def setup_sudoku():
    # Parse the grid
    rows = grid_str.strip().split('\n')
    grid = []
    for row in rows:
        grid.append([int(x) for x in row.split()])
        
    variables = [(r, c) for r in range(9) for c in range(9)]
    domains = {}
    
    # Initialize domains
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                domains[(r, c)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                domains[(r, c)] = [grid[r][c]]
                
    # Generate neighbors (arcs)
    neighbors = {v: set() for v in variables}
    for r in range(9):
        for c in range(9):
            # Same row
            for c2 in range(9):
                if c != c2:
                    neighbors[(r, c)].add((r, c2))
            # Same column
            for r2 in range(9):
                if r != r2:
                    neighbors[(r, c)].add((r2, c))
            # Same 3x3 block
            br, bc = r // 3, c // 3
            for r2 in range(br * 3, br * 3 + 3):
                for c2 in range(bc * 3, bc * 3 + 3):
                    if (r, c) != (r2, c2):
                        neighbors[(r, c)].add((r2, c2))
                        
    return variables, domains, neighbors

def REVISE(domains, Xi, Xj):
    """
    function REVISE(csp, Xi, Xj) returns true iff we revise the domain of Xi
    """
    revised = False
    # Iterate over a copy since we might modify the list
    for x in list(domains[Xi]):
        satisfies = False
        # Constraint: x != y for all neighbors
        for y in domains[Xj]:
            if x != y:
                satisfies = True
                break
        
        if not satisfies:
            domains[Xi].remove(x)
            revised = True
            
    return revised

def AC3(variables, domains, neighbors):
    """
    function AC-3(csp) returns false if an inconsistency is found and true otherwise
    """
    queue = collections.deque()
    for Xi in variables:
        for Xj in neighbors[Xi]:
            queue.append((Xi, Xj))
            
    while queue:
        Xi, Xj = queue.popleft()
        
        if REVISE(domains, Xi, Xj):
            if len(domains[Xi]) == 0:
                return False
            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
                    
    return True

if __name__ == "__main__":
    variables, domains, neighbors = setup_sudoku()
    
    # Calculate initial domain sizes
    initial_total_values = sum(len(domains[v]) for v in variables)
    
    # Calculate total number of binary constraints (arcs)
    total_arcs = sum(len(neighbors[v]) for v in variables)
    print(f"1. Arc Generation: Generated {total_arcs} binary constraints (arcs).")
    
    # Run AC-3
    print("\nRunning AC-3...")
    is_consistent = AC3(variables, domains, neighbors)
    
    # Calculate final domain sizes
    final_total_values = sum(len(domains[v]) for v in variables)
    values_removed = initial_total_values - final_total_values
    
    print(f"\n2. State Tracking: {values_removed} values were removed from all domains combined.")
    
    print("\n3. Visualization: Grid showing the remaining domain size for each cell:")
    for r in range(9):
        row_sizes = []
        for c in range(9):
            row_sizes.append(str(len(domains[(r, c)])))
        print(" ".join(row_sizes))
        
    print("\n--- Key Question ---")
    if not is_consistent:
        print("Does AC-3 reduce any domain to zero? YES. AC-3 returned False, meaning the puzzle is unsolvable based on the initial state and rules (or there's a contradiction).")
    else:
        all_solved = all(len(domains[v]) == 1 for v in variables)
        if all_solved:
            print("Does AC-3 reduce all domains to one? YES. The puzzle was completely solved by AC-3!")
            print("Solution:")
            for r in range(9):
                row_vals = []
                for c in range(9):
                    row_vals.append(str(domains[(r, c)][0]))
                print(" ".join(row_vals))
        else:
            print("Did AC-3 reduce any domain to zero or all domains to one? NO.")
            print("AC-3 finished successfully but could not reduce all domains to 1. The puzzle is partially solved (possibilities thinned out), and backtracking/guessing would be required to finish it.")