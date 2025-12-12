matriks = [
   [10, 20, 30, 40, 50, 60],
   [15, 25, 35, 45, 55, 65],
   [27, 29, 37, 48, 59, 69],
   [32, 33, 39, 50, 60, 70],
   [35, 36, 40, 51, 66, 71],
   [39, 41, 43, 55, 67, 99]
]

print("Matriks awal:")
for nilai in matriks:
   print(nilai)

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

maks_iteratif = iteratif(matriks)
maks_rekursif = rekursif(matriks)
maks_divide_conquer = rekursif_divide_conquer(matriks)
print("\nIteratif :", maks_iteratif)
print("Rekursif :", maks_rekursif)
print("Rekursif DC :", maks_divide_conquer)
