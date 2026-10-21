import random
from neighbors import all_neighbors, random_neighbor
from core import is_valid

problem = {
    "ship": {"width": 4, "length": 4, "max_capacity": 10},
    "vehicles": [
        {"id": "A", "width": 2, "length": 1, "fee": 10, "weight": 3, "eta": 1},
        {"id": "B", "width": 2, "length": 1, "fee": 20, "weight": 4, "eta": 1}
    ],
}

state = [
    {"location": 0, "x": 0, "y": 0, "orientation": "H"},
    {"location": -1, "x": 0, "y": 0, "orientation": "H"},
]

rng = random.Random(0)

neighbors = all_neighbors(state, problem)
print(len(neighbors))
print(all(is_valid(n, problem) for n in neighbors))
print(random_neighbor(state, problem, rng))