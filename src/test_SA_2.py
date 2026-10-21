from SA import SA
import random

problem = {
    "ship": {"width": 6, "length": 3, "max_capacity": 22},
    "vehicles": [
        {"id": "A", "width": 2, "length": 1, "fee": 10, "weight": 3, "eta": 1},
        {"id": "B", "width": 2, "length": 1, "fee": 20, "weight": 5, "eta": 1},
        {"id": "C", "width": 1, "length": 4, "fee": 30, "weight": 6, "eta": 3},
        {"id": "D", "width": 2, "length": 2, "fee": 25, "weight": 5, "eta": 2},
        {"id": "E", "width": 3, "length": 2, "fee": 40, "weight": 8, "eta": 4},
    ],
}

state = [
    {"location": 0, "x": 0, "y": 0, "orientation": "H"},
    {"location": -1, "x": 0, "y": 0, "orientation": "H"},
    {"location": 0, "x": 0, "y": 2, "orientation": "V"},
    {"location": -1, "x": 0, "y": 0, "orientation": "H"},
    {"location": -1, "x": 0, "y": 0, "orientation": "H"},
]

for run, seed in enumerate([0, 1, 2], start = 1):
    rng = random.Random(seed)
    hasil = SA(state, problem, 100, 0.95, 1000, rng)

    print("State awal run ", run, ": ", hasil[0])
    print()
    print("State akhir run ", run, ": ", hasil[1])
    print()
    print("Objective function run ", run, ": ", hasil[2])
    print()
    print("Sejarah objective function run ", run, ": ", hasil[3])
    print()
    print("Durasi pencarian run ", run, ": ", hasil[4])
    print()
    print("Sejarah math.exp(delta/temperature) run ", run, ": ", hasil[5])