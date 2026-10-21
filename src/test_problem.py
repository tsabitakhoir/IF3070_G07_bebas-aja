import random
from neighbors import all_neighbors, random_neighbor
from core import is_valid
from problem import load_problem, random_state, save_output
import json
import os
import random

dummy_json_path = "test_tc_dummy.json"
dummy_data = {
    "ship": {"width": 5, "length": 5, "max_capacity": 100},
    "vehicles": [
        {"id": "1", "width": 2, "length": 3, "fee": 50, "weight": 10, "eta": 2},
        {"id": "2", "width": 2, "length": 2, "fee": 30, "weight": 5, "eta": 1},
        {"id": "3", "width": 4, "length": 4, "fee": 100, "weight": 90, "eta": 1}
    ]
}

with open(dummy_json_path, "w", encoding="utf-8") as f:
    json.dump(dummy_data, f)


print("test load problem")
try:
    problem = load_problem(dummy_json_path)
    print("Problem berhasil dimuat.")
    print("Ukuran Kapal:", problem["ship"])
    print("Total Kendaraan:", len(problem["vehicles"]))
except Exception as e:
    print("failed", e)


print("\n test random state")
rng = random.Random(42) 
state_awal = random_state(problem, rng)

print("State random:")
for i, s in enumerate(state_awal):
    print(f"Kendaraan {i} ({problem['vehicles'][i]['id']}): {s}")

validity = is_valid(state_awal, problem)
print(f"state valid? {validity}")


print("\n test save output")
dummy_result = {
    "algorithm": "test",
    "config": {"max_iter": 100},
    "run": 1,
    "seed": 42,
    "initial_state": state_awal,
    "final_state": state_awal,
    "final_value": 80,
    "duration_s": 0.05,
    "iterations": 10,
    "evaluations": 10,
    "history": [10, 20, 20, 50, 80, 80, 80],
    "extra": {}
}

try:
    path_json, path_png = save_output(dummy_result, "output")
    print(f"berasil, json ada di {path_json}")
    print(f"berasil, visualissi ada di{path_png}")
except Exception as e:
    print("failed", e)
