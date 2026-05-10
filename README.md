# 🧮 ModernCalc

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-32%20passed-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)

**Aplikasi kalkulator desktop modern dan professional**  
dibangun dengan Python & PyQt6 — clean architecture, secure, dan production-ready.

</div>

---

## ✨ Fitur Utama

### 🔢 Basic Calculator
- Operasi dasar: tambah, kurang, kali, bagi, modulus
- Input desimal, negatif, dan kurung `( )`
- Tombol Clear `C` dan Backspace `⌫`
- Update display secara real-time

### 🔬 Scientific Calculator
| Fungsi | Fungsi | Fungsi |
|--------|--------|--------|
| `sin()` | `cos()` | `tan()` |
| `log()` | `ln()` | `√` (sqrt) |
| `x²` | `xʸ` (power) | `\|x\|` (absolute) |
| `n!` (factorial) | `1/x` (reciprocal) | `π` dan `e` |

### 🧠 Sistem Memori
- **M+** — Tambahkan nilai ke memori
- **M−** — Kurangi nilai dari memori
- **MR** — Ambil nilai dari memori
- **MC** — Hapus memori

### 📋 History System
- Menyimpan semua riwayat perhitungan otomatis
- Tersimpan ke file JSON secara lokal
- Sidebar history yang bisa dibuka/tutup dengan animasi
- Klik item history untuk menggunakan kembali ekspresi
- Tombol Clear History
- Dilengkapi timestamp setiap perhitungan

### 🎨 Theme System
- **Dark Mode** — Default (Catppuccin-inspired)
- **Light Mode** — Toggle dengan satu klik
- Preferensi tema tersimpan otomatis

### ⌨️ Keyboard Shortcuts
| Key | Aksi |
|-----|------|
| `Enter` / `Return` | Hitung hasil |
| `Escape` | Clear semua |
| `Backspace` | Hapus karakter terakhir |
| `0–9` | Input angka |
| `+` `-` `*` `/` | Operator aritmatika |
| `.` | Desimal |
| `%` | Persen |
| `(` `)` | Kurung |

### 🔐 Keamanan
- **Zero `eval()`** — Ekspresi dievaluasi menggunakan Python AST
- Whitelist fungsi matematika yang diizinkan
- Validasi & sanitasi input sebelum parsing
- Blokir keyword berbahaya (`exec`, `__import__`, dll)

---

## 🚀 Instalasi & Menjalankan

### Prasyarat
- Python 3.11 atau lebih baru
- pip (Python package manager)

### Langkah Instalasi

**1. Clone repository**
```bash
git clone https://github.com/username/moderncalc.git
cd moderncalc/calculator-app
```

**2. (Opsional tapi direkomendasikan) Buat virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Jalankan aplikasi**
```bash
python main.py
```

---

## 🧪 Menjalankan Unit Tests

```bash
# Menggunakan unittest (tanpa pytest)
python -m unittest tests/test_calculator_engine.py -v

# Menggunakan pytest (jika terinstal)
pip install pytest
pytest tests/ -v
```

**Output yang diharapkan:**
```
Ran 32 tests in 0.006s
OK
```

---

## 📦 Build ke File .exe (Windows)

**1. Install PyInstaller**
```bash
pip install pyinstaller
```

**2. Build single executable**
```bash
pyinstaller --onefile --windowed ^
  --name "ModernCalc" ^
  --add-data "app/assets;app/assets" ^
  main.py
```

**3. Hasil build**

File `.exe` akan tersedia di:
```
dist/
└── ModernCalc.exe
```

---

## 🏗️ Arsitektur Proyek

```
calculator-app/
│
├── main.py                          # Entry point aplikasi
├── requirements.txt
├── README.md
│
├── app/
│   ├── ui/                          # Lapisan tampilan (View)
│   │   ├── main_window.py           # Window utama + keyboard shortcut
│   │   ├── splash_screen.py         # Splash screen animasi
│   │   └── components/
│   │       ├── calculator_display.py  # Panel display
│   │       ├── button_grid.py         # Grid tombol basic & scientific
│   │       └── history_sidebar.py     # Sidebar collapsible
│   │
│   ├── core/                        # Logika bisnis (Model)
│   │   ├── calculator_engine.py     # State ekspresi & evaluasi
│   │   ├── scientific_engine.py     # Ekstensi fungsi ilmiah
│   │   ├── expression_parser.py     # AST parser aman (no eval)
│   │   └── validator.py             # Validasi & sanitasi input
│   │
│   ├── services/                    # Lapisan layanan
│   │   ├── history_service.py       # Persistence history ke JSON
│   │   ├── memory_service.py        # Register memori M+/M-/MR/MC
│   │   └── theme_service.py         # Manajemen tema & QSS
│   │
│   ├── utils/
│   │   ├── constants.py             # Konstanta global
│   │   ├── formatter.py             # Format angka & ekspresi
│   │   └── helpers.py               # JSON I/O, timestamp
│   │
│   └── assets/themes/
│       ├── dark.qss                 # Dark theme stylesheet
│       └── light.qss                # Light theme stylesheet
│
├── data/                            # Auto-generated saat runtime
│   ├── history.json
│   └── settings.json
│
└── tests/
    └── test_calculator_engine.py   # 32 unit tests
```

---

## 🔒 Alur Keamanan

```
Input Pengguna
    ↓
Validator (regex whitelist + keyword blacklist)
    ↓
SafeExpressionParser (Python AST)
    ↓
Whitelist: operator math + fungsi math.*
    ↓
Hasil Aman ✅
```

---

## 📋 Dependencies

| Package | Versi | Kegunaan |
|---------|-------|----------|
| `PyQt6` | >= 6.6.0 | Framework UI desktop |
| `PyInstaller` | >= 6.0.0 | Build ke .exe (opsional) |

---

## 🤝 Kontribusi

1. Fork repository ini
2. Buat branch: `git checkout -b feature/nama-fitur`
3. Commit: `git commit -m "feat: deskripsi fitur"`
4. Push: `git push origin feature/nama-fitur`
5. Buat Pull Request



---

<div align="center">
Dibuat dengan ❤️ menggunakan Python & PyQt6
</div>
