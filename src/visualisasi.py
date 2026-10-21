import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from core import footprint

def draw_state(ax, state, problem, judul):
    w_ship = problem["ship"]["width"]
    l_ship = problem["ship"]["length"]

    for i, j in enumerate(state):
        if j["location"] == 0:
            x, y, xa, ya = footprint(problem["vehicles"][i], j)
            w = xa - x
            l = ya - y 
            label = problem["vehicles"][i]["id"]
            rect = Rectangle((x, y), w, l, facecolor="skyblue", edgecolor="SteelBlue", linewidth=1)
            ax.add_patch(rect)
            ax.text((x + w/2), (y + l/2), label, ha="center", va="center", fontsize=10)

    ax.set_xlim(0, w_ship)
    ax.set_ylim(0, l_ship)
    ax.set_yticks(range(l_ship + 1))
    ax.set_xticks(range(w_ship + 1))
    ax.set_aspect("equal")

    ax.invert_yaxis()
    ax.set_title(judul)

def draw_trend(ax, history, judul, y_label):
    ax.plot(history)
    ax.set_title(judul)
    ax.set_xlabel("iterasi")
    ax.set_ylabel(y_label)
    ax.grid(True)