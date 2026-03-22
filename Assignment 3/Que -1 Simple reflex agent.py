import random

Rooms = ["A", "B", "C"]

# Environment
halat = {
    "A": random.choice(["Clean","Dirty"]),
    "B": random.choice(["Clean","Dirty"]),
    "C": random.choice(["Clean","Dirty"])
}
rule_table={
    ("A", "Dirty"): ["Suck","Clean"],
    ("A", "Clean"): ["Move_Right","Stay"],
    ("B", "Dirty"): ["Suck","Clean"],
    ("B", "Clean"): ["Random_move","Stay"],
    ("C", "Dirty"): ["Suck","Clean"],
    ("C", "Clean"): ["Move_Left","Stay"]
}
action_table={
    ("A","Move_Right"): "B",
    ("B","Move_Right"): "C",
    ("C","Move_Left"): "B",
    ("B","Move_Left"):"A",
    ("B","Suck"):"B",
    ("A","Suck"):"A",
    ("C","Suck"):"C"
}
start_location=random.choice(Rooms)
print("Initial Rooms:", halat)
current_location=start_location
for i in range(10):

    current_status = halat[current_location]
    action = rule_table[(current_location, current_status)]

    if action[0] == "Suck":
        halat[current_location] = action[1]
        print(f"{current_location} and {current_status} and action taken is {action}")

    if action[0] == "Random_move":
        move = random.choice(["Move_Left","Move_Right"])
        current_location = action_table[(current_location, move)]
        new_status = halat[current_location]
        print(f"{current_location} and {new_status} and action taken is {(move,action[1])}")
        continue

    current_location = action_table[(current_location, action[0])]
    new_status = halat[current_location]
    print(f"{current_location} and {new_status} and action taken is {action}")


