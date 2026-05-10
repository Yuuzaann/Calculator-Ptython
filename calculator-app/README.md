# ModernCalc — Professional Desktop Calculator

Aplikasi kalkulator desktop modern dan premium dibangun dengan Python 3.11+ dan PyQt6.

---

## Fitur

| Kategori | Fitur |
|---|---|
| **Basic** | +, −, ×, ÷, %, desimal, kurung, negasi |
| **Scientific** | sin, cos, tan, log, ln, √, x², xʸ, \|x\|, 1/x, n!, π, e |
| **Memory** | M+, M−, MR, MC |
| **History** | Auto-save JSON, sidebar collapsible, klik untuk reuse |
| **Theme** | Dark mode (default) + Light mode, persisten |
| **Keyboard** | Enter=hitung, Esc=clear, Backspace=hapus, angka & operator |
| **Keamanan** | AST parser (NO eval()), validator, whitelist fungsi |
| **UX** | Splash screen, copy to clipboard, responsive font, animasi sidebar |

---

## Struktur Proyek

```
calculator-app/
├── main.py                          # Entry point
├── requirements.txt
├── README.md
├── app/
│   ├── ui/
│   │   ├── main_window.py           # Window utama
│   │   ├── splash_screen.py         # Splash screen animasi
│   │   └── components/
│   │       ├── calculator_display.py  # Panel display
│   │       ├── button_grid.py         # Grid tombol (basic & scientific)
│   │       └── history_sidebar.py     # Sidebar history collapsible
│   ├── core/
│   │   ├── calculator_engine.py     # Engine dasar + state expression
│   │   ├── scientific_engine.py     # Ekstensi fungsi ilmiah
│   │   ├── expression_parser.py     # AST parser aman (no eval)
│   │   └── validator.py             # Validasi input
│   ├── services/
│   │   ├── history_service.py       # Persistence history (JSON)
│   │   ├── memory_service.py        # Register memori M+/M-/MR/MC
│   │   └── theme_service.py         # Manajemen tema + QSS
│   ├── utils/
│   │   ├── constants.py             # Konstanta global
│   │   ├── formatter.py             # Format angka & ekspresi
│   │   └── helpers.py               # JSON I/O, timestamp, dll
│   └── assets/
│       └── themes/
│           ├── dark.qss             # Dark theme stylesheet
│           └── light.qss            # Light theme stylesheet
├── data/
│   ├── history.json                 # Auto-generated: riwayat perhitungan
│   └── settings.json               # Auto-generated: preferensi tema
└── tests/
    └── test_calculator_engine.py   # Unit tests
```

---

## Instalasi

### 1. Pastikan Python 3.11+ terinstal

```bash
python --version
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:

```bash
pip install PyQt6
```

---

## Menjalankan Aplikasi

```bash
cd calculator-app
python main.py
```

---

## Menjalankan Unit Tests

```bash
cd calculator-app
python -m pytest tests/ -v
```

Atau tanpa pytest:

```bash
python -m unittest tests/test_calculator_engine.py -v
```

---

## Build ke .exe (Windows) dengan PyInstaller

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build single executable

```bash
cd calculator-app
pyinstaller --onefile --windowed --name "ModernCalc" \
  --add-data "app/assets:app/assets" \
  main.py
```

### 3. Output

File `.exe` ada di folder `dist/ModernCalc.exe`

### 4. Build dengan spec file (direkomendasikan)

```bash
pyinstaller ModernCalc.spec
```

---

## Arsitektur

### Pola MVC / Clean Architecture

```
UI Layer         →  app/ui/
  ↕ signals/slots
Service Layer    →  app/services/
  ↕ method calls
Core Layer       →  app/core/
  ↕ pure logic
Utils            →  app/utils/
```

### Keputusan Arsitektur

1. **No `eval()`** — Semua ekspresi di-parse menggunakan Python `ast` module dengan whitelist ketat. Tidak ada kode arbitrary yang bisa dieksekusi.

2. **ScientificEngine extends CalculatorEngine** — Scientific mode menambah fungsi tanpa mengubah logika dasar (Open/Closed Principle).

3. **Services sebagai singletons** — `HistoryService`, `MemoryService`, `ThemeService` di-instantiate sekali di `main.py` lalu di-inject ke `MainWindow`.

4. **QSS dipisah per tema** — `dark.qss` dan `light.qss` adalah file terpisah, memudahkan kustomisasi visual tanpa menyentuh kode Python.

5. **`ButtonDef` dataclass** — Layout tombol dideklarasikan sebagai data, bukan hardcoded di UI code. Mudah dimodifikasi tanpa refaktor grid logic.

---

## Keyboard Shortcuts

| Key | Aksi |
|---|---|
| `Enter` / `Return` | Hitung (=) |
| `Escape` | Clear semua |
| `Backspace` | Hapus karakter terakhir |
| `0–9` | Input angka |
| `+`, `−`, `*`, `/` | Operator |
| `.` | Desimal |
| `%` | Persen |
| `(`, `)` | Kurung |

---

## Security

- Input divalidasi dengan regex whitelist sebelum parsing
- Keyword berbahaya (`__import__`, `eval`, `exec`, dll) diblokir
- AST parser hanya mengizinkan operator matematika dan fungsi `math` yang terdaftar
- Tidak ada eksekusi kode arbitrary

---

## Requirements

```
Python >= 3.11
PyQt6 >= 6.6.0
PyInstaller >= 6.0.0  (hanya untuk build .exe)
```
