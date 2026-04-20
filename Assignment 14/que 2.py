# Backward Chaining with explicit AND + OR support

def backward_chaining(rules, facts, goal, visited=None, level=0):
    if visited is None:
        visited = set()

    indent = "  " * level
    print(f"{indent}Trying to prove: {goal}")

    # If goal is already a fact
    if goal in facts:
        print(f"{indent} {goal} is a known fact")
        return True

    # Avoid infinite loops
    if goal in visited:
        print(f"{indent} Already visited {goal}, skipping")
        return False

    visited.add(goal)

    # Try all rules that conclude the goal
    for premise, conclusion, rule_type in rules:
        if conclusion == goal:
            print(f"{indent}Checking {rule_type} rule: {premise} -> {conclusion}")

            if rule_type == "AND":
                # All subgoals must be true
                if all(backward_chaining(rules, facts, p, visited, level+1) for p in premise):
                    print(f"{indent} AND rule satisfied for {goal}")
                    return True

            elif rule_type == "OR":
                # Any one subgoal must be true
                if any(backward_chaining(rules, facts, p, visited, level+1) for p in premise):
                    print(f"{indent} OR rule satisfied for {goal}")
                    return True

    print(f"{indent} Cannot prove {goal}")
    return False


# ---------------- EXAMPLE ----------------

rules = [
    (['A', 'B'], 'L', 'AND'),   # A ∧ B → L
    (['L', 'M'], 'P', 'AND'),   # L ∧ M → P
    (['X', 'Y'], 'Z', 'OR'),    # X ∨ Y → Z
    (['P'], 'Q', 'AND')         # P → Q
]

facts = ['A', 'B', 'M', 'X']
goal = 'Q'

print("\n========== RUN ==========")
result = backward_chaining(rules, facts, goal)
print("\nResult:", result)