import matplotlib.pyplot as plt
import time
import random

def iteratif(matriks):
   if not matriks:
      return float('-inf')
   maksimal = float('-inf')
   for baris in matriks:
      for nilai in baris:
         if nilai > maksimal:
            maksimal = nilai
   return maksimal

def rekursif(matriks):
   if not matriks:
      return float('-inf')

   def rekursif_max(baris, kolom, max_sementara):
      if baris >= len(matriks):
         return max_sementara

      if not matriks[baris]:
         return rekursif_max(baris + 1, 0, max_sementara)

      if kolom >= len(matriks[baris]):
         return rekursif_max(baris + 1, 0, max_sementara)

      nilai_sekarang = matriks[baris][kolom]

      if nilai_sekarang > max_sementara:
         max_sementara = nilai_sekarang

      return rekursif_max(baris, kolom + 1, max_sementara)
   return rekursif_max(0, 0, float('-inf'))

def rekursif_divide_conquer(matriks):
   if not matriks or not matriks[0]:
      return float('-inf')
   
   def dc_max(baris_start, baris_end, kolom_start, kolom_end):
      if baris_start >= baris_end or kolom_start >= kolom_end:
         return float('-inf')
      
      if baris_end - baris_start == 1 and kolom_end - kolom_start == 1:
         return matriks[baris_start][kolom_start]
      
      baris_mid = (baris_start + baris_end) // 2
      kolom_mid = (kolom_start + kolom_end) // 2

      return max(
         dc_max(baris_start, baris_mid, kolom_start, kolom_mid),
         dc_max(baris_start, baris_mid, kolom_mid, kolom_end),
         dc_max(baris_mid, baris_end, kolom_start, kolom_mid),
         dc_max(baris_mid, baris_end, kolom_mid, kolom_end)
      )

   return dc_max(0, len(matriks), 0, len(matriks[0]))

def buat_matriks(n, seed=None):
   if seed is not None:
      random.seed(seed)
   return [[random.randint(1, 1000) for _ in range(n)] for _ in range(n)]

def ukur_waktu(func, matriks):
   start = time.perf_counter()
   func(matriks)
   end = time.perf_counter()
   return end - start

matriks = [
   [10,  20,  30,  40,  50,  60,  70,  80,  90,  100],
   [110, 120, 130, 140, 150, 160, 170, 180, 190, 200],
   [210, 220, 230, 240, 250, 260, 270, 280, 290, 300],
   [310, 320, 330, 340, 350, 360, 370, 380, 390, 400],
   [410, 420, 430, 440, 450, 460, 470, 480, 490, 500],
   [510, 520, 530, 540, 550, 560, 570, 580, 590, 600],
   [610, 620, 630, 640, 650, 660, 670, 680, 690, 700],
   [710, 720, 730, 740, 750, 760, 770, 780, 790, 800],
   [810, 820, 830, 840, 850, 860, 870, 880, 890, 900],
   [910, 920, 930, 940, 950, 960, 970, 980, 990, 1000]
]

print("Matriks :")
for baris in matriks:
   print(baris)

max_iteratif = iteratif(matriks)
max_rekursif = rekursif(matriks)
max_divide_conquer = rekursif_divide_conquer(matriks)
print("\nIteratif :", max_iteratif)
print("Rekursif :", max_rekursif)
print("Rekursif DC :", max_divide_conquer)

ukuran_list = [1, 2, 3, 4, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500]
n_ukuran = len(ukuran_list)

waktu_iteratif = [float('nan')] * n_ukuran
waktu_rekursif = [float('nan')] * n_ukuran
waktu_dc = [float('nan')] * n_ukuran

print("\nMengukur waktu eksekusi...")
for i, n in enumerate(ukuran_list):
   print(f"  Menguji ukuran {n}x{n}...")
   m = buat_matriks(n, seed=42)

   try:
      waktu_iteratif[i] = ukur_waktu(iteratif, m)
   except Exception as e:
      print(f"   Iteratif error: {e}")

   try:
      waktu_rekursif[i] = ukur_waktu(rekursif, m)
   except RecursionError:
      print(f"   Rekursif: RecursionError pada n={n}")
   except Exception as e:
      print(f"   Rekursif error: {e}")

   try:
      waktu_dc[i] = ukur_waktu(rekursif_divide_conquer, m)
   except RecursionError:
      print(f"   Divide & Conquer: RecursionError pada n={n}")
   except Exception as e:
      print(f"   Divide & Conquer error: {e}")

plt.figure(figsize=(8, 5))
plt.plot(ukuran_list, waktu_iteratif, label='Iteratif', color='green', marker='o')
plt.plot(ukuran_list, waktu_rekursif, label='Rekursif', color='blue', marker='s')
plt.plot(ukuran_list, waktu_dc, label='Rekursif Divide & Conquer', color='orange', marker='^')

plt.xlabel('Ukuran Matriks (n x n)')
plt.ylabel('Waktu Eksekusi (detik)')
plt.title('Laju Pertumbuhan Waktu Eksekusi Ketiga Algoritma')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.yscale('log')
plt.tight_layout()
plt.show()
