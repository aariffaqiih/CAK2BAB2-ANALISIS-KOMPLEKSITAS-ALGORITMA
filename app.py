import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time
import random
import sys

sys.setrecursionlimit(20000)

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
   hasil = func(matriks)
   end = time.perf_counter()
   return hasil, end - start

st.set_page_config(page_title="Iterative vs Recursive Max Matrix", layout="centered")

st.title("Analisis Komputasi Pencarian Nilai Maksimum Matriks")
st.markdown("---")

st.header("Deskripsi Sistem")
st.write("""
Perangkat lunak ini dirancang untuk melakukan evaluasi komparatif terhadap tiga pendekatan algoritma fundamental dalam pencarian nilai ekstrem (maksimum) pada struktur data matriks 2 dimensi. 
Analisis mencakup kompleksitas waktu (Time Complexity) dan analisis perilaku memori (Stack Depth) melalui pendekatan Iteratif, Rekursif Linear, dan Rekursif Divide & Conquer. 
Sistem ini memfasilitasi pengujian empiris dengan generator data stokastik dan visualisasi performa asimtotik.
""")

st.header("Konfigurasi Generator Matriks")

n_input = st.number_input("Tentukan Ordo Matriks (N x N)", min_value=1, value=10, step=1)
use_seed = st.checkbox("Gunakan Seed Deterministik (Reproducibility)", value=True)
seed_val = 42 if use_seed else None

if st.button("Generate Matriks"):
   st.session_state['matriks_utama'] = buat_matriks(n_input, seed_val)
   st.session_state['n_saat_ini'] = n_input
   st.success(f"Matriks berordo {n_input}x{n_input} berhasil digenerate.")

