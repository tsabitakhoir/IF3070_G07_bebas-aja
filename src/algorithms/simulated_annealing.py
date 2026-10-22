import math
import time
from core import objective
from neighbors import all_neighbors

def SA(state, problem, temperature, alpha, iterations, rng):
    curr_state = state
    curr_fee = objective(curr_state, problem)
    best_state = curr_state
    best_fee = curr_fee
    history_fee = []
    history_probability = []
    stuck = 0

    start = time.perf_counter()
    for x in range(iterations):
        tetangga = all_neighbors(curr_state, problem)
        if len(tetangga) == 0:
            break

        nilai = []
        for t in tetangga:
            nilai.append(objective(t, problem))
        if max(nilai) <= curr_fee:
            stuck += 1

        pilih = rng.randrange(len(tetangga))
        neighbor = tetangga[pilih]
        neighbor_fee = nilai[pilih]

        delta = neighbor_fee - curr_fee
        if delta >= 0:
            probability = 1
            curr_state = neighbor
            curr_fee = neighbor_fee
            if neighbor_fee > best_fee:
                best_state = neighbor
                best_fee = neighbor_fee

        else:
            probability = math.exp(delta/temperature)
            if rng.random() < probability:
                curr_state = neighbor
                curr_fee = neighbor_fee

        history_probability.append(probability)
        history_fee.append(curr_fee)
        temperature *= alpha

        if temperature <= 1e-8:
            break
    end = time.perf_counter()
    durasi = end - start
    return state, best_state, best_fee, history_fee, durasi, history_probability, stuck