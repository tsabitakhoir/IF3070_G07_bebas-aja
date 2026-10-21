import copy
import time
from problem import random_state
from core import is_valid, objective

# fungsi inisialisasi, bikin populasi awal as representasi
def create_population(problem, rng, population_size):
    list_of_states = []
    for _ in range(population_size):
            state = random_state(problem, rng)
            list_of_states.append(state)
    list_of_fitness = [objective(state, problem) for state in list_of_states]
    return list_of_states, list_of_fitness

# fungsi selection. pakai selection tournament karena simpel, tidak perlu sorting, sehingga memakan waktu yang singkat
def tournament(list_of_fitness, list_of_states,rng, prohibited = None, tournament_size = 3):
    population_size = len(list_of_states)
    valid_index = [i for i in range(population_size) if prohibited is None or i not in prohibited]
    tournament_index = rng.sample(valid_index, min(tournament_size, len(valid_index)))
    best_index = tournament_index[0]
    best_fitness = list_of_fitness[best_index]
    for i in tournament_index:
         if list_of_fitness[i] > best_fitness:
            best_index = i
            best_fitness = list_of_fitness[i]
    return best_index, list_of_states[best_index], best_fitness

# fungsi crossover (motong 2 parent di crossover point, digabungin jadi 1 child)
def crossover(parent1, parent2, rng):
    crossover_point = rng.randint(1, len(parent1) - 1)
    child = copy.deepcopy(parent1[0:crossover_point]) + copy.deepcopy(parent2[crossover_point:])
    return child

#fungsi mutation. state child diubah berdasarkan kategori state (lokasi, x, y, orientasi)
def mutation(child, problem, rng, mutation_rate=0.1):
    # kalau mutation rate lebih kecil di banding random number, mutasi ga terjadi, langsung return child aja
    if rng.random() > mutation_rate:
        return child

    i = rng.randint(0, len(child) - 1)
    origin_state = child[i].copy()
    vehicle_spec = problem["vehicles"][i]
    ship_width = problem["ship"]["width"]
    ship_length = problem["ship"]["length"]

    # kendaraan di luar kapal cuma bisa mutasi lokasi doang
    if origin_state["location"] == -1:
        category = "location"
    else:
        category = rng.choice(["location", "x", "y", "orientation"])
        
    # mutasi tiap2 kategori dalam state secara random
    if category == "location":
        if origin_state["location"] == 0:
            child[i] = {"location": -1, "x": 0, "y": 0, "orientation" : "H"}
        else:
            orientation = rng.choice(["H", "V"])
            if orientation == "H":
                limit_x = ship_width - vehicle_spec["width"]
                limit_y = ship_length - vehicle_spec["length"]
            else:
                limit_x = ship_width - vehicle_spec["length"]
                limit_y = ship_length - vehicle_spec["width"]
            child[i] = {
                "location": 0,
                "x": rng.randint(0, max(0, limit_x)),
                "y": rng.randint(0, max(0, limit_y)),
                "orientation": orientation
            }
    elif category == "x":
        if child[i]["orientation"] == "H":
            limit_x = ship_width - vehicle_spec["width"]
        else:
            limit_x = ship_width - vehicle_spec["length"]
        child[i]["x"] = rng.randint(0, max(0, limit_x))
    elif category == "y":
        if child[i]["orientation"] == "H":
            limit_y = ship_length - vehicle_spec["length"]
        else:
            limit_y = ship_length - vehicle_spec["width"]
        child[i]["y"] = rng.randint(0, max(0, limit_y))
    elif category == "orientation":
        child[i]["orientation"] = "H" if child[i]["orientation"] == "V" else "V"

    # make sure validasi child, bcs child bisa aja jadi ga bisa dimuat di kapal setelah mutasi
    if not is_valid(child, problem):
        child[i] = origin_state

    return child

# fungsi mating. fungsi buat ngeprodiksi satu anak yang valid
def mating (list_of_states, list_of_fitness, problem, rng, mutation_rate, tournament_size, max_attempts=10):
    for _ in range(max_attempts):
        pi1 = tournament(list_of_fitness, list_of_states, rng, tournament_size=tournament_size)[0]
        pi2 = tournament(list_of_fitness, list_of_states, rng, prohibited=[pi1], tournament_size=tournament_size)[0]
        child = crossover(list_of_states[pi1], list_of_states[pi2], rng)
        mutant = mutation(child, problem, rng, mutation_rate)
        if is_valid(mutant, problem):
            return mutant
    return copy.deepcopy(list_of_states[rng.choice([pi1, pi2])])

#fungsi utama genetic algorithm
def genetic_algorithm(problem, rng, population_size=50, max_generations=100, mutation_rate=0.1, tournament_size=3, max_attempts=10):
    # ibarat taksi nyalain argo yee
    start_time = time.perf_counter()
    evaluations = 0

    # inisialisasi populasi. bikin generasi ke 0
    list_of_states, list_of_fitness = create_population(problem, rng, population_size)
    evaluations += population_size

    # ngecek siapa si yang paling mantep
    best_state, best_fitness = max(zip(list_of_states, list_of_fitness), key=lambda x: x[1])
    initial_state = copy.deepcopy(best_state)
    history_max = []
    history_mean = []

    # proses looping utama
    for generation in range(max_generations):
        new_list_of_states = []
        new_list_of_fitness = []

        # looping buat bikin anak
        for _ in range(population_size):
            child = mating(list_of_states, list_of_fitness, problem, rng, mutation_rate, tournament_size, max_attempts)
            new_list_of_states.append(child)
            new_list_of_fitness.append(objective(child, problem))
            evaluations += 1

        # list dah penuh, populasi lama diganti sama populasi anak2 baru
        list_of_states = new_list_of_states
        list_of_fitness = new_list_of_fitness

        current_best_state, current_best_fitness = max(zip(list_of_states, list_of_fitness), key=lambda x: x[1])
        if current_best_fitness > best_fitness:
            best_state = copy.deepcopy(current_best_state)
            best_fitness = current_best_fitness

        history_max.append(current_best_fitness)
        history_mean.append(sum(list_of_fitness) / len(list_of_fitness))   

    end_time = time.perf_counter()

    return{
        "algorithm": "Genetic Algorithm",
        "config": {
            "population_size": population_size,
            "max_generations": max_generations,
            "mutation_rate": mutation_rate,
            "tournament_size": tournament_size,
            "max_attempts": max_attempts
        },
        "initial_state": initial_state,
        "final_state": best_state,
        "final_value": best_fitness,
        "history_max": history_max,
        "history_mean": history_mean,
        "duration_s": end_time - start_time,
        "iterations": max_generations,
        "evaluations": evaluations,
        "extra": {}
    }    
