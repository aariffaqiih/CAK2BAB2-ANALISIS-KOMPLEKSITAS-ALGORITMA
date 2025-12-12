import matplotlib.pyplot as plt
import time
import random

# === FUNGSI ALGORITMA KAMU ===
def iteratif(matriks):
    if not matriks:
        return float('-inf')
    maksimum = float('-inf')
    for baris in matriks:
        for nilai in baris:
            if nilai > maksimum:
                maksimum = nilai
    return maksimum

def rekursif(matriks):
    if not matriks:
        return float('-inf')
    def rekursif_maks(baris, kolom, maks_sementara):
        if baris >= len(matriks):
            return maks_sementara
        if not matriks[baris]:
            return rekursif_maks(baris + 1, 0, maks_sementara)
        if kolom >= len(matriks[baris]):
            return rekursif_maks(baris + 1, 0, maks_sementara)
        nilai_sekarang = matriks[baris][kolom]
        if nilai_sekarang > maks_sementara:
            maks_sementara = nilai_sekarang
        return rekursif_maks(baris, kolom + 1, maks_sementara)
    return rekursif_maks(0, 0, float('-inf'))

def rekursif_divide_conquer(matriks):
    if not matriks:
        return float('-inf')
    def flatten(rows):
        if not rows:
            return []
        return rows[0] + flatten(rows[1:])
    data = flatten(matriks)
    if not data:
        return float('-inf')
    def rekursif_maks(lst):
        if len(lst) == 1:
            return lst[0]
        mid = len(lst) // 2
        kiri = rekursif_maks(lst[:mid])
        kanan = rekursif_maks(lst[mid:])
        return kiri if kiri > kanan else kanan
    return rekursif_maks(data)

# === GENERATOR MATRIKS ===
def buat_matriks(n, seed=None):
    if seed is not None:
        random.seed(seed)
    return [[random.randint(1, 1000) for _ in range(n)] for _ in range(n)]

def ukur_waktu(func, matriks):
    start = time.perf_counter()
    func(matriks)
    end = time.perf_counter()
    return end - start

# === DATA UJI ===
matriks_awal = [
   [10, 20, 30, 40, 50, 60],
   [15, 25, 35, 45, 55, 65],
   [27, 29, 37, 48, 59, 69],
   [32, 33, 39, 50, 60, 70],
   [35, 36, 40, 51, 66, 71],
   [39, 41, 43, 55, 67, 99]
]

print("Matriks awal:")
for baris in matriks_awal:
    print(baris)

maks_iteratif = iteratif(matriks_awal)
maks_rekursif = rekursif(matriks_awal)
maks_divide_conquer = rekursif_divide_conquer(matriks_awal)
print("\nIteratif :", maks_iteratif)
print("Rekursif :", maks_rekursif)
print("Rekursif DC :", maks_divide_conquer)

# === PENGUKURAN UNTUK GRAFIK ASYMPTOTIC ===
ukuran_list = [10, 20, 30, 40, 50]
n_ukuran = len(ukuran_list)

waktu_iter = [float('nan')] * n_ukuran
waktu_rek = [float('nan')] * n_ukuran
waktu_dc = [float('nan')] * n_ukuran

print("\nMengukur waktu eksekusi...")
for i, n in enumerate(ukuran_list):
    print(f"  Menguji ukuran {n}x{n}...")
    m = buat_matriks(n, seed=42)

    # Iteratif
    try:
        waktu_iter[i] = ukur_waktu(iteratif, m)
    except Exception as e:
        print(f"    Iteratif error: {e}")

    # Rekursif
    try:
        waktu_rek[i] = ukur_waktu(rekursif, m)
    except RecursionError:
        print(f"    Rekursif: RecursionError pada n={n}")
    except Exception as e:
        print(f"    Rekursif error: {e}")

    # Divide & Conquer
    try:
        waktu_dc[i] = ukur_waktu(rekursif_divide_conquer, m)
    except RecursionError:
        print(f"    Divide & Conquer: RecursionError pada n={n}")
    except Exception as e:
        print(f"    Divide & Conquer error: {e}")

# === PLOT GRAFIK ===
plt.figure(figsize=(8, 5))
plt.plot(ukuran_list, waktu_iter, label='Iteratif', color='green', marker='o')
plt.plot(ukuran_list, waktu_rek, label='Rekursif', color='blue', marker='s')
plt.plot(ukuran_list, waktu_dc, label='Rekursif Divide & Conquer', color='orange', marker='^')

plt.xlabel('Ukuran Matriks (n × n)')
plt.ylabel('Waktu Eksekusi (detik)')
plt.title('Laju Pertumbuhan Waktu Eksekusi Ketiga Algoritma')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.yscale('log')
plt.tight_layout()
plt.show()
