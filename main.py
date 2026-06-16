import os
os.environ["PYTHONIOENCODING"] = "utf-8"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------------------------------------------
# FUNGSI KEANGGOTAAN (Membership Functions)
# ----------------------------------------------------------

def mf_glukosa_rendah(x):
    """Trapesium Kiri: 1 jika x<=70, turun linear 70-100, 0 jika x>100"""
    if x <= 70:
        return 1.0
    elif x <= 100:
        return (100 - x) / (100 - 70)
    return 0.0

def mf_glukosa_normal(x):
    """Segitiga: naik 70-105, turun 105-140"""
    if x <= 70 or x >= 140:
        return 0.0
    elif x <= 105:
        return (x - 70) / (105 - 70)
    else:
        return (140 - x) / (140 - 105)

def mf_glukosa_tinggi(x):
    """Trapesium Kanan: 0 jika x<=110, naik 110-140, 1 jika x>140"""
    if x <= 110:
        return 0.0
    elif x <= 140:
        return (x - 110) / (140 - 110)
    return 1.0

def mf_bmi_kurus(y):
    """Trapesium Kiri: 1 jika y<=18, turun 18-22, 0 jika y>22"""
    if y <= 18:
        return 1.0
    elif y <= 22:
        return (22 - y) / (22 - 18)
    return 0.0

def mf_bmi_normal(y):
    """Segitiga: naik 18-24, turun 24-30"""
    if y <= 18 or y >= 30:
        return 0.0
    elif y <= 24:
        return (y - 18) / (24 - 18)
    else:
        return (30 - y) / (30 - 24)

def mf_bmi_obesitas(y):
    """Trapesium Kanan: 0 jika y<=27, naik 27-30, 1 jika y>30"""
    if y <= 27:
        return 0.0
    elif y <= 30:
        return (y - 27) / (30 - 27)
    return 1.0

def mf_usia_muda(z):
    """Trapesium Kiri: 1 jika z<=30, turun 30-35, 0 jika z>35"""
    if z <= 30:
        return 1.0
    elif z <= 35:
        return (35 - z) / (35 - 30)
    return 0.0

def mf_usia_paruhbaya(z):
    """Segitiga: naik 30-42.5, turun 42.5-55"""
    if z <= 30 or z >= 55:
        return 0.0
    elif z <= 42.5:
        return (z - 30) / (42.5 - 30)
    else:
        return (55 - z) / (55 - 42.5)

def mf_usia_tua(z):
    """Trapesium Kanan: 0 jika z<=50, naik 50-55, 1 jika z>55"""
    if z <= 50:
        return 0.0
    elif z <= 55:
        return (z - 50) / (55 - 50)
    return 1.0

def mf_genetik_rendah(w):
    """Trapesium Kiri: 1 jika w<=0.3, turun 0.3-0.5, 0 jika w>0.5"""
    if w <= 0.3:
        return 1.0
    elif w <= 0.5:
        return (0.5 - w) / (0.5 - 0.3)
    return 0.0

def mf_genetik_sedang(w):
    """Segitiga: naik 0.3-0.55, turun 0.55-0.8"""
    if w <= 0.3 or w >= 0.8:
        return 0.0
    elif w <= 0.55:
        return (w - 0.3) / (0.55 - 0.3)
    else:
        return (0.8 - w) / (0.8 - 0.55)

def mf_genetik_tinggi(w):
    """Trapesium Kanan: 0 jika w<=0.7, naik 0.7-0.8, 1 jika w>0.8"""
    if w <= 0.7:
        return 0.0
    elif w <= 0.8:
        return (w - 0.7) / (0.8 - 0.7)
    return 1.0

# ----------------------------------------------------------
# INVERS FUNGSI OUTPUT (Tsukamoto)
# ----------------------------------------------------------

def invers_rendah(alpha):
    """muRendah(r) = (50-r)/50  ->  r = 50 - 50*alpha"""
    if alpha >= 1.0:
        return 0.0
    if alpha <= 0.0:
        return 50.0
    return 50.0 - 50.0 * alpha

def invers_tinggi(alpha):
    """muTinggi(r) = (r-50)/50  ->  r = 50 + 50*alpha"""
    if alpha >= 1.0:
        return 100.0
    if alpha <= 0.0:
        return 50.0
    return 50.0 + 50.0 * alpha

# ----------------------------------------------------------
# RULE BASE (Total ada 81 Rules - Metode Tsukamoto)
# ----------------------------------------------------------

