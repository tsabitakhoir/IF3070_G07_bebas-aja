
# footprint
def footprint(vehicle, placement):
    width = vehicle["width"]
    length = vehicle["length"]
    if (placement["orientation"] == "H"):
        width_x = width
        length_y = length
    elif (placement["orientation"] == "V"):
        width_x = length
        length_y = width
    else:
        orientation = placement["orientation"]
        raise ValueError(f"Tidak ada orientasi: {orientation!r}, Orientasi yang valid hanya H/V")
    x_akhir = placement["x"] + width_x
    y_akhir = placement["y"] + length_y
    x_awal = placement["x"]
    y_awal = placement["y"]
    return (x_awal, y_awal, x_akhir, y_akhir)

# in_bound
def in_bound(box, ship):
    return (box[0] >= 0 and
            box[1] >= 0 and
            box[2] <= ship["width"] and
            box[3] <= ship["length"])  

# overlap
def overlap(box1, box2):
    return not (box1[2] <= box2[0] or
                box2[2] <= box1[0] or
                box1[3] <= box2[1] or
                box2[3] <= box1[1])

# total_weight
def total_weight(state, problem):
    total = 0
    for (i,vehicle) in enumerate(problem["vehicles"]):
        placement = state[i]
        if placement["location"] == 0:
            total += problem["vehicles"][i]["weight"]
    return total

# is_valid
def is_valid(state, problem):
    if total_weight(state, problem) > problem["ship"]["max_capacity"]:
        return False
    for (i,vehicle) in enumerate(problem["vehicles"]):
        placement = state[i]
        if placement["location"] != 0:
            continue
        box1 = footprint(vehicle, placement)
        if not in_bound(box1, problem["ship"]):
            return False
        for j in range(i+1, len(problem["vehicles"])):
            placement2 = state[j]
            if placement2["location"] != 0:
                continue
            vehicle2 = problem["vehicles"][j]
            box2 = footprint(vehicle2, placement2)
            if overlap(box1, box2):
                return False
    return True

# objective
def objective(state, problem):
    total = 0
    for (i,vehicle) in enumerate(problem["vehicles"]):
        placement = state[i]
        if placement["location"] == 0:
            total += problem["vehicles"][i]["fee"]
    return total


