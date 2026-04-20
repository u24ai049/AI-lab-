# Resolution Method with Detailed Tracing (Improved Version)

def is_complementary(a, b):
    """Check if two literals are complementary"""
    return a == '¬' + b or b == '¬' + a


def resolve(ci, cj):
    """Generate resolvents between two clauses"""
    resolvents = []

    for di in ci:
        for dj in cj:
            if is_complementary(di, dj):
                new_clause = (ci | cj) - {di, dj}
                resolvents.append(new_clause)

    return resolvents


def print_clauses(clauses):
    for c in clauses:
        print(c)


def resolution(kb, query):
    # Convert KB into set format
    clauses = [set(c) for c in kb]

    # Add negated query
    neg_query = '¬' + query
    clauses.append({neg_query})

    print("\nInitial Clauses:")
    print_clauses(clauses)

    step = 1

    while True:
        new_clauses = []

        print(f"\n--- Resolution Step {step} ---")

        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):

                ci, cj = clauses[i], clauses[j]
                resolvents = resolve(ci, cj)

                for r in resolvents:
                    print(f"Resolving {ci} and {cj} → {r}")

                    # If empty clause found
                    if len(r) == 0:
                        print("\nEmpty clause found → CONTRADICTION")
                        print("Query is TRUE")
                        return True

                    # Add only new clauses
                    if r not in clauses and r not in new_clauses:
                        new_clauses.append(r)

        # If nothing new is generated
        if not new_clauses:
            print("\nNo new clauses generated")
            print("Query is FALSE (cannot be proved)")
            return False

        # Add new clauses
        for clause in new_clauses:
            print("Adding new clause:", clause)
            clauses.append(clause)

        step += 1


# -----------------------------
# CASE (a)
# -----------------------------
kb_a = [
    ['P', 'Q'],
    ['¬P', 'R'],
    ['¬Q', 'S'],
    ['¬R', 'S']
]

print("\n========== CASE (a) ==========")
result_a = resolution(kb_a, 'S')
print("Final Result (a):", result_a)


# -----------------------------
# CASE (b)
# -----------------------------
kb_b = [
    ['¬P', 'Q'],
    ['¬Q', 'R'],
    ['¬S', '¬R'],
    ['P']
]

print("\n========== CASE (b) ==========")
result_b = resolution(kb_b, 'S')
print("Final Result (b):", result_b)    