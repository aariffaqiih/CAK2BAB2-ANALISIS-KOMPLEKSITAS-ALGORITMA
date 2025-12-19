import streamlit as st
import matplotlib.pyplot as plt
import time
import random
import pandas as pd
import numpy as np

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
   result = func(matriks)
   end = time.perf_counter()
   return result, end - start

st.set_page_config(page_title="Analisis Kompleksitas Algoritma Maksimum Matriks", layout="centered")

st.title("Analisis Kompleksitas Algoritma Pencarian Nilai Maksimum Matriks")
st.markdown("""
Program ini menganalisis performa tiga algoritma pencarian nilai maksimum dalam matriks:
1. **Iteratif** - Pencarian linear melalui setiap elemen
2. **Rekursif** - Pencarian dengan rekursi berurutan
3. **Divide and Conquer Rekursif** - Pencarian dengan pembagian matriks
""")

with st.container():
   st.header("Konfigurasi Generator Matriks")
   col1, col2 = st.columns(2)
   with col1:
      ukuran_matriks = st.number_input("Ukuran Matriks (n x n)", min_value=1, max_value=10000, value=10, step=1)
      seed_acak = st.number_input("Seed untuk Reproduktibilitas", value=42)
   with col2:
      rentang_min = st.number_input("Rentang Minimum", value=1)
      rentang_max = st.number_input("Rentang Maksimum", value=1000)

   if st.button("Generate Matriks", type="primary"):
      random.seed(seed_acak)
      matriks = [[random.randint(rentang_min, rentang_max) for _ in range(ukuran_matriks)] for _ in range(ukuran_matriks)]
      st.session_state.matriks = matriks
      st.session_state.generated = True

if 'matriks' in st.session_state:
   with st.container():
      st.header("Matriks yang Dihasilkan")
      df = pd.DataFrame(st.session_state.matriks)
      st.dataframe(df, height=400, use_container_width=True)
      
      total_elemen = ukuran_matriks * ukuran_matriks
      nilai_min = min(min(baris) for baris in st.session_state.matriks)
      nilai_maks = max(max(baris) for baris in st.session_state.matriks)
      
      st.subheader("Deskripsi Matriks")
      col1, col2, col3 = st.columns(3)
      col1.metric("Ukuran Matriks", f"{ukuran_matriks} × {ukuran_matriks}")
      col2.metric("Total Elemen", f"{total_elemen:,}")
      col3.metric("Rentang Nilai", f"{nilai_min} - {nilai_maks}")

with st.container():
   st.header("Hasil Pencarian Nilai Maksimum")
   
   if 'matriks' in st.session_state:
      col1, col2, col3 = st.columns(3)
      
      with col1:
         st.subheader("Algoritma Iteratif")
         try:
            hasil_iteratif, waktu_iteratif = ukur_waktu(iteratif, st.session_state.matriks)
            st.metric("Nilai Maksimum", hasil_iteratif)
            st.metric("Waktu Eksekusi", f"{waktu_iteratif:.6f} detik")
            st.session_state.hasil_iteratif = hasil_iteratif
            st.session_state.waktu_iteratif = waktu_iteratif
         except Exception as e:
            st.error(f"Error: {e}")
      
      with col2:
         st.subheader("Algoritma Rekursif")
         try:
            hasil_rekursif, waktu_rekursif = ukur_waktu(rekursif, st.session_state.matriks)
            st.metric("Nilai Maksimum", hasil_rekursif)
            st.metric("Waktu Eksekusi", f"{waktu_rekursif:.6f} detik")
            st.session_state.hasil_rekursif = hasil_rekursif
            st.session_state.waktu_rekursif = waktu_rekursif
         except RecursionError:
            st.error("RecursionError: Kedalaman rekursi melebihi batas")
         except Exception as e:
            st.error(f"Error: {e}")
      
      with col3:
         st.subheader("Algoritma Divide & Conquer")
         try:
            hasil_dc, waktu_dc = ukur_waktu(rekursif_divide_conquer, st.session_state.matriks)
            st.metric("Nilai Maksimum", hasil_dc)
            st.metric("Waktu Eksekusi", f"{waktu_dc:.6f} detik")
            st.session_state.hasil_dc = hasil_dc
            st.session_state.waktu_dc = waktu_dc
         except RecursionError:
            st.error("RecursionError: Kedalaman rekursi melebihi batas")
         except Exception as e:
            st.error(f"Error: {e}")