RULES = [
    # (Glukosa,    BMI,       Usia,        Genetik,   Output)
    ("Rendah",  "Kurus",    "Muda",       "Rendah",  "Rendah"),   # R1
    ("Rendah",  "Kurus",    "Muda",       "Sedang",  "Rendah"),   # R2
    ("Rendah",  "Kurus",    "Muda",       "Tinggi",  "Rendah"),   # R3
    ("Rendah",  "Kurus",    "ParuhBaya",  "Rendah",  "Rendah"),   # R4
    ("Rendah",  "Kurus",    "ParuhBaya",  "Sedang",  "Rendah"),   # R5
    ("Rendah",  "Kurus",    "ParuhBaya",  "Tinggi",  "Rendah"),   # R6
    ("Rendah",  "Kurus",    "Tua",        "Rendah",  "Rendah"),   # R7
    ("Rendah",  "Kurus",    "Tua",        "Sedang",  "Rendah"),   # R8
    ("Rendah",  "Kurus",    "Tua",        "Tinggi",  "Rendah"),   # R9
    ("Rendah",  "Normal",   "Muda",       "Rendah",  "Rendah"),   # R10
    ("Rendah",  "Normal",   "Muda",       "Sedang",  "Rendah"),   # R11
    ("Rendah",  "Normal",   "Muda",       "Tinggi",  "Rendah"),   # R12
    ("Rendah",  "Normal",   "ParuhBaya",  "Rendah",  "Rendah"),   # R13
    ("Rendah",  "Normal",   "ParuhBaya",  "Sedang",  "Rendah"),   # R14
    ("Rendah",  "Normal",   "ParuhBaya",  "Tinggi",  "Rendah"),   # R15
    ("Rendah",  "Normal",   "Tua",        "Rendah",  "Rendah"),   # R16
    ("Rendah",  "Normal",   "Tua",        "Sedang",  "Rendah"),   # R17
    ("Rendah",  "Normal",   "Tua",        "Tinggi",  "Tinggi"),   # R18
    ("Rendah",  "Obesitas", "Muda",       "Rendah",  "Rendah"),   # R19
    ("Rendah",  "Obesitas", "Muda",       "Sedang",  "Rendah"),   # R20
    ("Rendah",  "Obesitas", "Muda",       "Tinggi",  "Tinggi"),   # R21
    ("Rendah",  "Obesitas", "ParuhBaya",  "Rendah",  "Rendah"),   # R22
    ("Rendah",  "Obesitas", "ParuhBaya",  "Sedang",  "Tinggi"),   # R23
    ("Rendah",  "Obesitas", "ParuhBaya",  "Tinggi",  "Tinggi"),   # R24
    ("Rendah",  "Obesitas", "Tua",        "Rendah",  "Tinggi"),   # R25
    ("Rendah",  "Obesitas", "Tua",        "Sedang",  "Tinggi"),   # R26
    ("Rendah",  "Obesitas", "Tua",        "Tinggi",  "Tinggi"),   # R27
    ("Normal",  "Kurus",    "Muda",       "Rendah",  "Rendah"),   # R28
    ("Normal",  "Kurus",    "Muda",       "Sedang",  "Rendah"),   # R29
    ("Normal",  "Kurus",    "Muda",       "Tinggi",  "Rendah"),   # R30
    ("Normal",  "Kurus",    "ParuhBaya",  "Rendah",  "Rendah"),   # R31
    ("Normal",  "Kurus",    "ParuhBaya",  "Sedang",  "Rendah"),   # R32
    ("Normal",  "Kurus",    "ParuhBaya",  "Tinggi",  "Rendah"),   # R33
    ("Normal",  "Kurus",    "Tua",        "Rendah",  "Rendah"),   # R34
    ("Normal",  "Kurus",    "Tua",        "Sedang",  "Rendah"),   # R35
    ("Normal",  "Kurus",    "Tua",        "Tinggi",  "Rendah"),   # R36
    ("Normal",  "Normal",   "Muda",       "Rendah",  "Rendah"),   # R37
    ("Normal",  "Normal",   "Muda",       "Sedang",  "Rendah"),   # R38
    ("Normal",  "Normal",   "Muda",       "Tinggi",  "Rendah"),   # R39
    ("Normal",  "Normal",   "ParuhBaya",  "Rendah",  "Rendah"),   # R40
    ("Normal",  "Normal",   "ParuhBaya",  "Sedang",  "Rendah"),   # R41
    ("Normal",  "Normal",   "ParuhBaya",  "Tinggi",  "Tinggi"),   # R42
    ("Normal",  "Normal",   "Tua",        "Rendah",  "Rendah"),   # R43
    ("Normal",  "Normal",   "Tua",        "Sedang",  "Tinggi"),   # R44
    ("Normal",  "Normal",   "Tua",        "Tinggi",  "Tinggi"),   # R45
    ("Normal",  "Obesitas", "Muda",       "Rendah",  "Rendah"),   # R46
    ("Normal",  "Obesitas", "Muda",       "Sedang",  "Rendah"),   # R47
    ("Normal",  "Obesitas", "Muda",       "Tinggi",  "Tinggi"),   # R48
    ("Normal",  "Obesitas", "ParuhBaya",  "Rendah",  "Tinggi"),   # R49
    ("Normal",  "Obesitas", "ParuhBaya",  "Sedang",  "Tinggi"),   # R50
    ("Normal",  "Obesitas", "ParuhBaya",  "Tinggi",  "Tinggi"),   # R51
    ("Normal",  "Obesitas", "Tua",        "Rendah",  "Tinggi"),   # R52
    ("Normal",  "Obesitas", "Tua",        "Sedang",  "Tinggi"),   # R53
    ("Normal",  "Obesitas", "Tua",        "Tinggi",  "Tinggi"),   # R54
    ("Tinggi",  "Kurus",    "Muda",       "Rendah",  "Rendah"),   # R55
    ("Tinggi",  "Kurus",    "Muda",       "Sedang",  "Tinggi"),   # R56
    ("Tinggi",  "Kurus",    "Muda",       "Tinggi",  "Tinggi"),   # R57
    ("Tinggi",  "Kurus",    "ParuhBaya",  "Rendah",  "Tinggi"),   # R58
    ("Tinggi",  "Kurus",    "ParuhBaya",  "Sedang",  "Tinggi"),   # R59
    ("Tinggi",  "Kurus",    "ParuhBaya",  "Tinggi",  "Tinggi"),   # R60
    ("Tinggi",  "Kurus",    "Tua",        "Rendah",  "Tinggi"),   # R61
    ("Tinggi",  "Kurus",    "Tua",        "Sedang",  "Tinggi"),   # R62
    ("Tinggi",  "Kurus",    "Tua",        "Tinggi",  "Tinggi"),   # R63
    ("Tinggi",  "Normal",   "Muda",       "Rendah",  "Rendah"),   # R64
    ("Tinggi",  "Normal",   "Muda",       "Sedang",  "Tinggi"),   # R65
    ("Tinggi",  "Normal",   "Muda",       "Tinggi",  "Tinggi"),   # R66
    ("Tinggi",  "Normal",   "ParuhBaya",  "Rendah",  "Tinggi"),   # R67
    ("Tinggi",  "Normal",   "ParuhBaya",  "Sedang",  "Tinggi"),   # R68
    ("Tinggi",  "Normal",   "ParuhBaya",  "Tinggi",  "Tinggi"),   # R69
    ("Tinggi",  "Normal",   "Tua",        "Rendah",  "Tinggi"),   # R70
    ("Tinggi",  "Normal",   "Tua",        "Sedang",  "Tinggi"),   # R71
    ("Tinggi",  "Normal",   "Tua",        "Tinggi",  "Tinggi"),   # R72
    ("Tinggi",  "Obesitas", "Muda",       "Rendah",  "Tinggi"),   # R73
    ("Tinggi",  "Obesitas", "Muda",       "Sedang",  "Tinggi"),   # R74
    ("Tinggi",  "Obesitas", "Muda",       "Tinggi",  "Tinggi"),   # R75
    ("Tinggi",  "Obesitas", "ParuhBaya",  "Rendah",  "Tinggi"),   # R76
    ("Tinggi",  "Obesitas", "ParuhBaya",  "Sedang",  "Tinggi"),   # R77
    ("Tinggi",  "Obesitas", "ParuhBaya",  "Tinggi",  "Tinggi"),   # R78
    ("Tinggi",  "Obesitas", "Tua",        "Rendah",  "Tinggi"),   # R79
    ("Tinggi",  "Obesitas", "Tua",        "Sedang",  "Tinggi"),   # R80
    ("Tinggi",  "Obesitas", "Tua",        "Tinggi",  "Tinggi"),   # R81
]

