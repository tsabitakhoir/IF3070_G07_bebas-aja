from importlib.resources import path
import json
from core import is_valid
import os
import matplotlib
import matplotlib.pyplot as plt

import problem
matplotlib.use("Agg")

# helper untuk validasi angka
def check_int_positive(value, field_name):
    if isinstance(value, bool) or not (isinstance(value, int) and value > 0):
        raise ValueError(f"{field_name} harus bulat positif")


# baca file input dan ubah ke bentuk dictionaru
def load_problem(path):
    with open(path, "r", encoding="utf-8") as file:
        problem = json.load(file)

    # validasi di json harus ada ship sama vehicles
    if "ship" not in problem or "vehicles" not in problem:
        raise ValueError("file harus memiliki ship dan vehicles")

    # validasi w, l, max kapasitas kapal harus int positif
    ship = problem["ship"]
    check_int_positive(ship.get("width"), "lebar kapal")
    check_int_positive(ship.get("length"), "panjang kapal")
    check_int_positive(ship.get("max_capacity"), "kapasitas maksimal kapal")

    # validasi komponen2 di kendaraan
    seen_id = set()
    for vehicle in problem["vehicles"]:
        vehicle_id = vehicle.get("id")
    if not isinstance(vehicle_id, str):
        raise ValueError("ID kendaraan harus string")
    if vehicle_id in seen_id:
        raise ValueError(f"ID {vehicle_id} duplikat")
    seen_id.add(vehicle_id)

    check_int_positive(vehicle.get("width"), f"lebar kendaraan {vehicle_id}")
    check_int_positive(vehicle.get("length"), f"panjang kendaraan {vehicle_id}")
    check_int_positive(vehicle.get("fee"), f"fee kendaraan {vehicle_id}")
    check_int_positive(vehicle.get("weight"), f"berat kendaraan {vehicle_id}")
    check_int_positive(vehicle.get("eta"), f"eta kendaraan {vehicle_id}")

    return problem


# ngembaliin state valid kendaraan
def random_state(problem, rng, max_attempts=10):
    vehicles = problem["vehicles"]
    ship = problem["ship"]
    total = len(vehicles)

    state = []
    for _ in range (total):
        state.append({"location": -1, "x": 0, "y": 0, "orientation": "H"})

    #acak urutan kendaraan yg mau dimasukin
    order = list(range(total))
    rng.shuffle(order)

    #masukin kendaraan ke kapal
    for index in order:
        v = vehicles[index]

        # loop max attempts buat orientasi
        for _ in range (max_attempts):
            orientation = rng.choice(["H", "V"])

            if orientation == "H":
                w2 = v["width"]
                l2 = v["length"]
            else:
                w2 = v["length"]
                l2 = v["width"]

        limit_x = ship["width"] - w2
        limit_y = ship["length"] - l2

        if limit_x < 0 or limit_y < 0:
            continue

        state[index] = {"location": 0, "x": rng.randint(0, limit_x), "y": rng.randint(0, limit_y), "orientation": orientation}

        if is_valid(state, problem) == True:
            break
        else:
            state[index] = {"location": -1, "x": 0, "y": 0, "orientation": "H"}
    return state

# fungsi helper buat penamaan file
def config_to_text(config):
    if not config:
        return "default"
    return "_".join(f"{key}{value}" for key, value in sorted(config.items()))

#ngesave ke output dan bikin visualisasi
def save_output(result, output_directory="output"):
    name = f"{result ['algorithm']}_{config_to_text(result.get('config', {}))}_run{result['run']}"
    json_path = os.path.join(output_directory, name + ".json")
    png_path = os.path.join(output_directory, name + ".png")

    with open(json_path, 'w', encoding="utf-8") as file:
        json.dump(result, file, indent = 2, ensure_ascii = False)

    fig, ax = plt.subplots(figsize=(7, 5))

    if "history" in result:
        ax.plot(range(len(result["history"])), result["history"], label = "objective")
    else:
        ax.plot(range(len(result["history_max"])), result["history_max"], label = "max")
        ax.plot(range(len(result["history_mean"])), result["history_mean"], label = "mean")

    ax.set_title(f"{result['algorithm']} ({config_to_text(result.get('config', {}))}), run {result['run']}")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Objective Value")
    ax.legend()

    fig.tight_layout()
    fig.savefig(png_path, dpi=150)
    plt.close(fig)

    return json_path, png_path