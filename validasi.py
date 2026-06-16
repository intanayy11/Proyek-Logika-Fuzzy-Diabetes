import pandas as pd
import numpy as np

from main import inferensi_tsukamoto  

def validasi_sistem():
    try:
        df = pd.read_csv("hasil_pengujian.csv")
    except FileNotFoundError:
        print("[ERROR] File 'hasil_pengujian.csv' tidak ditemukan di folder ini!")
        return

    total_data = len(df)
    selisih_total = 0
    jumlah_cocok = 0
    
    print(f"=== MEMULAI VALIDASI OTOMATIS TSUKAMOTO ({total_data} DATA) ===")
    print("-" * 60)
    
    for index, row in df.iterrows():
        g = float(row['Glucose'])
        b = float(row['BMI'])
        u = float(row['Age'])
        w = float(row['DPF'])
        
        skor_dataset = float(row['Nilai Risiko'])
        
        # Fungsi ini mengembalikan: (skor_akhir, label_kategori, aturan_aktif)
        skor_sistem, _, _ = inferensi_tsukamoto(g, b, u, w, verbose=False)
        
        # Hitung selisih mutlak antara data laporan (CSV) dengan hitungan sistem saat ini
        selisih = abs(skor_dataset - skor_sistem)
        selisih_total += selisih
        
        # Toleransi perbedaan desimal sangat kecil akibat pembulatan (misal: 75.37 vs 75.368)
        if selisih < 0.05:
            jumlah_cocok += 1
            
    rata_rata_selisih = selisih_total / total_data
    persentase_akurasi = (jumlah_cocok / total_data) * 100
    
    print("\n=== HASIL EVALUASI KESESUAIAN ===")
    print(f"• Total Data yang Diuji          : {total_data} pasien")
    print(f"• Jumlah Data yang Sesuai Mutlak : {jumlah_cocok} data")
    print(f"• Rata-rata Selisih Skor (Error) : {rata_rata_selisih:.4f}")
    print(f"• Persentase Akurasi Program     : {persentase_akurasi:.2f}%")
    print("=" * 60)

if __name__ == "__main__":
    validasi_sistem()