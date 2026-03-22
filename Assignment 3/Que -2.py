import random

rule_table = {
    ("Inbound", "Present"): {"Gate_Arm": "Down", "Siren": "On",  "Signal_to_Train": "Red"},
    ("Inbound", "Absent"):  {"Gate_Arm": "Down", "Siren": "Off", "Signal_to_Train": "Green"},
    ("Outbound","Present"): {"Gate_Arm": "Up",   "Siren": "Off", "Signal_to_Train": "Green"},
    ("Outbound","Absent"):  {"Gate_Arm": "Up",   "Siren": "Off", "Signal_to_Train": "Green"}
}

def what_to_do(sensors, obstacles):
    return rule_table[(sensors, obstacles)]

for _ in range(1):
    sensors = random.choice(["Inbound","Outbound"])
    obstacles = random.choice(["Present","Absent"])
    manual_override = random.choice(["Active","Neutral"])

    result = what_to_do(sensors, obstacles)

    print(f"Sensors: {sensors}, Obstacles: {obstacles}, Manual Override: {manual_override}")
    print(f"Action: {result}")
    print("-"*80)
