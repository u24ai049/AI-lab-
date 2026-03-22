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

# ── Helpers ──────────────────────────────────────────────────────────────────
def tour_cost(tour):
    return sum(DIST[tour[i]][tour[(i + 1) % N]] for i in range(N))

def tour_str(tour):
    return " -> ".join(CITIES[i] for i in tour) + f" -> {CITIES[tour[0]]}"

def random_tour():
    t = list(range(N))
    random.shuffle(t)
    return t

def get_neighbors(tour):
    """All 2-opt swap neighbors."""
    neighbors = []
    for i in range(1, N - 1):
        for j in range(i + 1, N):
            neighbor = tour[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors



# ════════════════════════════════════════════════════════════════════════════
# Q2 — GENETIC ALGORITHM
# ════════════════════════════════════════════════════════════════════════════
def order_crossover(p1, p2, num_points=1):
    """Order Crossover (OX) with 1 or 2 crossover points."""
    child = [-1] * N

    if num_points == 1:
        cut = random.randint(1, N - 2)
        child[:cut] = p1[:cut]
    else:
        c1, c2 = sorted(random.sample(range(1, N - 1), 2))
        child[c1:c2 + 1] = p1[c1:c2 + 1]

    # Fill remaining positions with p2's order
    fill = [gene for gene in p2 if gene not in child]
    idx = 0
    for i in range(N):
        if child[i] == -1:
            child[i] = fill[idx]
            idx += 1
    return child

def mutate(tour, rate=0.1):
    t = tour[:]
    if random.random() < rate:
        i, j = random.sample(range(N), 2)
        t[i], t[j] = t[j], t[i]
    return t

def genetic_algorithm(crossover_points, pop_size=50, generations=200):
    population = [random_tour() for _ in range(pop_size)]
    population.sort(key=tour_cost)
    best_tour = population[0][:]
    best_cost = tour_cost(best_tour)
    all_paths = []  # stores (generation, rank, tour, cost)

    # Log initial population top-k
    for ri, ind in enumerate(population):
        all_paths.append((0, ri + 1, ind[:], tour_cost(ind)))

    for gen in range(1, generations + 1):
        new_pop = population[:5]  # Elitism: keep top 5

        while len(new_pop) < pop_size:
            # Always mate the two fittest individuals (rank 1 and rank 2)
            p1 = population[0]
            p2 = population[1]
            child = mutate(order_crossover(p1, p2, crossover_points))
            new_pop.append(child)

        population = sorted(new_pop, key=tour_cost)
        gen_cost = tour_cost(population[0])
        if gen_cost < best_cost:
            best_cost = gen_cost
            best_tour = population[0][:]

        # Log every 25 generations to keep output manageable
        if gen % 25 == 0 or gen == generations:
            for ri, ind in enumerate(population):
                all_paths.append((gen, ri + 1, ind[:], tour_cost(ind)))

    return best_tour, best_cost, all_paths


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    random.seed(42)


    # ── Q2: Genetic Algorithm ────────────────────────────────────────────────
    print("=" * 60)
    print("Q2 — GENETIC ALGORITHM (pop=50, 200 generations, elitism=5)")
    print("=" * 60)

    ga_results = {}
    for pts in [1, 2]:
        tour, cost, all_paths = genetic_algorithm(pts, pop_size=50, generations=200)
        ga_results[pts] = cost
        print(f"\n  Crossover Points = {pts}")
        print(f"  {'Gen':<6} {'Rank':<6} {'Cost':<6}  Path")
        print(f"  {'-'*4:<6} {'-'*4:<6} {'-'*4:<6}  {'-'*40}")
        for (gen, rank, t, c) in all_paths:
            print(f"  {gen:<6} {rank:<6} {c:<6}  {tour_str(t)}")
        print(f"\n  >>> Best Path : {tour_str(tour)}")
        print(f"  >>> Total Cost: {cost}")

    print("\n  --- Comparative Analysis ---")
    print(f"  1-point crossover → Cost: {ga_results[1]}")
    print(f"  2-point crossover → Cost: {ga_results[2]}")
    print("""
  Conclusion:
  2-point crossover preserves more contiguous subtours from both
  parents, producing more diverse offspring. 1-point crossover
  keeps a larger intact prefix from one parent, which can help or
  hurt depending on population structure. In practice, 2-point OX
  often converges to better solutions for TSP due to higher diversity.
    """)