if 'matriks_utama' in st.session_state:
   matriks = st.session_state['matriks_utama']
   n = st.session_state['n_saat_ini']

   st.subheader(f"Visualisasi Data Matriks ({n}x{n})")
   df = pd.DataFrame(matriks)
   st.dataframe(df, use_container_width=True)

   st.info(f"Matriks terdiri dari {n * n} elemen integer yang didistribusikan secara acak uniform [1, 1000].")

   st.header("Eksekusi Algoritma & Hasil Pencarian")

   col1, col2, col3 = st.columns(3)

   hasil_iter, waktu_iter_s = ukur_waktu(iteratif, matriks)
   waktu_iter_ms = waktu_iter_s * 1000

   try:
      hasil_rek, waktu_rek_s = ukur_waktu(rekursif, matriks)
      waktu_rek_ms = waktu_rek_s * 1000
      status_rek = "Sukses"
   except RecursionError:
      hasil_rek = "N/A (Stack Overflow)"
      waktu_rek_ms = 0
      status_rek = "Gagal"
   except Exception:
      hasil_rek = "Error"
      waktu_rek_ms = 0
      status_rek = "Gagal"

   try:
      hasil_dc, waktu_dc_s = ukur_waktu(rekursif_divide_conquer, matriks)
      waktu_dc_ms = waktu_dc_s * 1000
      status_dc = "Sukses"
   except RecursionError:
      hasil_dc = "N/A (Stack Overflow)"
      waktu_dc_ms = 0
      status_dc = "Gagal"
   except Exception:
      hasil_dc = "Error"
      waktu_dc_ms = 0
      status_dc = "Gagal"

   with col1:
      st.markdown("### Pendekatan Iteratif")
      st.metric(label="Nilai Maksimum", value=str(hasil_iter))
      st.metric(label="Waktu Komputasi", value=f"{waktu_iter_ms:.4f} ms")

   with col2:
      st.markdown("### Pendekatan Rekursif")
      st.metric(label="Nilai Maksimum", value=str(hasil_rek))
      st.metric(label="Waktu Komputasi", value=f"{waktu_rek_ms:.4f} ms" if status_rek == "Sukses" else "N/A")
      if status_rek != "Sukses":
         st.error("Recursion Depth Exceeded")

   with col3:
      st.markdown("### Divide & Conquer")
      st.metric(label="Nilai Maksimum", value=str(hasil_dc))
      st.metric(label="Waktu Komputasi", value=f"{waktu_dc_ms:.4f} ms" if status_dc == "Sukses" else "N/A")
      if status_dc != "Sukses":
         st.error("Recursion Depth Exceeded")

   st.header("Landasan Teoretis dan Formalisme Matematika")

   st.markdown("#### 1. Teorema Iteratif")
   st.latex(r"""
   Misalkan A adalah matriks berukuran n \times n. Algoritma iteratif melakukan pemindaian linear elemen demi elemen.
   """)
   st.latex(r"""
   Maks(A) = \max_{0 \le i < n} \left( \max_{0 \le j < n} A[i][j] \right)
   """)
   st.latex(r"""
   Kompleksitas Waktu: T(n) = \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} \mathcal{O}(1) = \mathcal{O}(n^2)
   """)
   st.write("Pendekatan ini menggunakan struktur kontrol loop bersarang, meminimalkan overhead memori stack.")

   st.markdown("#### 2. Teorema Rekursif Linear (Sequential Recursion)")
   st.latex(r"""
   Fungsi didefinisikan sebagai transisi state F(i, j, \mu), di mana \mu adalah maksimum lokal saat ini.
   """)
   st.latex(r"""
   F(i, j, \mu) = 
   \begin{cases} 
   \mu & \text{jika } i \ge n \\
   F(i+1, 0, \mu) & \text{jika } j \ge n \\
   F(i, j+1, \max(\mu, A[i][j])) & \text{lainnya}
   \end{cases}
   """)
   st.write("Karena setiap sel dikunjungi secara sekuensial melalui pemanggilan fungsi, kedalaman rekursi (Stack Depth) berbanding lurus dengan jumlah total elemen.")
   st.latex(r"""
   S(n) = \mathcal{O}(n^2) \quad (\text{Sangat rentan terhadap Stack Overflow})
   """)

   st.markdown("#### 3. Teorema Divide & Conquer (Master Theorem)")
   st.latex(r"""
   Matriks dibagi menjadi 4 sub-kuadran yang sama besar hingga mencapai kasus basis trivial (1 elemen).
   """)
   st.latex(r"""
   T(n) = 4T\left(\frac{n}{2}\right) + \Theta(1)
   """)
   st.write("Menggunakan Teorema Master dengan a=4, b=2, dan d=0:")
   st.latex(r"""
   \log_b a = \log_2 4 = 2. \quad \text{Karena } f(n) = \Theta(1) = O(n^{\log_b a - \epsilon}), \text{ maka } T(n) = \Theta(n^2).
   """)
   st.write("Meski kompleksitas waktu setara iteratif, struktur pohon rekursi memiliki kedalaman logaritmik:")
   st.latex(r"""
   S(n) = \mathcal{O}(\log n)
   """)

st.header("Analisis Skalabilitas Asimtotik")