with st.container():
   st.header("Analisis Teoritis Kompleksitas Algoritma")
   
   st.subheader("1. Algoritma Iteratif")
   st.latex(r"""
   \begin{aligned}
   &T(n) = \Theta(n^2) \\
   &S(n) = \Theta(1)
   \end{aligned}
   """)
   st.markdown("""
   **Analisis**: 
   - Kompleksitas waktu: $\\Theta(n^2)$ karena dua loop bersarang
   - Kompleksitas ruang: $\\Theta(1)$ hanya menyimpan satu variabel maksimum
   - Notasi Big-O: $O(n^2)$
   """)
   
   st.subheader("2. Algoritma Rekursif")
   st.latex(r"""
   \begin{aligned}
   &T(n) = T(n-1) + \Theta(1) \\
   &S(n) = \Theta(n^2)
   \end{aligned}
   """)
   st.markdown("""
   **Analisis**: 
   - Kompleksitas waktu: $\\Theta(n^2)$ dengan relasi rekurensi
   - Kompleksitas ruang: $\\Theta(n^2)$ karena stack rekursi
   - Recurrence Relation: $T(m) = T(m-1) + \\Theta(1)$ dimana $m = n^2$
   """)
   
   st.subheader("3. Algoritma Divide & Conquer Rekursif")
   st.latex(r"""
   \begin{aligned}
   &T(n) = 4T\left(\frac{n}{2}\right) + \Theta(1) \\
   &\text{Dengan Teorema Master: } a=4, b=2, d=0 \\
   &a > b^d \Rightarrow 4 > 2^0 \Rightarrow T(n) = \Theta(n^{\log_2 4}) = \Theta(n^2)
   \end{aligned}
   """)
   st.markdown("""
   **Analisis**: 
   - Kompleksitas waktu: $\\Theta(n^2)$ berdasarkan Teorema Master
   - Kompleksitas ruang: $\\Theta(\log n)$ untuk stack rekursi
   - Case 3 Teorema Master: $\\Theta(n^{\\log_b a}) = \\Theta(n^{\\log_2 4}) = \\Theta(n^2)$
   """)

