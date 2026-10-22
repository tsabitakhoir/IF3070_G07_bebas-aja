import math
import time
from src.core import objective
from src.neighbors import random_neighbor

def count_stuck(history, treshold):
    countt = 0
    stuckk = 0
    length = 1

    for k in range (1, len(history)):
        if history[k] == history[k - 1]:
            length +=1

        else:
            if length >= treshold:
                countt += 1
                stuckk += length
            length = 1

    if length >= treshold:
        countt += 1
        stuckk += length

    return countt, stuckk

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

        if temperature <= 0.5:
            break
    end = time.perf_counter()
    durasi = end - start
    countt, stuckk = count_stuck(history_fee, max(5, 0.05 * len(history_fee)))
    return state, curr_state, curr_fee, history_fee, durasi, history_probability, countt, stuckk