# matriks
# ini matriks ukuran 3x3, yaitu 3 baris dan 3 kolom
matriks = [
   [10, 20, 30],
   [40, 50, 60],
   [70, 80, 90]
]

# menampilkan matriks satu per satu
# perulangannya menggunakan for sehingga setiap elemen (yang berupa list) ditampilkan satu per satu
for nilai in matriks:
   print (nilai)

# iteratif
# kenapa fungsi ini butuh parameter matriks?
# karena matriks yang akan diproses ada di luar fungsi
# sehingga agar fungsi ini bisa membaca matriks tersebut, maka matriks itu harus dikirim ke dalam fungsi ini sebagai parameter
def iteratif(matriks):
   # pertama, anggap elemen pertama sebagai maksimum
   # karena nanti nilai maksismumnya akan dibandingnkan dengan elemen lainnya
   # dan jika elemen yang nantinya dibandingkan ternyata lebih besar dari nilai maksimum yang sekarang
   # maka nanti nilai yang lebih besar itu akan mengisi variabel maksimum
   maksimum = matriks[0][0]

   # perulangan secara horizontal
   # artinya perulangan berjalan dari baris pertama hingga baris terakhir
   for baris in matriks:
      # perulangaan secara vertikal
      # maksudnya perulangan berjalan dari kolom pertama sampai kolom terakhir dalam satu baris
      for nilai in baris:
         # jika nilai yang ditemukan dalam proses pencarian ternyata lebih besar dari variabel maksimum yang sudah ditentukan di awal
         if nilai > maksimum:
            # maka nilai tersebutlah yang akan mengisi variabel maksimum
            maksimum = nilai

   # setelah semua nilai selesai diperiksa, kembalikan nilai maksimum yang telah ditemukan
   return maksimum

# rekursif
def rekursif(matriks, baris = 0, kolom = 0):
   # jika baris sudah mencapai jumlah baris dalam matriks
   # itu artinya seluruh elemen matriks sudah selesai diproses
   # maka fungsi harus berhenti dan mengembalikan nilai dasar (base case)
   if baris == len(matriks):
      # float('-inf') digunakan karena merupakan nilai yang sangat kecil sehingga tidak mengganggu hasil pencarian maksimum
      return float('-inf')

   # menentukan baris selanjutnya yang akan diproses
   # awalnya baris selanjutnya dianggap sama dengan baris sekarang
   baris_selanjutnya = baris
   # kolom selanjutnya ditetapkan sebagai kolom saat ini ditambah satu
   # karena pergerakan normal dalam matriks adalah bergerak ke kanan dulu
   kolom_selanjutnya = kolom + 1

   # pengecekan apakah pergerakan ke kanan sudah melewati batas kolom
   # jika iya maka harus pindah ke baris berikutnya
   if kolom_selanjutnya == len(matriks[0]):
      # menambah nilai baris agar pindah ke baris selanjutnya
      baris_selanjutnya += 1
      # kolom di-reset menjadi 0 karena kembali ke kolom pertama di baris baru
      kolom_selanjutnya = 0

   # bagian yang melakukan proses rekursi
   # fungsi membandingkan nilai elemen saat ini dengan nilai maksimum dari sisa elemen yang dihitung oleh pemanggilan rekursif
   return max(matriks[baris][kolom], rekursif(matriks, baris_selanjutnya, kolom_selanjutnya))

# menampilkan hasil pencarian
# memanggil fungsi iteratif untuk menampilkan hasil maksimum dengan cara perulangan biasa
print("secara iteratif :", iteratif(matriks))
# memanggil fungsi rekursif untuk menampilkan hasil maksimum dengan menggunakan teknik rekursi
print("secara rekursif :", rekursif(matriks))