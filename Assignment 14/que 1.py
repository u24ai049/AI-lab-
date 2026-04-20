# Forward Chaining with rules

def forward_chaining(rules, facts, goal):
    inferred = set(facts)
    step = 1

    print("\nInitial Facts:", inferred)

    while True:
        new_inferred = False

        for premise, conclusion, rule_type in rules:

            # AND rule
            if rule_type == "AND":
                condition = set(premise).issubset(inferred)

            # OR rule
            elif rule_type == "OR":
                condition = any(p in inferred for p in premise)

            else:
                continue

            # Apply rule if condition satisfied
            if condition and conclusion not in inferred:
                print(f"\nStep {step}: Applying {rule_type} Rule {premise} -> {conclusion}")
                print("Before:", inferred)

                inferred.add(conclusion)
                new_inferred = True

                print("After:", inferred)
                step += 1

                if goal in inferred:
                    print("\nGoal reached:", goal)
                    return True

        if not new_inferred:
            print("\nNo more rules can be applied.")
            print("Final Facts:", inferred)
            return False


# ---------------- EXAMPLE ----------------

rules = [
    (['A', 'B'], 'L', 'AND'),   # A ∧ B → L
    (['L', 'M'], 'P', 'AND'),   # L ∧ M → P
    (['X', 'Y'], 'Z', 'OR'),    # X ∨ Y → Z
    (['P'], 'Q', 'AND')         # P → Q
]

facts = ['A', 'B', 'M', 'X']   # X triggers OR rule
goal = 'Q'

print("\n========== RUN ==========")
result = forward_chaining(rules, facts, goal)
print("\nResult:", result)