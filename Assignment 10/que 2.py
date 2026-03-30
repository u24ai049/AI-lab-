from dataclasses import dataclass

# 🔹 State representation
@dataclass(frozen=True, order=True)
class State:
    loc: str  # 'A' or 'B'
    A: str    # 'C' or 'D'
    B: str    # 'C' or 'D'


# 🔹 Goal test
def is_goal(s):
    return s.A == 'C' and s.B == 'C'


# 🔹 Print state
def state_to_string(s):
    return f"({s.loc},{s.A},{s.B})"


# 🔹 Possible results of SUCK (erratic)
def suck_results(s):
    results = []

    if s.loc == 'A':
        if s.A == 'D':
            # Clean A, maybe clean B
            results.append(State('A', 'C', s.B))
            results.append(State('A', 'C', 'C'))
        else:
            # May become dirty again
            results.append(State('A', 'D', s.B))
            results.append(State('A', 'C', s.B))
    else:  # loc == 'B'
        if s.B == 'D':
            results.append(State('B', s.A, 'C'))
            results.append(State('B', 'C', 'C'))
        else:
            results.append(State('B', s.A, 'D'))
            results.append(State('B', s.A, 'C'))

    return results


# 🔹 Move actions
def move_left(s):
    return State('A', s.A, s.B)


def move_right(s):
    return State('B', s.A, s.B)


# 🔹 AND-OR Search
def and_search(states, path):
    for s in states:
        if not or_search(s, path):
            return False
    return True


def or_search(s, path):
    if is_goal(s):
        print(f"Goal reached at state {state_to_string(s)}")
        return True

    if s in path:
        return False

    path = path.copy()
    path.add(s)

    print(f"Exploring state {state_to_string(s)}")

    # 🔸 Try SUCK
    results = suck_results(s)
    if and_search(results, path):
        print(f"Action: SUCK at {state_to_string(s)}")
        return True

    # 🔸 Try Move Right
    if s.loc == 'A':
        next_state = move_right(s)
        if or_search(next_state, path):
            print(f"Action: MOVE RIGHT from {state_to_string(s)}")
            return True

    # 🔸 Try Move Left
    if s.loc == 'B':
        next_state = move_left(s)
        if or_search(next_state, path):
            print(f"Action: MOVE LEFT from {state_to_string(s)}")
            return True

    return False


def main():
    start = State('A', 'D', 'D')

    print("Starting AND-OR Search...\n")

    if not or_search(start, set()):
        print("No solution found.")


if __name__ == "__main__":
    main()