sizes_str = st.text_input("Masukkan ukuran sampel uji (pisahkan dengan koma)", "10, 20, 30, 40, 50, 60, 70, 80, 90, 100")
if st.button("Jalankan Analisis Komprehensif"):
   try:
      ukuran_list = [int(x.strip()) for x in sizes_str.split(',')]
      ukuran_list.sort()
   except ValueError:
      st.error("Input tidak valid. Harap masukkan angka yang dipisahkan koma.")
      st.stop()

   waktu_iteratif_list = []
   waktu_rekursif_list = []
   waktu_dc_list = []

   depth_iteratif = []
   depth_rekursif = []
   depth_dc = []

   with st.spinner('Melakukan komputasi... Harap tunggu.'):
      progress_bar = st.progress(0)
      for idx, n_val in enumerate(ukuran_list):
         matriks_uji = buat_matriks(n_val, seed=42)

         try:
            _, t = ukur_waktu(iteratif, matriks_uji)
            waktu_iteratif_list.append(t * 1000)
            depth_iteratif.append(1)
         except Exception:
            waktu_iteratif_list.append(None)
            depth_iteratif.append(None)

         try:
            _, t = ukur_waktu(rekursif, matriks_uji)
            waktu_rekursif_list.append(t * 1000)
            depth_rekursif.append(n_val * n_val)
         except RecursionError:
            waktu_rekursif_list.append(None)
            depth_rekursif.append(None)
         except Exception:
            waktu_rekursif_list.append(None)
            depth_rekursif.append(None)

         try:
            _, t = ukur_waktu(rekursif_divide_conquer, matriks_uji)
            waktu_dc_list.append(t * 1000)
            depth_dc.append(np.log2(n_val))
         except RecursionError:
            waktu_dc_list.append(None)
            depth_dc.append(None)
         except Exception:
            waktu_dc_list.append(None)
            depth_dc.append(None)
         
         progress_bar.progress((idx + 1) / len(ukuran_list))

   st.subheader("1. Visualisasi Pertumbuhan Waktu Eksekusi (2D)")

   fig, ax = plt.subplots(figsize=(10, 6))
   ax.plot(ukuran_list, waktu_iteratif_list, label='Iteratif', color='green', marker='o', linewidth=2)
   ax.plot(ukuran_list, waktu_rekursif_list, label='Rekursif Linear', color='blue', marker='s', linewidth=2)
   ax.plot(ukuran_list, waktu_dc_list, label='Rekursif Divide & Conquer', color='orange', marker='^', linewidth=2)

   ax.set_xlabel('Dimensi Matriks (N)')
   ax.set_ylabel('Waktu Eksekusi (milisecond)')
   ax.set_title('Analisis Empiris Kompleksitas Waktu')
   ax.legend()
   ax.grid(True, linestyle='--', alpha=0.6)
   st.pyplot(fig)

   st.subheader("2. Visualisasi Waktu Dinamis Multidimensi (3D - Time)")
   st.caption("Sumbu X: Ukuran Input (N), Sumbu Y: Waktu Eksekusi (ms), Sumbu Z: Algoritma")

   fig_3d = go.Figure()

   fig_3d.add_trace(go.Scatter3d(
      x=ukuran_list, y=[0]*len(ukuran_list), z=waktu_iteratif_list,
      mode='lines+markers', name='Iteratif',
      line=dict(color='green', width=5)
   ))

   fig_3d.add_trace(go.Scatter3d(
      x=ukuran_list, y=[1]*len(ukuran_list), z=waktu_rekursif_list,
      mode='lines+markers', name='Rekursif Linear',
      line=dict(color='blue', width=5)
   ))

   fig_3d.add_trace(go.Scatter3d(
      x=ukuran_list, y=[2]*len(ukuran_list), z=waktu_dc_list,
      mode='lines+markers', name='Divide & Conquer',
      line=dict(color='orange', width=5)
   ))

   fig_3d.update_layout(
      scene=dict(
         xaxis_title='Ukuran Input (N)',
         yaxis_title='ID Algoritma',
         zaxis_title='Waktu (ms)',
         yaxis=dict(tickvals=[0, 1, 2], ticktext=['Iteratif', 'Rekursif', 'D&C'])
      ),
      margin=dict(l=0, r=0, b=0, t=0),
      height=600
   )
   st.plotly_chart(fig_3d, use_container_width=True)

   st.subheader("3. Estimasi Kedalaman Rekursi (Theoretical Stack Depth - 2D)")
   fig_depth, ax_depth = plt.subplots(figsize=(10, 6))

   valid_depth_rec = [d for d in depth_rekursif if d is not None]
   valid_x_rec = [ukuran_list[i] for i, d in enumerate(depth_rekursif) if d is not None]

   ax_depth.plot(ukuran_list, depth_iteratif, label='Iteratif (Constant)', color='green', linewidth=2)
   ax_depth.plot(valid_x_rec, valid_depth_rec, label='Rekursif Linear (Quadratic)', color='blue', linewidth=2)
   ax_depth.plot(ukuran_list, depth_dc, label='Divide & Conquer (Logarithmic)', color='orange', linewidth=2)

   ax_depth.set_yscale('log')
   ax_depth.set_xlabel('Dimensi Matriks (N)')
   ax_depth.set_ylabel('Estimasi Stack Frames (Log Scale)')
   ax_depth.set_title('Perbandingan Penggunaan Stack Memory')
   ax_depth.legend()
   ax_depth.grid(True, linestyle='--', alpha=0.6)
   st.pyplot(fig_depth)

   st.subheader("4. Estimasi Kedalaman Rekursi Dinamis (3D - Stack Depth)")
   st.caption("Visualisasi 3D untuk membandingkan penggunaan memori stack antar algoritma.")

   fig_3d_depth = go.Figure()

   fig_3d_depth.add_trace(go.Scatter3d(
      x=ukuran_list, y=[0]*len(ukuran_list), z=depth_iteratif,
      mode='lines+markers', name='Iteratif (Constant)',
      line=dict(color='green', width=5)
   ))

   fig_3d_depth.add_trace(go.Scatter3d(
      x=ukuran_list, y=[1]*len(ukuran_list), z=depth_rekursif,
      mode='lines+markers', name='Rekursif Linear (N^2)',
      line=dict(color='blue', width=5)
   ))

   fig_3d_depth.add_trace(go.Scatter3d(
      x=ukuran_list, y=[2]*len(ukuran_list), z=depth_dc,
      mode='lines+markers', name='Divide & Conquer (Log N)',
      line=dict(color='orange', width=5)
   ))

   fig_3d_depth.update_layout(
      scene=dict(
         xaxis_title='Ukuran Input (N)',
         yaxis_title='ID Algoritma',
         zaxis_title='Stack Depth (Frames)',
         zaxis_type='log',
         yaxis=dict(tickvals=[0, 1, 2], ticktext=['Iteratif', 'Rekursif', 'D&C'])
      ),
      margin=dict(l=0, r=0, b=0, t=0),
      height=600
   )
   st.plotly_chart(fig_3d_depth, use_container_width=True)

   st.header("Meta-Analisis Hasil Eksperimen")

   valid_iter = [x for x in waktu_iteratif_list if x is not None]
   valid_rek = [x for x in waktu_rekursif_list if x is not None]
   valid_dc = [x for x in waktu_dc_list if x is not None]

   avg_iter = sum(valid_iter)/len(valid_iter) if valid_iter else 0
   avg_dc = sum(valid_dc)/len(valid_dc) if valid_dc else 0

   limit_n_rek = ukuran_list[len(valid_rek)-1] if valid_rek else 0

   analisis_text = f"""
   Berdasarkan metadata eksperimental yang telah dikumpulkan, terlihat pola kinerja yang signifikan. 
   Algoritma **Iteratif** menunjukkan stabilitas tertinggi dengan rata-rata waktu eksekusi pada sampel valid sebesar **{avg_iter:.6f} ms**. 
   Hal ini konsisten dengan teori bahwa overhead pemanggilan fungsi pada Python sangat mempengaruhi kinerja.

   Algoritma **Rekursif Linear** mengalami kegagalan (Stack Overflow) setelah ukuran input N melampaui **{limit_n_rek}**. 
   Ini mengonfirmasi teorema $S(n) = O(n^2)$, di mana kedalaman tumpukan memori tumbuh secara kuadratik terhadap sisi matriks, 
   dengan cepat menghabiskan batas rekursi standar interpreter.

   Algoritma **Divide & Conquer** menunjukkan performa yang lebih lambat dibandingkan Iteratif namun jauh lebih stabil dibandingkan Rekursif Linear 
   dari sisi memori. Rata-rata waktu eksekusi adalah **{avg_dc:.6f} ms**. Struktur pohon rekursi logaritmik terbukti efektif mencegah 
   Stack Overflow pada ukuran input yang lebih besar, meskipun overhead pemecahan masalah (dividing) masih membebani waktu eksekusi total.
   """

   st.markdown(analisis_text)

   st.markdown("---")
   st.header("5. Tabulasi Data Eksperimental & Metrik Kinerja")
   st.caption("Tabel berikut menyajikan data mentah dengan presisi tinggi beserta rasio degradasi kinerja relatif terhadap pendekatan Iteratif.")

   data_final = []
   for i, n in enumerate(ukuran_list):
      t_iter = waktu_iteratif_list[i]
      t_rec = waktu_rekursif_list[i]
      t_dc = waktu_dc_list[i]

      ratio_rec = (t_rec / t_iter) if (t_rec is not None and t_iter is not None and t_iter > 0) else None
      ratio_dc = (t_dc / t_iter) if (t_dc is not None and t_iter is not None and t_iter > 0) else None

      row = {
         "Ordo (N)": n,
         "Complexity Space (N^2)": n * n,
         "T_Iteratif (ms)": t_iter,
         "T_Rekursif (ms)": t_rec,
         "Δ_Rekursif (x Baseline)": ratio_rec,
         "T_DivideConquer (ms)": t_dc,
         "Δ_DC (x Baseline)": ratio_dc,
         "Status Memori": "SAFE" if t_rec is not None else "CRITICAL (Stack Overflow)"
      }
      data_final.append(row)

   df_results = pd.DataFrame(data_final)

   def highlight_status(val):
      color = '#ff4b4b' if 'CRITICAL' in str(val) else '#09ab3b'
      return f'color: {color}; font-weight: bold'

   st.dataframe(
      df_results.style.map(highlight_status, subset=['Status Memori']),
      column_config={
         "Ordo (N)": st.column_config.NumberColumn("Input Size (N)", help="Panjang sisi matriks persegi", format="%d"),
         "Complexity Space (N^2)": st.column_config.NumberColumn("Total Elements", help="Total ruang pencarian (N*N)", format="%d"),
         "T_Iteratif (ms)": st.column_config.NumberColumn("Iteratif Time", help="Waktu eksekusi pendekatan Iteratif (Baseline)", format="%.4f ms"),
         "T_Rekursif (ms)": st.column_config.NumberColumn("Recursive Time", help="Waktu eksekusi pendekatan Rekursif Linear", format="%.4f ms"),
         "Δ_Rekursif (x Baseline)": st.column_config.NumberColumn("Rec. Slowdown", help="Faktor perlambatan dibanding Iteratif", format="%.2f x"),
         "T_DivideConquer (ms)": st.column_config.NumberColumn("D&C Time", help="Waktu eksekusi pendekatan Divide & Conquer", format="%.4f ms"),
         "Δ_DC (x Baseline)": st.column_config.NumberColumn("D&C Slowdown", help="Faktor perlambatan D&C dibanding Iteratif", format="%.2f x"),
         "Status Memori": st.column_config.TextColumn("System Integrity", help="Status integritas stack memori selama eksekusi", width="medium")
      },
      use_container_width=True,
      hide_index=True
   )

   st.info("Catatan: Waktu ditampilkan dalam milidetik (ms). Kolom 'Slowdown' menunjukkan berapa kali lipat lebih lambat algoritma tersebut dibandingkan Iteratif.")

st.markdown("---")
st.header("Identitas Kelompok")

data_kelompok = [
    {"NIM": "103112430267", "Nama": "Raden Aurel Aditya Kusumawaningyun"},
    {"NIM": "103112430182", "Nama": "'Aarif Rahmaan Jalaluddin Faqiih"},
    {"NIM": "103112430185", "Nama": "Atha Muyassar"},
]

df_kelompok = pd.DataFrame(data_kelompok)

st.dataframe(
    df_kelompok,
    column_config={
        "NIM": st.column_config.TextColumn("NIM", width="medium"),
        "Nama": st.column_config.TextColumn("Nama Lengkap", width="large"),
    },
    hide_index=True,
    use_container_width=True
)

st.caption("CAK2BAB2-S1IF-12-07 / Analisis Kompleksitas Algoritma")