with st.container():
   st.header("Analisis Performa Berbagai Ukuran Input")
   
   input_ukuran = st.text_input("Masukkan ukuran matriks (pisahkan dengan koma)", "1,10,20,50,100,200,500,1000,2000,5000,10000")
   
   if st.button("Run Analisis Komprehensif", type="primary"):
      try:
         ukuran_list = [int(x.strip()) for x in input_ukuran.split(",")]
         ukuran_list = [x for x in ukuran_list if 1 <= x <= 10000]
         ukuran_list.sort()
         
         if not ukuran_list:
            st.error("Masukkan setidaknya satu ukuran valid antara 1-10000")
         else:
            waktu_iteratif_list = []
            waktu_rekursif_list = []
            waktu_dc_list = []
            ukuran_valid = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, n in enumerate(ukuran_list):
               status_text.text(f"Menganalisis matriks {n} × {n}...")
               progress_bar.progress((idx + 1) / len(ukuran_list))
               
               try:
                  m = buat_matriks(n, seed=42)
                  ukuran_valid.append(n)
                  
                  _, waktu_iter = ukur_waktu(iteratif, m)
                  waktu_iteratif_list.append(waktu_iter)
                  
                  try:
                     _, waktu_rek = ukur_waktu(rekursif, m)
                     waktu_rekursif_list.append(waktu_rek)
                  except RecursionError:
                     waktu_rekursif_list.append(float('nan'))
                  
                  try:
                     _, waktu_dc = ukur_waktu(rekursif_divide_conquer, m)
                     waktu_dc_list.append(waktu_dc)
                  except RecursionError:
                     waktu_dc_list.append(float('nan'))
                     
               except MemoryError:
                  st.warning(f"Memori tidak cukup untuk matriks {n}×{n}")
                  break
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            ax.plot(ukuran_valid, waktu_iteratif_list, label='Iteratif', color='green', marker='o', linewidth=2)
            ax.plot(ukuran_valid, waktu_rekursif_list, label='Rekursif', color='blue', marker='s', linewidth=2)
            ax.plot(ukuran_valid, waktu_dc_list, label='Divide & Conquer', color='orange', marker='^', linewidth=2)
            
            ax.set_xlabel('Ukuran Matriks (n × n)', fontsize=12)
            ax.set_ylabel('Waktu Eksekusi (detik)', fontsize=12)
            ax.set_title('Perbandingan Waktu Eksekusi Tiga Algoritma', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.set_yscale('log')
            ax.set_xscale('log')
            
            st.pyplot(fig)
            
            st.session_state.analisis_data = {
               'ukuran': ukuran_valid,
               'waktu_iteratif': waktu_iteratif_list,
               'waktu_rekursif': waktu_rekursif_list,
               'waktu_dc': waktu_dc_list
            }
            
      except ValueError:
         st.error("Format input tidak valid. Gunakan format: 1,10,100,1000")

if 'analisis_data' in st.session_state:
   with st.container():
      st.header("Metadata dan Statistik Analisis")
      
      data = st.session_state.analisis_data
      df_metadata = pd.DataFrame({
         'Ukuran Matriks': data['ukuran'],
         'Waktu Iteratif (detik)': [f"{x:.6f}" for x in data['waktu_iteratif']],
         'Waktu Rekursif (detik)': [f"{x:.6f}" if not np.isnan(x) else 'RecursionError' for x in data['waktu_rekursif']],
         'Waktu D&C (detik)': [f"{x:.6f}" if not np.isnan(x) else 'RecursionError' for x in data['waktu_dc']]
      })
      
      st.dataframe(df_metadata, use_container_width=True)
      
      st.subheader("Interpretasi Hasil Analisis")
      
      if 'waktu_iteratif' in locals() and 'waktu_rekursif' in locals() and 'waktu_dc' in locals():
         rata_iter = np.mean([x for x in data['waktu_iteratif'] if not np.isnan(x)])
         rata_rek = np.mean([x for x in data['waktu_rekursif'] if not np.isnan(x)])
         rata_dc = np.mean([x for x in data['waktu_dc'] if not np.isnan(x)])
         
         st.markdown(f"""
         Berdasarkan analisis performa pada {len(data['ukuran'])} variasi ukuran matriks:
         
         1. **Algoritma Iteratif** menunjukkan performa paling stabil dengan waktu eksekusi rata-rata **{rata_iter:.6f} detik**.
         2. **Algoritma Rekursif** mengalami RecursionError pada ukuran matriks tertentu karena batas kedalaman rekursi Python.
         3. **Algoritma Divide & Conquer** memiliki kompleksitas waktu teoretis $\\Theta(n^2)$ dengan overhead rekursi yang signifikan.
         
         **Kesimpulan**: Untuk matriks berukuran besar, algoritma iteratif merupakan pilihan optimal karena:
         - Tidak ada overhead rekursi
         - Kompleksitas ruang konstan
         - Implementasi sederhana dan mudah dioptimasi
         """)
         
         ukuran_tercepat_iter = data['ukuran'][np.argmin(data['waktu_iteratif'])]
         waktu_tercepat_iter = min(data['waktu_iteratif'])
         
         st.markdown(f"""
         **Finding Kritis**:
         - Ukuran matriks dengan eksekusi tercepat untuk algoritma iteratif: **{ukuran_tercepat_iter}×{ukuran_tercepat_iter}** ({waktu_tercepat_iter:.6f} detik)
         - Rasio pertumbuhan waktu mengikuti pola kuadratik sesuai prediksi teoretis
         - Overhead rekursi menjadi faktor pembatas pada algoritma rekursif untuk $n > 1000$
         """)

with st.container():
   st.header("Informasi Teknis")
   col1, col2 = st.columns(2)
   
   with col1:
      st.subheader("Spesifikasi Pengujian")
      st.markdown("""
      - Rentang nilai matriks: 1-1000
      - Seed random: 42 (reproduktibel)
      - Metode pengukuran: time.perf_counter()
      - Batas rekursi Python: 1000
      - Presisi waktu: mikrodetik
      """)
   
   with col2:
      st.subheader("Batasan Implementasi")
      st.markdown("""
      - RecursionError untuk n > ~1000 pada rekursi
      - MemoryError untuk n > ~10000 pada sistem standar
      - Linear scaling untuk algoritma iteratif
      - Quadratic complexity untuk semua algoritma
      """)

st.markdown("---")
st.caption("Analisis Kompleksitas Algoritma - Implementasi untuk Penelitian PhD © 2024")