# ----------------------------------------------------------
# INFERENSI TSUKAMOTO
# ----------------------------------------------------------

MF_GLUKOSA = {
    "Rendah":  mf_glukosa_rendah,
    "Normal":  mf_glukosa_normal,
    "Tinggi":  mf_glukosa_tinggi,
}
MF_BMI = {
    "Kurus":    mf_bmi_kurus,
    "Normal":   mf_bmi_normal,
    "Obesitas": mf_bmi_obesitas,
}
MF_USIA = {
    "Muda":      mf_usia_muda,
    "ParuhBaya": mf_usia_paruhbaya,
    "Tua":       mf_usia_tua,
}
MF_GENETIK = {
    "Rendah": mf_genetik_rendah,
    "Sedang": mf_genetik_sedang,
    "Tinggi": mf_genetik_tinggi,
}
INVERS_OUTPUT = {
    "Rendah": invers_rendah,
    "Tinggi": invers_tinggi,
}

def inferensi_tsukamoto(glukosa, bmi, usia, genetik, verbose=False):
    """
    Hitung risiko diabetes dengan metode Tsukamoto.
    Mengembalikan: (skor_risiko, label_risiko, detail_rules_aktif)
    """
    numerator   = 0.0
    denominator = 0.0
    aktif = []

    for i, (rg, rb, ru, rw, out) in enumerate(RULES):
        mu_g = MF_GLUKOSA[rg](glukosa)
        mu_b = MF_BMI[rb](bmi)
        mu_u = MF_USIA[ru](usia)
        mu_w = MF_GENETIK[rw](genetik)

        alpha = min(mu_g, mu_b, mu_u, mu_w)   # operator AND = min

        if alpha > 0:
            z_i = INVERS_OUTPUT[out](alpha)
            numerator   += alpha * z_i
            denominator += alpha
            aktif.append((i+1, rg, rb, ru, rw, out, round(alpha, 4), round(z_i, 2)))

    if denominator == 0:
        skor = 50.0  # default jika tidak ada rule aktif
    else:
        skor = numerator / denominator

    label = "TINGGI" if skor >= 50 else "RENDAH"

    return skor, label, aktif

