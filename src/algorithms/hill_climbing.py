import time

from src.core import objective
from src.neighbors import copy_state, all_neighbors
from src.problem import random_state
 
 
def hill_climbing_sideways(problem, rng, max_sideways=100):
    mulai = random_state(problem, rng)
    sekarang = copy_state(mulai)
    nilai_sekarang = objective(sekarang, problem)
 
    history = [nilai_sekarang]
    sideways = 0
    iterasi = 0
    evaluasi = 1
    t0 = time.perf_counter()
    total_sideways = 0
    alasan = ""
 
    while True:
        tetangga = all_neighbors(sekarang, problem)
        if len(tetangga) == 0:
            alasan = "tidak ada tetangga"
            break
 
        # menghitung nilai tetangga
        nilai = []
        for t in tetangga:
            nilai.append(objective(t, problem))
        evaluasi += len(tetangga)
 
        # nyari tetangga terbaik, kalau sama pilih acak
        nilai_terbaik = max(nilai)
        seri = []
        for i in range(len(nilai)):
            if nilai[i] == nilai_terbaik:
                seri.append(i)
        terbaik = tetangga[rng.choice(seri)]
 
        if nilai_terbaik > nilai_sekarang:
            sekarang = terbaik
            nilai_sekarang = nilai_terbaik
            sideways = 0
        elif nilai_terbaik == nilai_sekarang and sideways < max_sideways:
            sekarang = terbaik
            sideways += 1
            total_sideways += 1
        else:
            if nilai_terbaik == nilai_sekarang:
                alasan = "jatah sideways habis"
            else:
                alasan = "puncak lokal"
            break
 
        iterasi += 1
        history.append(nilai_sekarang)
 
    durasi = time.perf_counter() - t0
    return mulai, sekarang, nilai_sekarang, history, durasi, iterasi, evaluasi, sideways, total_sideways, alasan