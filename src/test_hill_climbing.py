import random
from algorithms.hill_climbing import hill_climbing_sideways
from core import objective, is_valid
from problem import load_problem
problem = load_problem("test_tc_dummy.json")
 
 
def run(seed, max_sideways=100):
    rng = random.Random(seed)
    return hill_climbing_sideways(problem, rng, max_sideways)
 
 
def tes_jalan_dan_nilai_naik():
    hasil = run(42)
    mulai = hasil[0]
    nilai_akhir = hasil[2]
    history = hasil[3]
 
    nilai_awal = objective(mulai, problem)
    print("nilai awal :", nilai_awal)
    print("nilai akhir:", nilai_akhir)
 
    assert history[0] == nilai_awal
    assert nilai_akhir >= nilai_awal
    print("tes 1 lolos")
 
 
def tes_state_akhir_valid():
    hasil = run(42)
    akhir = hasil[1]
    assert is_valid(akhir, problem)
    print("tes 2 lolos")
 
 
def tes_history():
    hasil = run(42)
    nilai_akhir = hasil[2]
    history = hasil[3]
    iterasi = hasil[5]
 
    # gak boleh ada yang turun
    for i in range(1, len(history)):
        if history[i] < history[i - 1]:
            print("history turun di index", i, ":", history[i - 1], "->", history[i])
        assert history[i] >= history[i - 1]
 
    assert len(history) == iterasi + 1
    assert history[-1] == nilai_akhir
    print("panjang history:", len(history), "iterasi:", iterasi)
    print("tes 3 lolos")
 
 
def tes_seed_sama():
    a = run(42)
    b = run(42)

    # nilai akhir
    assert a[2] == b[2]   
    # history
    assert a[3] == b[3]   
    # iterasi
    assert a[5] == b[5]   
    # evaluasi
    assert a[6] == b[6]   
    # sideways
    assert a[7] == b[7]   
    print("tes 4 lolos")
 
 
def tes_max_sideways():
    r0 = run(42, 0)
    r100 = run(42, 100)
 
    print("max_sideways=0   -> nilai", r0[2], "| iterasi", r0[5], "| evaluasi", r0[6], "| sideways", r0[7])
    print("max_sideways=100 -> nilai", r100[2], "| iterasi", r100[5], "| evaluasi", r100[6], "| sideways", r100[7])
 
    # kalau max 0, gak boleh ada sideways sama sekali
    assert r0[7] == 0
    # seed sama, jadi lintasan max=0 itu bagian awal dari lintasan max=100
    assert r100[2] >= r0[2]
    assert r100[5] >= r0[5]
    print("tes 5 lolos")
 
 
def tes_banyak_seed():
    for seed in range(10):
        hasil = run(seed)
        assert is_valid(hasil[1], problem)
        assert hasil[2] >= hasil[3][0]
        print("seed", seed, "ok, nilai akhir", hasil[2])
    print("tes 6 lolos")
 
 
if __name__ == "__main__":
    tes_jalan_dan_nilai_naik()
    tes_state_akhir_valid()
    tes_history()
    tes_seed_sama()
    tes_max_sideways()
    tes_banyak_seed()
    print("semua tes lolos")

