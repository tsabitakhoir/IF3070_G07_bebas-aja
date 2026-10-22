from SA import SA
import random
import matplotlib.pyplot as plt
from visualisasi import draw_state, draw_trend

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

rng = random.Random(3)
hasil = SA(state, problem, 100, 0.95, 1000, rng)

print("State awal run ", 1, ": ", hasil[0])
print()
print("State akhir run ", 1, ": ", hasil[1])
print()
print("Objective function run ", 1, ": ", hasil[2])
print()
print("Sejarah objective function run ", 1, ": ", hasil[3])
print()
print("Durasi pencarian run ", 1, ": ", hasil[4])
print()
print("Sejarah math.exp(delta/temperature) run ", 1, ": ", hasil[5])

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
draw_state(axes[0, 0], hasil[0], problem, "State Awal")
draw_state(axes[0, 1], hasil[1], problem, "State Akhir")
draw_trend(axes[1, 0], hasil[3], "Objective per iterasi", "Objective")
draw_trend(axes[1, 1], hasil[5], "Probabilitas per iterasi", "e^(delta/T)")

plt.tight_layout()
plt.show()