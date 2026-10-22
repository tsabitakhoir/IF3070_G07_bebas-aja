import copy
import time
from src.problem import random_state
from src.core import is_valid, objective

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

# fungsi crossover. child mulai dari parent1, lalu gen parent2 setelah titik potong
# ditempel satu-satu, kalau bikin child nggak valid gen itu dilewati
def crossover(parent1, parent2, problem, rng):
    crossover_point = rng.randint(1, len(parent1) - 1)
    child = copy.deepcopy(parent1)
    for i in range(crossover_point, len(parent2)):
        if child[i] == parent2[i]:
            continue
        lama = child[i]
        child[i] = dict(parent2[i])
        if not is_valid(child, problem):
            child[i] = lama
    return child

# fungsi mutation. pilih satu kendaraan, kalau lagi di kapal kadang dikeluarin,
# selain itu ditaruh di posisi dan orientasi acak. diulang sampai ketemu yang valid
def mutation(child, problem, rng, mutation_rate=1.0, max_attempts=10):
    if rng.random() > mutation_rate:
        return child

    ship = problem["ship"]
    for _ in range(max_attempts):
        i = rng.randint(0, len(child) - 1)
        origin_state = child[i]

        if origin_state["location"] == 0 and rng.random() < 0.3:
            child[i] = {"location": -1, "x": 0, "y": 0, "orientation": "H"}
        else:
            v = problem["vehicles"][i]
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
            child[i] = {"location": 0, "x": rng.randint(0, limit_x), "y": rng.randint(0, limit_y), "orientation": orientation}

        if is_valid(child, problem):
            return child
        child[i] = origin_state

    return child

# fungsi mating. fungsi buat ngeprodiksi satu anak yang valid
def mating (list_of_states, list_of_fitness, problem, rng, mutation_rate, tournament_size, max_attempts=10):
    pi1 = tournament(list_of_fitness, list_of_states, rng, tournament_size=tournament_size)[0]
    pi2 = tournament(list_of_fitness, list_of_states, rng, prohibited=[pi1], tournament_size=tournament_size)[0]
    child = crossover(list_of_states[pi1], list_of_states[pi2], problem, rng)
    return mutation(child, problem, rng, mutation_rate, max_attempts)

#fungsi utama genetic algorithm
def genetic_algorithm(problem, rng, population_size=50, max_generations=100, mutation_rate=1.0, tournament_size=3, max_attempts=10):
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
