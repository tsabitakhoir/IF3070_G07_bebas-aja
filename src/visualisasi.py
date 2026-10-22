import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from src.core import footprint, objective

MAKS_ID = 8

def draw_state(ax, state, problem, judul):
    lebar_kapal = problem["ship"]["width"]
    panjang_kapal = problem["ship"]["length"]

    for i, kendaraan in enumerate(state):
        if kendaraan["location"] != 0:
            continue

        x1, y1, x2, y2 = footprint(problem["vehicles"][i], kendaraan)
        lebar = x2 - x1
        panjang = y2 - y1

        kotak = Rectangle((x1, y1), lebar, panjang,
                          facecolor="skyblue", edgecolor="SteelBlue", linewidth=1)
        ax.add_patch(kotak)
        ax.text(x1 + lebar / 2, y1 + panjang / 2, problem["vehicles"][i]["id"],
            ha="center", va="center", fontsize=10)
        
    ax.set_xlim(0, lebar_kapal)
    ax.set_ylim(0, panjang_kapal)
    ax.set_yticks(range(panjang_kapal + 1))
    ax.set_xticks(range(lebar_kapal + 1))
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.set_title(judul)


def draw_trend(ax, history, judul, y_label):
    ax.plot(history)
    ax.set_title(judul)
    ax.set_xlabel("iterasi")
    ax.set_ylabel(y_label)
    ax.grid(True)

def draw_state_lengkap(ax, state, problem, judul):
    nilai = objective(state, problem)
    berat = 0
    for i, s in enumerate(state):
        if s["location"] == 0:
            berat += problem["vehicles"][i]["weight"]
    kapasitas = problem["ship"]["max_capacity"]

    draw_state(ax, state, problem, f"{judul}\nnilai {nilai}, berat {berat}/{kapasitas}")


    di_luar = []
    for i, s in enumerate(state):
        if s["location"] == -1:
            di_luar.append(problem["vehicles"][i]["id"])

    if len(di_luar) == 0:
        teks = "Di luar kapal: -"
    else:
        teks = f"Di luar kapal ({len(di_luar)}): " + ", ".join(di_luar[:MAKS_ID])
        if len(di_luar) > MAKS_ID:
            teks += f", ... (+{len(di_luar) - MAKS_ID})"

    ax.set_xlabel(teks, fontsize=8)


def draw_trend_multi(ax, series, judul, y_label, x_label="iterasi"):
    for label, history in series.items():
        ax.plot(history, label=label)
    ax.set_title(judul)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True)
    ax.legend()

def draw_info(ax, lines):
    ax.axis("off")
    ax.text(0.0, 1.0, "\n".join(lines), va="top", ha="left",
            family="monospace", fontsize=9, transform=ax.transAxes)

def info_lines(result):
    lines = [f"Algoritma   : {result['algorithm']}"]
    for key, value in result.get("config", {}).items():
        lines.append(f"{key}: {value}")
    lines.append("")
    lines.append(f"Nilai akhir: {result['final_value']}")
    lines.append(f"Durasi: {result['duration_s']:.3f} detik")
    lines.append(f"Iterasi: {result.get('iterations')}")
    lines.append(f"Evaluasi: {result.get('evaluations')}")
    lines.append(f"Seed/run: {result.get('seed')} / {result.get('run')}")
    return lines

def draw_result(result, problem, save_path=None, show=False):

    fig, axes = plt.subplots(2, 2, figsize=(11, 8.5))
    draw_state_lengkap(axes[0, 0], result["initial_state"], problem, "State awal")
    draw_state_lengkap(axes[0, 1], result["final_state"], problem, "State akhir")

    if "history_max" in result:
        draw_trend_multi(
            axes[1, 0],
            {"maksimum": result["history_max"], "rata-rata": result["history_mean"]},
            "Objective populasi per generasi", "Objective", x_label="generasi",
        )
        draw_info(axes[1, 1], info_lines(result))
    else:
        draw_trend(axes[1, 0], result["history"], "Objective per iterasi", "Objective")
        probs = result.get("extra", {}).get("accept_prob_history")
        if probs:
            draw_trend(axes[1, 1], probs, "Probabilitas per iterasi", "e^(delta/T)")
            stuck = result.get("extra", {}).get("count_stuck")
            if stuck is not None:
                axes[1, 1].set_xlabel(f"iterasi (stuck di local optimum: {stuck}x)")
        else:
            draw_info(axes[1, 1], info_lines(result))

    fig.suptitle(f"{result['algorithm']} - run {result.get('run', '?')}")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
