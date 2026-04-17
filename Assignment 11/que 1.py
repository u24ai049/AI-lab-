"""
Q1: Map Coloring of Gujarat districts as CSP
Constraints: no two adjacent districts share a color
Goal: minimum number of colors (chromatic number)
Method: Backtracking with Forward Checking + MRV + LCV heuristics
"""

# Gujarat districts (excluding Diu, Rann of Kuchchh, Little Rann of Kuchchh)

# Simplified — use clean district names only
districts = [
    'Kuchchh', 'Banaskantha', 'Patan', 'Mehsana', 'Sabarkantha',
    'GandhiNagar', 'Ahmedabad', 'Kheda', 'Panchmahal', 'Dahod',
    'Anand', 'Vadodara', 'Surendranagar', 'Rajkot', 'Jamnagar',
    'Porbandar', 'Junaghad', 'Amreli', 'Bhavnagar',
    'Bharuch', 'Narmada', 'Surat', 'Navsari', 'Valsad', 'Dangs'
]

# Adjacency list (based on Gujarat map)
adjacency = {
    'Kuchchh':       ['Banaskantha', 'Patan', 'Surendranagar', 'Rajkot', 'Jamnagar'],
    'Banaskantha':   ['Kuchchh', 'Patan', 'Mehsana', 'Sabarkantha'],
    'Patan':         ['Kuchchh', 'Banaskantha', 'Mehsana', 'Surendranagar'],
    'Mehsana':       ['Banaskantha', 'Patan', 'Sabarkantha', 'GandhiNagar', 'Ahmedabad', 'Surendranagar'],
    'Sabarkantha':   ['Banaskantha', 'Mehsana', 'GandhiNagar', 'Kheda', 'Panchmahal'],
    'GandhiNagar':   ['Mehsana', 'Sabarkantha', 'Ahmedabad', 'Kheda'],
    'Ahmedabad':     ['Mehsana', 'GandhiNagar', 'Kheda', 'Anand', 'Surendranagar'],
    'Kheda':         ['GandhiNagar', 'Sabarkantha', 'Ahmedabad', 'Anand', 'Panchmahal'],
    'Panchmahal':    ['Sabarkantha', 'Kheda', 'Anand', 'Vadodara', 'Dahod'],
    'Dahod':         ['Panchmahal', 'Vadodara'],
    'Anand':         ['Ahmedabad', 'Kheda', 'Panchmahal', 'Vadodara', 'Bharuch'],
    'Vadodara':      ['Anand', 'Panchmahal', 'Dahod', 'Bharuch', 'Narmada'],
    'Surendranagar': ['Kuchchh', 'Patan', 'Mehsana', 'Ahmedabad', 'Rajkot', 'Bhavnagar'],
    'Rajkot':        ['Kuchchh', 'Surendranagar', 'Jamnagar', 'Amreli'],
    'Jamnagar':      ['Kuchchh', 'Rajkot', 'Porbandar'],
    'Porbandar':     ['Jamnagar', 'Junaghad'],
    'Junaghad':      ['Porbandar', 'Rajkot', 'Amreli'],
    'Amreli':        ['Rajkot', 'Junaghad', 'Bhavnagar'],
    'Bhavnagar':     ['Surendranagar', 'Rajkot', 'Amreli', 'Bharuch'],
    'Bharuch':       ['Anand', 'Vadodara', 'Bhavnagar', 'Narmada', 'Surat'],
    'Narmada':       ['Vadodara', 'Bharuch', 'Surat', 'Dangs'],
    'Surat':         ['Bharuch', 'Narmada', 'Navsari', 'Dangs'],
    'Navsari':       ['Surat', 'Valsad', 'Dangs'],
    'Valsad':        ['Navsari', 'Dangs'],
    'Dangs':         ['Narmada', 'Surat', 'Navsari', 'Valsad'],
}

def is_consistent(district, color, assignment):
    for neighbor in adjacency[district]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def backtrack(assignment, num_colors):
    if len(assignment) == len(districts):
        return assignment
    # MRV: pick unassigned district with fewest legal colors
    unassigned = [d for d in districts if d not in assignment]
    var = min(unassigned, key=lambda d: sum(
        1 for c in range(num_colors) if is_consistent(d, c, assignment)
    ))
    # LCV: try colors that rule out fewest neighbor options first
    colors_ordered = sorted(range(num_colors), key=lambda c: sum(
        1 for n in adjacency[var] if n not in assignment and not is_consistent(n, c, {**assignment, var: c})
    ))
    for color in colors_ordered:
        if is_consistent(var, color, assignment):
            assignment[var] = color
            result = backtrack(assignment, num_colors)
            if result is not None:
                return result
            del assignment[var]
    return None

# Find chromatic number that will fit the map
for k in range(2, 6):
    result = backtrack({}, k)
    if result:
        print(f"Chromatic number: {k} colors")
        color_names = ['Red', 'Blue', 'Green', 'Yellow', 'Purple']
        print("\nColoring:")
        for d, c in sorted(result.items()):
            print(f"  {d:20s} → {color_names[c]}")
        # Verify
        ok = True
        for d in districts:
            for n in adjacency[d]:
                if result.get(d) == result.get(n):
                    print(f"CONFLICT: {d} - {n}")
                    ok = False
        print(f"\nValid coloring: {ok}")
        break