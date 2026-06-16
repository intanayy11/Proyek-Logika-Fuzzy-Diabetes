# Sistem Pendukung Keputusan Penentuan Risiko Diabetes Menggunakan Metode Fuzzy Tsukamoto

Aplikasi ini merupakan sistem pendukung keputusan (SPK) berbasis desktop yang dirancang untuk memprediksi tingkat risiko diabetes pada pasien. Logika perhitungan didasarkan pada metode Fuzzy Tsukamoto dengan mengacu pada dataset riil Pima Indians Diabetes Database dari Kaggle.

Sistem ini dikembangkan sebagai Proyek Akhir Mata Kuliah Logika Fuzzy (Semester 4) oleh Kelompok 6.

## Anggota Tim dan Pembagian Tugas
1. **Ian** - Pengumpulan Data dan Penentuan Variabel Fuzzy
2. **Haydar** - Perancangan Fungsi Keanggotaan (Membership Function)
3. **Yusuf** - Penyusunan Basis Aturan (81 Rule Base)
4. **Wati** - Perhitungan Inferensi dan Validasi Manual
5. **Intan** - Implementasi Pemrograman dan Antarmuka Grafis (GUI)
6. **Nadin** - Analisis Hasil Eksperimen dan Penyusunan Artikel Ilmiah

---

## Fitur Utama Aplikasi
* **Mesin Inferensi Tsukamoto:** Pemrosesan logika fuzzy yang sinkron secara matematis antara hitungan sistem dengan hitungan manual.
* **Antarmuka Grafis (GUI) Interaktif:** Dibuat menggunakan pustaka Tkinter untuk mempermudah input data medis pasien secara real-time.
* **Visualisasi Kurva Dinamis:** Mengintegrasikan grafik Matplotlib ke dalam GUI untuk menampilkan posisi skor defuzzifikasi pada kurva risiko secara langsung.
* **Tabel Analisis Aturan Aktif:** Menampilkan daftar aturan (rules) yang aktif beserta nilai alpha-predikat dan nilai z individual untuk setiap proses komputasi.
* **Skrip Validasi Otomatis:** Menyediakan fitur pengujian massal untuk mencocokkan akurasi program terhadap ratusan data uji secara instan.

---

## Spesifikasi Variabel Fuzzy

### Variabel Input
1. **Glucose (Kadar Glukosa Darah)**
   * Rendah: 0 - 100 mg/dL
   * Normal: 70 - 140 mg/dL
   * Tinggi: 110 - 200+ mg/dL

2. **BMI (Indeks Massa Tubuh)**
   * Kurus: 0 - 22 kg/m²
   * Normal: 18 - 30 kg/m²
   * Obesitas: 27 - 50+ kg/m²

3. **Age (Usia Pasien)**
   * Muda: 18 - 35 tahun
   * Paruh Baya: 30 - 55 tahun
   * Tua: 50 - 80+ tahun

4. **DPF (Diabetes Pedigree Function / Riwayat Genetik)**
   * Rendah: 0.0 - 0.5
   * Sedang: 0.3 - 0.8
   * Tinggi: 0.7 - 2.5

### Variabel Output
* **Skor Risiko Diabetes** (Skala 0 - 100)
  * Kurva Risiko Rendah (Monoton Turun)
  * Kurva Risiko Tinggi (Monoton Naik)

Total kombinasi aturan yang diterapkan pada sistem ini adalah 81 aturan (3 x 3 x 3 x 3).

---

## Hasil Pengujian dan Akurasi Sistem
Berdasarkan pengujian otomatis menggunakan skrip validasi terhadap keseluruhan dataset yang berjumlah 768 data pasien, sistem ini menunjukkan performa komputasi sebagai berikut:

* **Total Data yang Diuji:** 768 pasien
* **Jumlah Data Sesuai Mutlak:** 759 data
* **Rata-rata Selisih Skor (Mean Absolute Error):** 0.7682
* **Persentase Kesesuaian Sistem:** 98.83%

Selisih kecil sebesar 1.17% disebabkan oleh variasi pembulatan angka desimal (floating-point precision) antara spreadsheet data pengujian dengan bahasa pemrograman Python, sehingga sistem dinyatakan sangat valid dan konsisten.

---

## Persyaratan Sistem (Prerequisites)
Sebelum menjalankan aplikasi, pastikan Anda telah memasang Python (versi 3.10 ke atas direkomendasikan) beserta pustaka pendukung berikut:

* NumPy
* Pandas
* Matplotlib

Pustaka Tkinter umumnya sudah terpasang secara bawaan bersamaan dengan instalasi Python. Jika belum tersedia, Anda dapat memasang dependensi di atas melalui pip:

```bash
pip install numpy pandas matplotlib