# ----------------------------------------------------------
# VISUALISASI MEMBERSHIP FUNCTION
# ----------------------------------------------------------

def plot_membership_functions(glukosa=None, bmi=None, usia=None, genetik=None, skor=None, label=None, show=True):
    """
    Tampilkan grafik membership function. Saat input kosong, grafik umum tetap
    tampil tanpa marker, arsiran, dan panel hasil.
    """
    fig = plt.figure(figsize=(15.4, 8.7), dpi=95)
    fig.suptitle("Sistem Fuzzy Tsukamoto - Penentuan Risiko Diabetes",
                 fontsize=12.5, fontweight='bold', y=0.975)
    fig.subplots_adjust(left=0.055, right=0.985, bottom=0.075, top=0.905,
                        wspace=0.18, hspace=0.55)

    grid = fig.add_gridspec(2, 3, width_ratios=[1, 1, 1.05])
    ax1 = fig.add_subplot(grid[0, 0])
    ax2 = fig.add_subplot(grid[0, 1])
    ax3 = fig.add_subplot(grid[1, 0])
    ax4 = fig.add_subplot(grid[1, 1])
    ax5 = fig.add_subplot(grid[0, 2])
    ax6 = fig.add_subplot(grid[1, 2])

    def draw_input_marker(ax, xs, curves, value, funcs, colors):
        ax.axvline(value, color='black', lw=1.8, ls='--', label=f'Input = {value:g}')
        for ys, fn, color in zip(curves, funcs, colors):
            mu = fn(value)
            if mu > 0:
                ax.fill_between(xs, 0, np.minimum(ys, mu), color=color, alpha=0.13, linewidth=0)
                ax.hlines(mu, xs.min(), value, color=color, lw=1, ls=':', alpha=0.7)
                ax.plot(value, mu, 'o', color=color, ms=5.5, zorder=5)

    def polish_axis(ax, title, xlabel):
        ax.set_title(title, fontweight='bold', fontsize=10, pad=6)
        ax.set_xlabel(xlabel, fontsize=8.5, labelpad=3)
        ax.set_ylabel('Derajat Keanggotaan (mu)', fontsize=8.5, labelpad=3)
        ax.tick_params(labelsize=8)
        ax.legend(fontsize=7, loc="best", framealpha=0.86)
        ax.set_ylim(-0.05, 1.15)
        ax.grid(alpha=0.26)

    x = np.linspace(0, 210, 400)
    g_curves = [
        np.array([mf_glukosa_rendah(v) for v in x]),
        np.array([mf_glukosa_normal(v) for v in x]),
        np.array([mf_glukosa_tinggi(v) for v in x]),
    ]
    for curve, color, name in zip(g_curves, ['blue', 'green', 'red'], ['Rendah', 'Normal', 'Tinggi']):
        ax1.plot(x, curve, color=color, lw=2, label=name)
    if glukosa is not None:
        draw_input_marker(ax1, x, g_curves, glukosa,
                          [mf_glukosa_rendah, mf_glukosa_normal, mf_glukosa_tinggi],
                          ['blue', 'green', 'red'])
    polish_axis(ax1, 'Input 1: Glukosa (mg/dL)', 'mg/dL')

    y = np.linspace(0, 55, 400)
    b_curves = [
        np.array([mf_bmi_kurus(v) for v in y]),
        np.array([mf_bmi_normal(v) for v in y]),
        np.array([mf_bmi_obesitas(v) for v in y]),
    ]
    for curve, color, name in zip(b_curves, ['blue', 'green', 'red'], ['Kurus', 'Normal', 'Obesitas']):
        ax2.plot(y, curve, color=color, lw=2, label=name)
    if bmi is not None:
        draw_input_marker(ax2, y, b_curves, bmi,
                          [mf_bmi_kurus, mf_bmi_normal, mf_bmi_obesitas],
                          ['blue', 'green', 'red'])
    polish_axis(ax2, 'Input 2: BMI (kg/m2)', 'kg/m2')

    z = np.linspace(15, 90, 400)
    u_curves = [
        np.array([mf_usia_muda(v) for v in z]),
        np.array([mf_usia_paruhbaya(v) for v in z]),
        np.array([mf_usia_tua(v) for v in z]),
    ]
    for curve, color, name in zip(u_curves, ['blue', 'green', 'red'], ['Muda', 'Paruh Baya', 'Tua']):
        ax3.plot(z, curve, color=color, lw=2, label=name)
    if usia is not None:
        draw_input_marker(ax3, z, u_curves, usia,
                          [mf_usia_muda, mf_usia_paruhbaya, mf_usia_tua],
                          ['blue', 'green', 'red'])
    polish_axis(ax3, 'Input 3: Usia (tahun)', 'Tahun')

    w = np.linspace(0, 2.6, 400)
    d_curves = [
        np.array([mf_genetik_rendah(v) for v in w]),
        np.array([mf_genetik_sedang(v) for v in w]),
        np.array([mf_genetik_tinggi(v) for v in w]),
    ]
    for curve, color, name in zip(d_curves, ['blue', 'green', 'red'], ['Rendah', 'Sedang', 'Tinggi']):
        ax4.plot(w, curve, color=color, lw=2, label=name)
    if genetik is not None:
        draw_input_marker(ax4, w, d_curves, genetik,
                          [mf_genetik_rendah, mf_genetik_sedang, mf_genetik_tinggi],
                          ['blue', 'green', 'red'])
    polish_axis(ax4, 'Input 4: Riwayat Genetik (DPF)', 'Nilai DPF')

    r = np.linspace(0, 100, 400)
    mu_rendah = np.array([(50 - v) / 50 if 0 <= v <= 50 else (1.0 if v < 0 else 0.0) for v in r])
    mu_tinggi = np.array([(v - 50) / 50 if 50 <= v <= 100 else (0.0 if v < 50 else 1.0) for v in r])
    ax5.axvspan(0, 50, color='blue', alpha=0.04)
    ax5.axvspan(50, 100, color='red', alpha=0.04)
    ax5.plot(r, mu_rendah, color='blue', lw=2.2, label='Rendah')
    ax5.plot(r, mu_tinggi, color='red', lw=2.2, label='Tinggi')
    ax5.axvline(50, color='gray', lw=1, ls=':', alpha=0.7)
    if skor is not None:
        warna_skor = '#e74c3c' if label == 'TINGGI' else '#16a34a'
        selected_curve = mu_tinggi if label == 'TINGGI' else mu_rendah
        selected_mu = (skor - 50) / 50 if label == 'TINGGI' else (50 - skor) / 50
        selected_mu = max(0, min(1, selected_mu))
        mask = (r >= min(50, skor)) & (r <= max(50, skor))
        ax5.fill_between(r[mask], 0, np.minimum(selected_curve[mask], selected_mu),
                         color=warna_skor, alpha=0.18, linewidth=0)
        ax5.axvline(skor, color=warna_skor, lw=2.1, ls='--', label=f'Hasil = {skor:.1f}')
        ax5.hlines(selected_mu, 0, skor, color=warna_skor, lw=1, ls=':', alpha=0.75)
        ax5.plot(skor, selected_mu, 'o', color=warna_skor, ms=7, zorder=6, label=f'mu = {selected_mu:.3f}')
    polish_axis(ax5, 'Output: Risiko Diabetes', 'Skor Risiko (0-100)')

    ax6.axis('off')
    if skor is not None and label is not None:
        from matplotlib.patches import FancyBboxPatch
        warna_box = '#fee2e2' if label == 'TINGGI' else '#dcfce7'
        warna_teks = '#b91c1c' if label == 'TINGGI' else '#15803d'
        ax6.set_facecolor('#fff7f7' if label == 'TINGGI' else '#f7fff9')
        ax6.patch.set_visible(True)
        box = FancyBboxPatch((0.08, 0.08), 0.84, 0.28, boxstyle="round,pad=0.025",
                             facecolor=warna_box, edgecolor=warna_teks, lw=1.8,
                             transform=ax6.transAxes)
        ax6.add_patch(box)
        ax6.text(0.5, 0.88, "RINGKASAN HASIL", transform=ax6.transAxes,
                 fontsize=11.5, color='black', fontweight='bold', ha='center', va='center')
        for ypos, teks in zip(
            [0.74, 0.64, 0.54, 0.44],
            [f"Glukosa : {glukosa:g} mg/dL", f"BMI     : {bmi:g} kg/m2",
             f"Usia    : {usia:g} tahun", f"DPF     : {genetik:g}"]
        ):
            ax6.text(0.5, ypos, teks, transform=ax6.transAxes,
                     fontsize=9.7, color='black', ha='center', va='center')
        ax6.text(0.5, 0.265, f"Skor Risiko: {skor:.2f} / 100",
                 transform=ax6.transAxes, fontsize=10.2, color=warna_teks,
                 fontweight='bold', ha='center', va='center')
        ax6.text(0.5, 0.155, f"Hasil: Risiko {label}",
                 transform=ax6.transAxes, fontsize=11.7, color=warna_teks,
                 fontweight='bold', ha='center', va='center')
    else:
        ax6.text(0.5, 0.58, 'Grafik Membership Function',
                 transform=ax6.transAxes, fontsize=11, fontweight='bold',
                 ha='center', va='center', color='#334155')
        ax6.text(0.5, 0.45, 'Isi semua input lalu klik Hitung Risiko',
                 transform=ax6.transAxes, fontsize=9.5,
                 ha='center', va='center', color='#64748b')

    if show:
        plt.show()
    return fig

