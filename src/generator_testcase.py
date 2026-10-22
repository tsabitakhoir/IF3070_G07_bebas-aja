import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "input"

#atur atur
PRESETS = {
    "small": {
        "ship_w": 5, "ship_l": 5, "n": 6,
        "size_range": (1, 3), "fee_per_cell": (2, 8), "weight_per_cell": (1, 3),
        "eta_range": (1, 7), "capacity_ratio": 0.6, "seed": 11,
    },
    "medium": {
        "ship_w": 8, "ship_l": 12, "n": 12,
        "size_range": (1, 5), "fee_per_cell": (2, 8), "weight_per_cell": (1, 3),
        "eta_range": (1, 7), "capacity_ratio": 0.6, "seed": 22,
    },
    "large": {
        "ship_w": 14, "ship_l": 20, "n": 40,
        "size_range": (1, 6), "fee_per_cell": (2, 8), "weight_per_cell": (1, 3),
        "eta_range": (1, 7), "capacity_ratio": 0.5, "seed": 33,
    },
}

def build_vehicles(rng, n, size_range, fee_per_cell, weight_per_cell, eta_range):
    vehicles = []
    for i in range(1, n + 1):
        lebar = rng.randint(*size_range)
        panjang = rng.randint(*size_range)
        area = lebar * panjang
        vehicles.append({
            "id": f"V{i:03d}",
            "width": lebar,
            "length": panjang,
            "fee": max(1, round(area * rng.uniform(*fee_per_cell))),
            "weight": max(1, round(area * rng.uniform(*weight_per_cell))),
            "eta": rng.randint(*eta_range),
        })
    return vehicles

def check_quality(problem):
    ship = problem["ship"]
    vehicles = problem["vehicles"]
    issues = []

    total_area = sum(v["width"] * v["length"] for v in vehicles)
    total_weight = sum(v["weight"] for v in vehicles)
    if total_area <= ship["width"] * ship["length"]:
        issues.append("total luas kendaraan tidak melebihi luas geladak")
    if total_weight <= ship["max_capacity"]:
        issues.append("total berat kendaraan tidak melebihi kapasitas")

    for v in vehicles:
        muat_h = v["width"] <= ship["width"] and v["length"] <= ship["length"]
        muat_v = v["length"] <= ship["width"] and v["width"] <= ship["length"]
        if not (muat_h or muat_v):
            issues.append(f"{v['id']} tidak muat di geladak")
        if v["weight"] > ship["max_capacity"]:
            issues.append(f"{v['id']} lebih berat dari kapasitas kapal")
    return issues

def generate(params, max_tries=200):
    rng = random.Random(params["seed"])
    for _ in range(max_tries):
        vehicles = build_vehicles(
            rng, params["n"], params["size_range"], params["fee_per_cell"],
            params["weight_per_cell"], params["eta_range"],
        )
        total_weight = sum(v["weight"] for v in vehicles)
        problem = {
            "ship": {
                "width": params["ship_w"],
                "length": params["ship_l"],
                "max_capacity": max(1, round(total_weight * params["capacity_ratio"])),
            },
            "vehicles": vehicles,
        }
        if not check_quality(problem):
            return problem
    raise RuntimeError("Tidak berhasil membuat test case yang layak")

def describe(problem):
    ship = problem["ship"]
    vehicles = problem["vehicles"]
    total_luas = sum(v["width"] * v["length"] for v in vehicles)
    total_berat = sum(v["weight"] for v in vehicles)
    luas_geladak = ship["width"] * ship["length"]

    return (f"{len(vehicles)} kendaraan | luas {total_luas}/{luas_geladak}"
            f" | berat {total_berat}/{ship['max_capacity']}")

def validate_with_loader(path):
    sys.path.insert(0, str(ROOT / "src"))
    try:
        from problem import load_problem
    except ImportError:
        print("  (load_problem tidak ditemukan, validasi dilewati)")
        return
    load_problem(str(path))
    print("  lolos load_problem")

def main():
    names = sys.argv[1:] or list(PRESETS)
    for name in names:
        if name not in PRESETS:
            sys.exit(f"Nama tidak dikenal: {name}. Pilihan: {', '.join(PRESETS)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in names:
        problem = generate(PRESETS[name])
        path = OUT_DIR / f"tc_{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(problem, f, indent=2)
        print(f"{path}: {describe(problem)}")
        validate_with_loader(path)

if __name__ == "__main__":
    main()