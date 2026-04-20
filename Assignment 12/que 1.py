variables = ["P1","P2","P3","P4","P5","P6"]

domains = {v: {"R1","R2","R3"} for v in variables}

neighbors = {
    "P1": ["P2","P3","P6"],
    "P2": ["P1","P3","P4"],
    "P3": ["P1","P2","P5"],
    "P4": ["P2","P6"],
    "P5": ["P3","P6"],
    "P6": ["P1","P4","P5"]
}

def constraint(x, y):
    return x != y

def revise(domains, Xi, Xj):
    revised = False
    to_remove = set()
    for x in domains[Xi]:
        if not any(constraint(x, y) for y in domains[Xj]):
            to_remove.add(x)
    if to_remove:
        domains[Xi] -= to_remove
        revised = True
    return revised

def ac3(domains, trace=False):
    queue = []
    for Xi in variables:
        for Xj in neighbors[Xi]:
            queue.append((Xi, Xj))
    steps = 0
    while queue:
        Xi, Xj = queue.pop(0)
        if trace and steps < 5:
            print("step " + str(steps+1) + ": checking arc (" + Xi + "," + Xj + ")")
        if revise(domains, Xi, Xj):
            if trace:
                print("domain reduced: " + Xi + " -> " + str(domains[Xi]))
            if not domains[Xi]:
                return False
            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
        steps += 1
    return True

print("= ac-3 without assignment =")
domains_copy = {k: set(v) for k,v in domains.items()}
ac3(domains_copy, trace=True)
print("final domains: " + str(domains_copy))

print("= ac-3 after assigning p1 = r1 =")
domains_copy = {k: set(v) for k,v in domains.items()}
domains_copy["P1"] = {"R1"}
ac3(domains_copy, trace=True)
print("final domains: " + str(domains_copy))