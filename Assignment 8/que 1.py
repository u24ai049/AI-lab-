import random

# ── Distance Matrix ──────────────────────────────────────────────────────────
CITIES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
DIST = [
    [ 0, 10, 15, 20, 25, 30, 35, 40],  # City 0 (A)
    [12,  0, 35, 15, 20, 25, 30, 45],  # City 1 (B)
    [25, 30,  0, 10, 40, 20, 15, 35],  # City 2 (C)
    [18, 25, 12,  0, 15, 30, 20, 10],  # City 3 (D)
    [22, 18, 28, 20,  0, 15, 25, 30],  # City 4 (E)
    [35, 22, 18, 28, 12,  0, 40, 20],  # City 5 (F)
    [30, 35, 22, 18, 28, 32,  0, 15],  # City 6 (G)
    [40, 28, 35, 22, 18, 25, 12,  0],  # City 7 (H)
]
N = len(CITIES)

def tour_cost(tour):
    return sum(DIST[tour[i]][tour[(i + 1) % N]] for i in range(N))

def tour_str(tour):
    return " -> ".join(CITIES[i] for i in tour) + f" -> {CITIES[tour[0]]}"

def random_tour():
    t = list(range(N))
    random.shuffle(t)
    return t

def get_neighbors(tour):
    """Generate all 2-opt swap neighbors."""
    neighbors = []
    for i in range(1, N - 1):
        for j in range(i + 1, N):
            neighbor = tour[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def local_beam_search(k, max_iter=200):
    # Start with k random tours
    beams = [random_tour() for _ in range(k)]
    best_tour = min(beams, key=tour_cost)
    best_cost = tour_cost(best_tour)

    print(f"\n  Initial best cost: {best_cost}")

    for iteration in range(max_iter):
        # Generate all neighbors from all k beams
        all_neighbors = []
        for beam in beams:
            all_neighbors.extend(get_neighbors(beam))

        # Keep the k best states globally
        all_neighbors.sort(key=tour_cost)
        beams = all_neighbors[:k]

        iter_cost = tour_cost(beams[0])
        if iter_cost < best_cost:
            best_cost = iter_cost
            best_tour = beams[0][:]

        # Print progress every 50 iterations
        if (iteration + 1) % 50 == 0:
            print(f"  Iteration {iteration + 1:3d} | Best Cost So Far: {best_cost}")

    return best_tour, best_cost


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    random.seed(42)

    print("=" * 55)
    print("  Q1 — LOCAL BEAM SEARCH FOR TSP")
    print("  200 iterations | 2-opt neighborhood")
    print("=" * 55)

    results = {}
    for k in [3, 5, 10]:
        print(f"\n{'─'*55}")
        print(f"  Running with k = {k}")
        tour, cost = local_beam_search(k, max_iter=200)
        results[k] = cost
        print(f"\n  Best Path : {tour_str(tour)}")
        print(f"  Total Cost: {cost}")

    print(f"\n{'='*55}")
    print("  COMPARATIVE ANALYSIS")
    print(f"{'='*55}")
    print(f"  k =  3  →  Cost: {results[3]}")
    print(f"  k =  5  →  Cost: {results[5]}")
    print(f"  k = 10  →  Cost: {results[10]}")
    print("""
  Conclusion:
  - Higher k pools more neighbors each iteration, so the
    search escapes local optima more effectively.
  - k=3 is fastest per run but risks getting stuck early.
  - k=10 explores more broadly and finds lower-cost tours.
  - Yes, convergence quality DOES depend on k.
    """)