import sys
sys.stdout.reconfigure(encoding='utf-8')

class Symbol:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

def NOT(p): return not p
def AND(p, q): return p and q
def OR(p, q): return p or q
def IMPLIES(p, q): return (not p) or q
def BICONDITIONAL(p, q): return p == q

def all_combinations(n):
    if n == 0:
        return [()]
    rest = all_combinations(n - 1)
    return [(False,) + r for r in rest] + [(True,) + r for r in rest]

def print_truth_table(expr_func, variables, title):
    print("\n" + "_"*60)
    print(f"Truth table for: {title}")
    print("_"*60)
    headers = [v.name for v in variables] + ["Result"]
    print("\t".join(headers))
    for values in all_combinations(len(variables)):
        env = dict(zip([v.name for v in variables], values))
        result = expr_func(env)
        row = list(values) + [result]
        print("\t".join(['T' if x else 'F' for x in row]))

P = Symbol('P')
Q = Symbol('Q')
R = Symbol('R')

# 1. ~P -> Q
def expr1(e): return IMPLIES(NOT(e['P']), e['Q'])

# 2. ~P ∧ ~Q
def expr2(e): return AND(NOT(e['P']), NOT(e['Q']))

# 3. ~P ∨ ~Q
def expr3(e): return OR(NOT(e['P']), NOT(e['Q']))

# 4. ~P -> ~Q
def expr4(e): return IMPLIES(NOT(e['P']), NOT(e['Q']))

# 5. ~P <-> ~Q
def expr5(e): return BICONDITIONAL(NOT(e['P']), NOT(e['Q']))

# 6. (P ∨ Q) ∧ (~P -> Q)
def expr6(e): return AND(OR(e['P'], e['Q']), IMPLIES(NOT(e['P']), e['Q']))

# 7. ((P ∨ Q) -> R)
def expr7(e): return IMPLIES(OR(e['P'], e['Q']), e['R'])

# 8. ((P ∨ Q) -> R) <-> ((~P ∧ ~Q) -> ~R)
def expr8(e):
    left = IMPLIES(OR(e['P'], e['Q']), e['R'])
    right = IMPLIES(AND(NOT(e['P']), NOT(e['Q'])), NOT(e['R']))
    return BICONDITIONAL(left, right)

# 9. ((P -> Q) ∧ (Q -> R)) -> (P -> R)
def expr9(e):
    left = AND(IMPLIES(e['P'], e['Q']), IMPLIES(e['Q'], e['R']))
    right = IMPLIES(e['P'], e['R'])
    return IMPLIES(left, right)

# 10. ((P -> (Q ∨ R)) -> (~P ∧ ~Q ∧ ~R))
def expr10(e):
    left = IMPLIES(e['P'], OR(e['Q'], e['R']))
    right = AND(NOT(e['P']), AND(NOT(e['Q']), NOT(e['R'])))
    return IMPLIES(left, right)

print_truth_table(expr1, [P, Q], "~P -> Q")
print_truth_table(expr2, [P, Q], "~P ∧ ~Q")
print_truth_table(expr3, [P, Q], "~P ∨ ~Q")
print_truth_table(expr4, [P, Q], "~P -> ~Q")
print_truth_table(expr5, [P, Q], "~P <-> ~Q")
print_truth_table(expr6, [P, Q], "(P ∨ Q) ∧ (~P -> Q)")
print_truth_table(expr7, [P, Q, R], "(P ∨ Q) -> R")
print_truth_table(expr8, [P, Q, R], "((P ∨ Q) -> R) <-> ((~P ∧ ~Q) -> ~R)")
print_truth_table(expr9, [P, Q, R], "((P -> Q) ∧ (Q -> R)) -> (P -> R)")
print_truth_table(expr10, [P, Q, R], "(P -> (Q ∨ R)) -> (~P ∧ ~Q ∧ ~R)")