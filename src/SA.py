import math
import time
from core import objective
from neighbors import random_neighbor

def SA(state, problem, temperature, alpha, iterations, rng):
    curr_state = state
    curr_fee = objective(curr_state, problem)
    best_state = curr_state
    best_fee = curr_fee
    history_fee = []
    history_probability = []

    start = time.perf_counter()
    for x in range(iterations):
        neighbor = random_neighbor(curr_state, problem, rng)
        if neighbor is None:
            break
        neighbor_fee = objective(neighbor, problem)

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
    return state, curr_state, curr_fee, history_fee, durasi, history_probability