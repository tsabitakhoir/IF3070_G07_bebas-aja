# IF3070_G07_bebas-aja
Tugas Besar 1 IF3070 - local search untuk penataan kendaraan di geladak kapal

## Deskripsi Singkat
Tujuan dari sistem ini adalah memaksimalkan total ShippingFee dari kendaraan yang berada di atas kapal. Terdapat tiga batasan yang harus dipenuhi. Pertama, kendaraan tidak boleh saling bertindihan, sehingga satu sel geladak hanya boleh ditempati satu kendaraan. Kedua, seluruh sel yang ditempati harus berada dalam batas geladak. Ketiga, total berat seluruh kendaraan yang berada di kapal tidak boleh melebihi kapasitas maksimum kapal. 
	
Dalam pengerjaan tugas ini, kami menggunakan pendekatan local search. Tiga algoritma yang dibandingkan adalah 

- Hill-Climbing
- Simulated Annealing
- Genetic Algorithm. 

## Cara Setup
1. Clone repo ini:
    ```bash
    git clone
    https://github.com/tsabitakhoir/IF3070_G07_bebas-aja.git
    cd IF3070_G07_bebas-aja
    ```

2. Install matplotlib library
    ```bash
    pip install matplotlib
    ```

## Cara Menjalankan Algoritma
Program dijalankan dari root repositroy. Tanpa argumen, program akan menjalkan semua eksperimen dengan test case kecil.

    ```bash
    python src/runner.py
    ```

atau

    ```bash
    python -m src.runner
    ```
Opsi yang tersedia:
| Opsi | Fungsi |
|---|---|
| `--testcase <path>` | File test case |
| `--only <nama..>` | Hanya jalankan eksperiemn tertentu: contoh: `GA_iteration` |
| `--seed <angka..>` | Seed pada setiap run |

## Struktur Repository
```
├── src/
│   ├── core.py                    
│   ├── neighbors.py               
│   ├── problem.py                 
│   ├── visualisasi.py             
│   ├── runner.py                  
│   └── algorithms/
│       ├── hill_climbing.py
│       ├── simulated_annealing.py
│       └── genetic_algorithm.py
├── tests/                         
├── input/ (berisikan seluruh test_case file)                        
├── output/ (berisikan seluruh output eksperimen (json dan visualisasi))                       
├── docs/ (berisikan laporan)                         
└── README.md
```

## Pembagian Tugas
| NIM | Nama | Pembagian Tugas |
|---|---|---|
| 18224006 | Tsabita Khoirunnisa | - Inisialisasi pembagian tugas<br>- Mengerjakan core.py<br>- Mengerjakan hill_climbing.py<br>- Mengerjakan runner.py, generator_testcase.py, dan visualisasi.py<br>- Penulisan core.py, visualisasi.py, dan hill_climbing.py  pada laporan |
| 18224034 | Wa Ode Amerta Lambelu Jamaluddin | - Mengerjakan problem.py<br>- Mengerjakan genetic_algorithm.py<br>- Mengerjakan testcase_generator.py<br>- Menuliskan algoritma genetik di laporan<br>- Menuliskan problem.py dan generator_testcase.py di laporan |
| 18224048 | Melvin Irsyad | - Mengerjakan neighbors.py<br>- Mengerjakan simulated_annealing.py<br>- Inisialisasi pengerjaan visualisasi.py<br>- Penulisan neighbors.py pada laporan<br>- Penulisan runner.py pada laporan<br>- Penulisan simulated_annealing.py, seluruh eksperimennya, dan analisis pada laporan<br>- Membantu formatting dokumen dan menambahkan README.md |
