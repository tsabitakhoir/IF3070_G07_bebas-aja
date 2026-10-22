# default ngerun pake tes case small
# kalo mau ngerun medimum/large:
# python src/runner.py --testcase input/tc_medium.json
# python src/runner.py --testcase input/tc_large.json

import matplotlib
matplotlib.use("Agg")
import sys
import argparse
import copy
import os
import random
import statistics
from pathlib import Path
from problem import load_problem, random_state, save_output, config_to_text
from algorithms.genetic_algorithm import genetic_algorithm
from algorithms.simulated_annealing import SA
from algorithms.hill_climbing import hill_climbing_sideways
from visualisasi import draw_result, draw_trend

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

ROOT = Path(__file__).resolve().parent.parent
SEEDS = [1, 2, 3]

def run_sa(problem, rng, temperature=100, cooling_rate=0.95, max_iterations=1000):
    state = random_state(problem, rng)
    initial_state = copy.deepcopy(state)
    hasil = SA(state, problem, temperature, cooling_rate, max_iterations, rng)
    _, final_state, final_value, history, duration, prob_history = hasil

    return {
        "algorithm": "Simulated Annealing",
        "config": {
            "temperature": temperature,
            "cooling_rate": cooling_rate,
            "max_iterations": max_iterations,
        },
        "initial_state": initial_state,
        "final_state": final_state,
        "final_value": final_value,
        "history": history,
        "duration_s": duration,
        "iterations": len(history),
        "evaluations": len(history),
        "extra": {"accept_prob_history": prob_history},
    }

def run_hc(problem, rng, max_sideways=100):
    hasil = hill_climbing_sideways(problem, rng, max_sideways)
    mulai, akhir, nilai_akhir, history, durasi, iterasi, evaluasi, _, total_sideways, alasan = hasil

    return {
        "algorithm": "Hill-Climbing Sideways",
        "config": {"max_sideways": max_sideways},
        "initial_state": mulai,
        "final_state": akhir,
        "final_value": nilai_akhir,
        "history": history,
        "duration_s": durasi,
        "iterations": iterasi,
        "evaluations": evaluasi,
        "extra": {
            "total_sideways": total_sideways,
            "alasan": alasan,
        },
    }

EXPERIMENTS = {
    "GA_iteration": {
        "fn": genetic_algorithm,
        "configs": [{"population_size": 50, "max_generations": g} for g in (50, 100, 200)],
    },
    "GA_population": {
        "fn": genetic_algorithm,
        "configs": [{"population_size": p, "max_generations": 100} for p in (20, 50, 100)],
    },
    "SA": {
        "fn": run_sa,
        "configs": [{"temperature": 100, "cooling_rate": 0.95, "max_iterations": 1000}],
    },
    "HC": {
        "fn": run_hc,
        "configs": [{"max_sideways": s} for s in (0, 100, 200)],
    }
}

def run_experiments(testcase_path, names, out_root, seeds, make_figures):
    problem = load_problem(str(testcase_path))
    out_dir = os.path.join(out_root, Path(testcase_path).stem)
    os.makedirs(out_dir, exist_ok=True)

    rows = []
    done = set()
    for exp_name in names:
        exp = EXPERIMENTS[exp_name]
        for config in exp["configs"]:
            for run_number, seed in enumerate(seeds, start=1):
                key = (exp["fn"].__name__, tuple(sorted(config.items())), run_number)
                if key in done:
                    continue
                done.add(key)

                rng = random.Random(seed)
                result = exp["fn"](problem, rng, **config)
                result["run"] = run_number
                result["seed"] = seed

                save_output(result, out_dir)
                config_text = config_to_text(result.get("config", {}))
                if make_figures:
                    base = f"{result['algorithm']}_{config_text}_run{run_number}"
                    draw_result(result, problem, os.path.join(out_dir, base + "_ringkasan.png"))

                rows.append({
                    "experiment": exp_name,
                    "algorithm": result["algorithm"],
                    "config": config_text,
                    "run": run_number,
                    "seed": seed,
                    "final_value": result["final_value"],
                    "duration_s": round(result["duration_s"], 4),
                    "iterations": result.get("iterations"),
                    "evaluations": result.get("evaluations"),
                })
                print(f"[{exp_name}] {config_text} run{run_number} (seed {seed}): "
                      f"nilai={result['final_value']}, {result['duration_s']:.2f} detik")

    summarize(rows, out_dir)
    print(f"\nHasil ada di {out_dir}")

def summarize(rows, out_dir):
    "Rata-rata, terbaik, terburuk, dan simpangan baku per konfigurasi."
    groups = {}
    for r in rows:
        groups.setdefault((r["algorithm"], r["config"]), []).append(r)

    agg_rows = []
    for (algo, cfg), items in groups.items():
        values = [r["final_value"] for r in items]
        durations = [r["duration_s"] for r in items]
        agg_rows.append({
            "algorithm": algo,
            "config": cfg,
            "runs": len(items),
            "best": max(values),
            "worst": min(values),
            "mean": round(statistics.mean(values), 2),
            "stdev": round(statistics.stdev(values), 2) if len(values) > 1 else 0.0,
            "mean_duration_s": round(statistics.mean(durations), 3),
        })

def main():
    parser = argparse.ArgumentParser(description="Runner eksperimen local search")
    parser.add_argument("--testcase", default=str(ROOT / "input" / "tc_small.json"))
    parser.add_argument("--only", nargs="+", choices=list(EXPERIMENTS), default=list(EXPERIMENTS))
    parser.add_argument("--out", default=str(ROOT / "output"))
    parser.add_argument("--seeds", nargs="+", type=int, default=SEEDS)
    parser.add_argument("--no-fig", action="store_true", help="lewati gambar ringkasan 2x2")
    args = parser.parse_args()

    run_experiments(args.testcase, args.only, args.out, args.seeds, not args.no_fig)

if __name__ == "__main__":
    main()