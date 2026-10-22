from itertools import combinations
from src.core import is_valid

def copy_state(state):
    return [dict(v) for v in state]

def update_state(state, updates):
    new_state = copy_state(state)
    for i, v in updates.items():
        new_state[i] = v
    return new_state

def shift(state, problem):
    width = problem["ship"]["width"]
    length = problem["ship"]["length"]
    res = []

    for i, v in enumerate(state):
        if v["location"] != 0:
            continue
        for x in range(width):
            for y in range(length):
                if x == v["x"] and y == v["y"]:
                    continue
                res.append(update_state(state, {i: {**v, "x": x, "y": y}}))

    return res

def rotate(state, problem):
    res = []

    for i, v in enumerate(state):
        if v["location"] != 0:
            continue
        if v["orientation"] == "H":
            new_o = "V"
        else:
            new_o = "H"
        res.append(update_state(state, {i: {**v, "orientation": new_o}}))

    return res

def enter(state, problem):
    width = problem["ship"]["width"]
    length = problem["ship"]["length"]
    res = []

    for i, v in enumerate(state):
        if v["location"] != -1:
            continue
        for x in range(width):
            for y in range(length):
                for o in ("H", "V"):
                    res.append(update_state(state, {i: {"location": 0, "x": x, "y": y, "orientation": o}}))

    return res

def outside():
    return {"location": -1, "x": 0, "y": 0, "orientation": "H"}

def leave(state, problem):
    res = []

    for i, v in enumerate(state):
        if v["location"] != 0:
            continue
        res.append(update_state(state, {i: outside()}))

    return res

def swap_2in(state, problem):
    in_ship = [i for i, v in enumerate(state) if v["location"] == 0]
    res = []

    for i, j in combinations(in_ship, 2):
        k, l = state[i], state[j]
        if k["x"] == l["x"] and k["y"] == l["y"]:
            continue
        res.append(update_state(state, {i: {**k, "x": l["x"], "y": l["y"]}, j: {**l, "x": k["x"], "y": k["y"]}}))

    return res

def swap_inout(state, problem):
    in_ship = [i for i, v in enumerate(state) if v["location"] == 0]
    out_ship = [j for j, v in enumerate(state) if v["location"] == -1]
    res = []

    for i in in_ship:
        for j in out_ship:
            for o in ("H", "V"):
                res.append(update_state(state, {i: outside(), j: {"location": 0, "x": state[i]["x"], "y": state[i]["y"], "orientation": o}}))

    return res

ALL_MOVE = [shift, rotate, enter, leave, swap_2in, swap_inout]

def all_neighbors(state, problem):
    res = []

    for move in ALL_MOVE:
        for s in move(state, problem):
            if is_valid(s, problem):
                res.append(s)

    return res

def random_neighbor(state, problem, rng):
    neighbors = all_neighbors(state, problem)
    if not neighbors:
        return None
    return rng.choice(neighbors)