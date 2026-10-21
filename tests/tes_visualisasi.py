import matplotlib.pyplot as plt
from visualisasi import draw_state

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

fig, ax = plt.subplots()
draw_state(ax, state, problem, "State Awal")
plt.show()