def plot_output_mf():
    """Versi standalone grafik output saja (dipakai menu 4)."""
    fig, ax = plt.subplots(figsize=(8, 4))
    r = np.linspace(0, 100, 400)
    ax.plot(r, [(50 - v)/50 if 0 <= v <= 50 else (1.0 if v < 0 else 0.0) for v in r],
            'b-', lw=2.5, label='Rendah (Monoton Turun)')
    ax.plot(r, [(v - 50)/50 if 50 <= v <= 100 else (0.0 if v < 50 else 1.0) for v in r],
            'r-', lw=2.5, label='Tinggi (Monoton Naik)')
    ax.axvline(50, color='gray', lw=1, ls=':', alpha=0.7, label='Batas (50)')
    ax.set_title('Fungsi Keanggotaan Output - Risiko Diabetes (Tsukamoto)', fontweight='bold')
    ax.set_xlabel('Skor Risiko'); ax.set_ylabel('Derajat Keanggotaan (mu)')
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_hasil_batch(df_hasil):
    """Visualisasi hasil pengujian batch."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Hasil Pengujian Sistem Fuzzy Tsukamoto - Risiko Diabetes",
                 fontsize=13, fontweight='bold')

    # Bar chart skor risiko
    ax = axes[0]
    colors = ['#e74c3c' if l == 'TINGGI' else '#2ecc71' for l in df_hasil['Label']]
    bars = ax.bar(range(len(df_hasil)), df_hasil['Skor'], color=colors, edgecolor='white', lw=0.5)
    ax.axhline(50, color='orange', lw=1.5, ls='--', label='Ambang Batas (50)')
    ax.set_xticks(range(len(df_hasil)))
    ax.set_xticklabels([f"#{i+1}" for i in range(len(df_hasil))], fontsize=8)
    ax.set_ylabel('Skor Risiko (0-100)')
    ax.set_title(f'Skor Risiko per Data (n={len(df_hasil)})')
    ax.set_ylim(0, 105)
    patch_t = mpatches.Patch(color='#e74c3c', label='Risiko Tinggi')
    patch_r = mpatches.Patch(color='#2ecc71', label='Risiko Rendah')
    ax.legend(handles=[patch_t, patch_r, ax.axhline(50, color='orange', ls='--')],
              fontsize=8)
    ax.grid(axis='y', alpha=0.3)

    # Pie chart distribusi
    ax = axes[1]
    jumlah_tinggi = (df_hasil['Label'] == 'TINGGI').sum()
    jumlah_rendah = (df_hasil['Label'] == 'RENDAH').sum()
    wedges, texts, autotexts = ax.pie(
        [jumlah_tinggi, jumlah_rendah],
        labels=[f'Tinggi\n({jumlah_tinggi})', f'Rendah\n({jumlah_rendah})'],
        colors=['#e74c3c', '#2ecc71'],
        autopct='%1.1f%%', startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    ax.set_title('Distribusi Risiko')

    plt.tight_layout()
    plt.show()

# ----------------------------------------------------------
# GUI TKINTER
# ----------------------------------------------------------

class DiabetesFuzzyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Fuzzy Tsukamoto - Risiko Diabetes")
        self.root.geometry("1180x760")
        self.root.minsize(1000, 680)
        self.chart_canvas = None

        self.colors = {
            "bg": "#f5f7fb",
            "panel": "#ffffff",
            "text": "#172033",
            "muted": "#5e6b82",
            "primary": "#2563eb",
            "success": "#16a34a",
            "danger": "#dc2626",
            "border": "#d8deea",
        }

        self.root.configure(bg=self.colors["bg"])
        self._configure_style()
        self._build_layout()
        self.clear_form()

    def _configure_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Panel.TFrame", background=self.colors["panel"])
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background=self.colors["panel"], foreground=self.colors["text"], font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=self.colors["panel"], foreground=self.colors["muted"], font=("Segoe UI", 9))
        style.configure("Title.TLabel", background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 18, "bold"))
        style.configure("Score.TLabel", background=self.colors["panel"], foreground=self.colors["text"], font=("Segoe UI", 34, "bold"))
        style.configure("Result.TLabel", background=self.colors["panel"], font=("Segoe UI", 16, "bold"))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8))
        style.configure("Accent.TButton", background=self.colors["primary"], foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _build_layout(self):
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=18, pady=(16, 8))
        ttk.Label(header, text="Sistem Pendukung Keputusan Risiko Diabetes", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Metode Fuzzy Tsukamoto dengan 4 input dan 81 rule",
            foreground=self.colors["muted"],
            background=self.colors["bg"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        main_area = ttk.Frame(self.root)
        main_area.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        main_area.columnconfigure(1, weight=1)
        main_area.rowconfigure(0, weight=1)

        left = ttk.Frame(main_area, style="Panel.TFrame", padding=16)
        left.grid(row=0, column=0, sticky="nsw", padx=(0, 14))

        right = ttk.Frame(main_area)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        self._build_input_panel(left)
        self._build_result_panel(right)
        self._build_tabs(right)

    def _build_input_panel(self, parent):
        ttk.Label(parent, text="Input Pasien", style="Panel.TLabel", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        ttk.Label(parent, text="Masukkan nilai numerik sesuai rentang berikut.", style="Muted.TLabel").pack(anchor="w", pady=(2, 14))

        self.inputs = {}
        fields = [
            ("glukosa", "Glukosa", "mg/dL", "Rentang: 0 - 200 mg/dL"),
            ("bmi", "BMI", "kg/m2", "Rentang: 10 - 60 kg/m2"),
            ("usia", "Usia", "tahun", "Rentang: 21 - 80 tahun"),
            ("genetik", "DPF / Genetik", "", "Rentang: 0.0 - 2.5"),
        ]
        for key, label, unit, hint in fields:
            row = ttk.Frame(parent, style="Panel.TFrame")
            row.pack(fill="x", pady=7)
            ttk.Label(row, text=label, style="Panel.TLabel").pack(anchor="w")
            ttk.Label(row, text=hint, style="Muted.TLabel").pack(anchor="w", pady=(1, 0))
            input_row = ttk.Frame(row, style="Panel.TFrame")
            input_row.pack(fill="x", pady=(4, 0))
            var = tk.StringVar(value="")
            entry = ttk.Entry(input_row, textvariable=var, width=18, font=("Segoe UI", 11))
            entry.pack(side="left", fill="x", expand=True)
            ttk.Label(input_row, text=unit, style="Muted.TLabel", width=8).pack(side="left", padx=(8, 0))
            entry.bind("<Return>", lambda _event: self.hitung())
            self.inputs[key] = var

        button_row = ttk.Frame(parent, style="Panel.TFrame")
        button_row.pack(fill="x", pady=(16, 10))
        ttk.Button(button_row, text="Hitung Risiko", style="Accent.TButton", command=self.hitung).pack(fill="x")
        ttk.Button(button_row, text="Bersihkan", command=self.clear_form).pack(fill="x", pady=(8, 0))

        ttk.Separator(parent).pack(fill="x", pady=14)
        ttk.Label(parent, text="Derajat Keanggotaan", style="Panel.TLabel", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        mu_frame = ttk.Frame(parent, style="Panel.TFrame")
        mu_frame.pack(fill="both", expand=True, pady=(8, 0))
        self.mu_text = tk.Text(mu_frame, width=34, height=13, wrap="none", relief="flat", bg="#f8fafc", fg=self.colors["text"], font=("Consolas", 9))
        mu_scroll = ttk.Scrollbar(mu_frame, orient="vertical", command=self.mu_text.yview)
        self.mu_text.configure(yscrollcommand=mu_scroll.set)
        self.mu_text.pack(side="left", fill="both", expand=True)
        mu_scroll.pack(side="right", fill="y")
        self.mu_text.configure(state="disabled")

    def _build_result_panel(self, parent):
        result = ttk.Frame(parent, style="Panel.TFrame", padding=14)
        result.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        result.columnconfigure(1, weight=1)

        ttk.Label(result, text="Skor Risiko", style="Panel.TLabel", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.score_label = ttk.Label(result, text="0.00", style="Score.TLabel")
        self.score_label.grid(row=1, column=0, sticky="w", pady=(2, 0))
        ttk.Label(result, text="/ 100", style="Muted.TLabel").grid(row=1, column=0, sticky="e", padx=(120, 0), pady=(28, 0))

        self.result_label = ttk.Label(result, text="Risiko -", style="Result.TLabel")
        self.result_label.grid(row=0, column=1, rowspan=2, sticky="e", padx=(20, 0))

        self.active_rules_label = ttk.Label(result, text="Rules aktif: 0 dari 81", style="Muted.TLabel")
        self.active_rules_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

    def _build_tabs(self, parent):
        self.tabs = ttk.Notebook(parent)
        self.tabs.grid(row=1, column=0, sticky="nsew")

        self.chart_tab = ttk.Frame(self.tabs, style="Panel.TFrame")
        self.rule_tab = ttk.Frame(self.tabs, style="Panel.TFrame", padding=10)
        self.tabs.add(self.chart_tab, text="Visualisasi")
        self.tabs.add(self.rule_tab, text="Rule Aktif")

        self.chart_tab.rowconfigure(0, weight=1)
        self.chart_tab.columnconfigure(0, weight=1)

        columns = ("rule", "glukosa", "bmi", "usia", "genetik", "output", "alpha", "zi")
        self.rule_table = ttk.Treeview(self.rule_tab, columns=columns, show="headings")
        headings = {
            "rule": "Rule", "glukosa": "Glukosa", "bmi": "BMI", "usia": "Usia",
            "genetik": "Genetik", "output": "Output", "alpha": "Alpha", "zi": "z_i"
        }
        widths = {"rule": 70, "glukosa": 95, "bmi": 95, "usia": 105, "genetik": 95, "output": 90, "alpha": 90, "zi": 90}
        for col in columns:
            self.rule_table.heading(col, text=headings[col])
            self.rule_table.column(col, width=widths[col], anchor="center")

        y_scroll = ttk.Scrollbar(self.rule_tab, orient="vertical", command=self.rule_table.yview)
        self.rule_table.configure(yscrollcommand=y_scroll.set)
        self.rule_table.pack(side="left", fill="both", expand=True)
        y_scroll.pack(side="right", fill="y")

    def _get_values(self):
        empty_fields = [key for key, var in self.inputs.items() if not var.get().strip()]
        if empty_fields:
            messagebox.showwarning("Input belum lengkap", "Lengkapi semua input terlebih dahulu.")
            return None

        try:
            values = {
                key: float(var.get().replace(",", "."))
                for key, var in self.inputs.items()
            }
        except ValueError:
            messagebox.showerror("Input tidak valid", "Semua input harus berupa angka.")
            return None

        ranges = {
            "glukosa": (0, 200, "Glukosa"),
            "bmi": (10, 60, "BMI"),
            "usia": (21, 80, "Usia"),
            "genetik": (0.0, 2.5, "DPF / Genetik"),
        }
        invalid = []
        for key, (minimum, maximum, label) in ranges.items():
            if values[key] < minimum or values[key] > maximum:
                invalid.append(f"{label}: {minimum:g} - {maximum:g}")

        if invalid:
            messagebox.showwarning(
                "Input di luar rentang",
                "Nilai input harus berada dalam rentang:\n\n" + "\n".join(invalid)
            )
            return None

        return values

    def _membership_summary(self, values):
        lines = [
            "Glukosa",
            f"  Rendah : {mf_glukosa_rendah(values['glukosa']):.3f}",
            f"  Normal : {mf_glukosa_normal(values['glukosa']):.3f}",
            f"  Tinggi : {mf_glukosa_tinggi(values['glukosa']):.3f}",
            "",
            "BMI",
            f"  Kurus    : {mf_bmi_kurus(values['bmi']):.3f}",
            f"  Normal   : {mf_bmi_normal(values['bmi']):.3f}",
            f"  Obesitas : {mf_bmi_obesitas(values['bmi']):.3f}",
            "",
            "Usia",
            f"  Muda      : {mf_usia_muda(values['usia']):.3f}",
            f"  ParuhBaya : {mf_usia_paruhbaya(values['usia']):.3f}",
            f"  Tua       : {mf_usia_tua(values['usia']):.3f}",
            "",
            "Genetik / DPF",
            f"  Rendah : {mf_genetik_rendah(values['genetik']):.3f}",
            f"  Sedang : {mf_genetik_sedang(values['genetik']):.3f}",
            f"  Tinggi : {mf_genetik_tinggi(values['genetik']):.3f}",
        ]
        return "\n".join(lines)

    def hitung(self):
        values = self._get_values()
        if values is None:
            return

        skor, label, aktif = inferensi_tsukamoto(
            values["glukosa"], values["bmi"], values["usia"], values["genetik"]
        )

        result_color = self.colors["danger"] if label == "TINGGI" else self.colors["success"]
        self.score_label.configure(text=f"{skor:.2f}")
        self.result_label.configure(text=f"Risiko {label}", foreground=result_color)
        self.active_rules_label.configure(text=f"Rules aktif: {len(aktif)} dari {len(RULES)}")

        self.mu_text.configure(state="normal")
        self.mu_text.delete("1.0", tk.END)
        self.mu_text.insert(tk.END, self._membership_summary(values))
        self.mu_text.configure(state="disabled")

        for item in self.rule_table.get_children():
            self.rule_table.delete(item)
        for row in aktif:
            no, g, b, u, w, out, alpha, zi = row
            self.rule_table.insert("", "end", values=(f"R{no}", g, b, u, w, out, f"{alpha:.4f}", f"{zi:.2f}"))

        self._update_chart(values, skor, label)

    def _update_chart(self, values, skor, label):
        if self.chart_canvas is not None:
            self.chart_canvas.get_tk_widget().destroy()
            plt.close(self.chart_canvas.figure)

        if values is None:
            fig = plot_membership_functions(show=False)
        else:
            fig = plot_membership_functions(
                values["glukosa"], values["bmi"], values["usia"], values["genetik"],
                skor=skor, label=label, show=False
            )
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_tab)
        self.chart_canvas.draw()
        widget = self.chart_canvas.get_tk_widget()
        widget.grid(row=0, column=0, sticky="nsew")

    def clear_form(self):
        for var in self.inputs.values():
            var.set("")

        self.score_label.configure(text="-")
        self.result_label.configure(text="Risiko -", foreground=self.colors["muted"])
        self.active_rules_label.configure(text="Rules aktif: -")

        self.mu_text.configure(state="normal")
        self.mu_text.delete("1.0", tk.END)
        self.mu_text.insert(tk.END, "Belum ada perhitungan.\n\nIsi semua input lalu klik Hitung Risiko.")
        self.mu_text.configure(state="disabled")

        for item in self.rule_table.get_children():
            self.rule_table.delete(item)

        self._update_chart(None, None, None)


def launch_gui():
    root = tk.Tk()
    DiabetesFuzzyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
