# 🎛️ zzluxora v8.0.0 (Gold Edition)

> **Native PySide6 (Qt6) + Art-Net DMX512 Lighting Control with Audio-Reactive Scene Generation.**  
> Edisi rilis v8 dengan tema visual *Gold Accent Edition* (`#FFD700`), konsolidasi engine *canonical color mapping* sebagai *single source of truth*, dan integrasi *default blackout safety*.

---

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-PySide6%20%2F%20Qt6-41CD52?style=flat-square&logo=qt&logoColor=white)
![Protocol](https://img.shields.io/badge/Protocol-Art--Net_4_DMX512_(UDP_6454)-orange?style=flat-square)
![Theme](https://img.shields.io/badge/Theme-Gold_Accent_(%23FFD700)-gold?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows_10%2F11-0078D6?style=flat-square&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

---

## 📑 Daftar Isi
1. [Gambaran Umum Proyek](#-1-gambaran-umum-proyek)
2. [Pembaruan & Fitur Unggulan v8.0.0](#-2-pembaruan--fitur-unggulan-v800)
3. [Arsitektur Sistem & Engine Terpusat](#-3-arsitektur-sistem--engine-terpusat)
4. [Katalog Direktori Proyek](#-4-katalog-direktori-proyek)
5. [Panduan Instalasi & Eksekusi](#-5-panduan-instalasi--eksekusi)
6. [Kompilasi Standalone .EXE & Installer](#-6-kompilasi-standalone-exe--installer)
7. [Pengujian Matematis Model (Unit Tests)](#-7-pengujian-matematis-model-unit-tests)
8. [Lisensi & Hak Cipta](#-8-lisensi--hak-cipta)

---

## 📖 1. Gambaran Umum Proyek

**zzluxora v8.0.0** merupakan kelanjutan evolusioner dari lini perangkat lunak pengendali tata cahaya panggung cerdas berbasis Windows native. Versi ini berfokus pada refaktorisasi modularitas matematika warna, penguatan keamanan operasional panggung (*blackout safety*), serta transisi identitas visual ke tema **Gold Accent Theme (`#FFD700`)**.

Aplikasi ini menghubungkan analisis komputasi audio musik (*Music Information Retrieval / MIR*) secara langsung dengan respons pencahayaan panggung (*Moving Head, PAR LED RGBW, Strobe*) secara deterministik 60 FPS tanpa jeda melalui protokol jaringan **Art-Net DMX512 via UDP (Port 6454)**.

---

## ✨ 2. Pembaruan & Fitur Unggulan v8.0.0

- 🌟 **Gold Accent Design System:** Pembaruan palet visual antarmuka bernuansa emas modern (`#FFD700`) pada komponen aktif, tombol pemicu, fader, dan status pill.
- 📐 **Canonical Color Mapping Engine:** Seluruh logika matematika konversi ruang warna kini dipusatkan ke `engines/color_mapping.py` (*Single Source of Truth*), mengeliminasi duplikasi kode antar modul.
- 🛡️ **Master Blackout Safety Default:** Fader master kini dimulai dari nilai 0 (Blackout) saat startup untuk mencegah lonjakan intensitas lampu mendadak di panggung.
- 🎧 **8-Stage Audio Analysis Pipeline:** Ekstraksi parameter audio komprehensif via **Librosa** (RMS Energy, Tempo BPM, Onset Strength, Spectral Centroid, Chroma STFT Mayor vs Minor, dan MFCC 13 Koefisien).
- 🧠 **Valence-Arousal Mood Classification:** Visualisasi koordinat afektif emosi musik 2D (Russell Circumplex Model) untuk klasifikasi dinamis suasana *Praise* dan *Worship*.
- 🎚️ **Precision DMX512 Channel Mixer:** Fader mixer kontrol kanal 0–255 dengan pembacaan numerik presisi dan proteksi kanal *White* murni.
- 🔘 **Page Tab Live Show Pad:** Matriks tombol pemicu adegan (*Scenes*) dan *Chases* secara instan untuk kebutuhan pertunjukan panggung langsung.
- 📦 **Inno Setup & PyInstaller Packaging:** Skrip kompilasi mandiri untuk distribusi installer Windows profesional.

---

## 🏗️ 3. Arsitektur Sistem & Engine Terpusat

```text
+-----------------------------------------------------------------------------------------+
|                                ARSITEKTUR ZZLUXORA v8.0                                 |
+-----------------------------------------------------------------------------------------+
  [1] USER INTERFACE (PySide6 / Qt6 - Gold Theme #FFD700):
      • HeaderBar       : Brand Title, Project Status, Art-Net Pill Indicator, Start/Stop
      • Collapsible Sidebar : Navigasi ikonik panel dengan toggle state
      • ProgramPanel    : Container tab multi-fungsi (Address, Audio, Scenes, Chase, Mixer, Page)
      • SettingsPanel   : Konfigurasi broadcast IP, port, interface jaringan, dan universe
          │
          ▼
  [2] COMPUTATIONAL ENGINES (Canonical Single Source of Truth):
      • color_mapping.py     : [CANONICAL] Transformasi HSV ke Physical 4-Channel RGBW
      • audio_engine.py      : Ekstraksi fitur akustik Librosa & deteksi tempo/onset
      • mood_engine.py       : Pemodelan afektif koordinat Valence-Arousal
      • scene_generator.py   : Pembangkit sekuens & palet warna dinamis
      • scene_player.py      : Playback loop sinkron 40 FPS
          │
          ▼
  [3] NETWORK PROTOCOL LAYER:
      • artnet_sender.py     : Penyusun paket biner ArtDmx UDP (OpCode 0x5000)
      • Target Receiver      : Node Mikrokontroler ESP32 DevKit V1 + MAX485 DMX512
+-----------------------------------------------------------------------------------------+
```

---

## 📁 4. Katalog Direktori Proyek

```text
zzluxora_v8/
├── main.py                  <- Titik masuk aplikasi (Entry Point PySide6)
├── main_window.py           <- Jendela utama dengan sistem navigasi sidebar & multi-panel
├── config.py / config.ini   <- Pengaturan default, universe Art-Net, & konfigurasi jaringan
├── fixture_manager.py       <- Pengelola database lampu panggung & DMX patch map
├── styles.py                <- Desain tema antarmuka Gold Accent (#FFD700) & QSS tokens
├── font_loader.py           <- Pemuat tipografi Windows native
├── icons.py                 <- Koleksi ikon vektor UI
├── requirements.txt         <- Daftar pustaka dependensi Python
├── zzluxora.spec            <- Konfigurasi PyInstaller Onedir Build
│
├── 📂 engines/              <- Core computational engines:
│   ├── analyze_pipeline.py  <- 8-stage pipeline orchestrator
│   ├── artnet_sender.py     <- Art-Net UDP socket packet broadcaster
│   ├── audio_engine.py      <- Ekstraksi fitur Librosa & deteksi tempo
│   ├── chase.py             <- Logika chase sequence ritmis
│   ├── color_mapping.py     <- [CANONICAL] Konversi ruang warna HSV ke RGBW
│   ├── color_mixer.py       <- Utilitas pencampur warna & Curve LUT
│   ├── fixture_types.py     <- Definisi profil kanal DMX
│   ├── mood_engine.py       <- Model Valence-Arousal mood classifier
│   ├── scene_generator.py   <- Pembangkit scene pencahayaan otomatis
│   └── va_presets.py        <- Preset koordinat afektif emosi musik
│
├── 📂 panels/               <- Panel antarmuka pengguna:
│   ├── address_tab.py       <- Manajemen alamat patch DMX
│   ├── audio_tab.py         <- Visualizer spektrum & parameter audio
│   ├── chase_tab.py         <- Pengaturan sekuens chase lampu
│   ├── color_mixer_tab.py   <- Pemilih palet warna manual
│   ├── fixture_editor_panel.py <- Editor profil lampu DMX
│   ├── fixture_list_panel.py   <- Daftar lampu yang terpasang
│   ├── mixer_tab.py         <- Fader kontrol kanal DMX512
│   ├── output_tab.py        <- Monitor data kanal live
│   ├── page_tab.py          <- Button pad pemicu adegan live show
│   ├── preview_tab.py       <- Pratinjau panggung visual 2D
│   ├── program_panel.py     <- Tab host utama
│   ├── settings_panel.py    <- Konfigurasi jaringan & Art-Net
│   └── about_panel.py       <- Informasi lisensi & metadata akademik
│
├── 📂 widgets/              <- Komponen UI kustom (ArtNet pill, Curve editor, Toast, dll)
├── 📂 fixtures/             <- Profil lampu Generic PAR RGBW 8ch (.json)
├── 📂 assets/               <- Ikon aplikasi, logo vektor, dan file .ico
├── 📂 installer/            <- Skrip Inno Setup Compiler (zzluxora.iss)
└── 📂 tests/                <- Unit tests verifikasi model matematika
```

---

## 🚀 5. Panduan Instalasi & Eksekusi

### Persyaratan Sistem:
- **Sistem Operasi:** Windows 10 / 11 (64-bit)
- **Python:** Versi 3.10 atau lebih baru

### Langkah Menjalankan:
1. **Clone Repositori:**
   ```powershell
   git clone https://github.com/zzdree/zzluxora-v8.git
   cd zzluxora-v8
   ```

2. **Install Dependensi:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi:**
   ```powershell
   python main.py
   ```

---

## 🛠️ 6. Kompilasi Standalone .EXE & Installer

### 1. Build Portable Executable (PyInstaller):
```powershell
python build.py
```
Hasil build akan tersimpan di direktori `dist/zzluxora/` (`zzluxora.exe` + folder `_internal/`).

### 2. Build Windows Setup Wizard (Inno Setup):
Buka berkas `installer/zzluxora.iss` menggunakan **Inno Setup Compiler**, lalu klik **Compile (Ctrl + F9)**. Installer mandiri `zzluxora-setup-v8.0.0.exe` akan dihasilkan secara otomatis.

---

## 🧪 7. Pengujian Matematis Model (Unit Tests)

Proyek ini dilengkapi dengan modul pengujian unit untuk memvalidasi akurasi formula matematika konversi ruang warna dan ekstraksi parameter audio:

```powershell
pytest tests/ -v
```

---

## 📜 8. Lisensi & Hak Cipta

Proyek ini dilisensikan di bawah **MIT License**.  
Hak Cipta (c) 2026 **Andreas Restuawanta Christwara ([@zzdree](https://github.com/zzdree))** — Universitas Negeri Semarang.
