# Building zzluxora Windows Installer

## Prerequisites

- Python 3.14+ with venv activated
- Pillow (`pip install pillow`)
- PyInstaller (`pip install pyinstaller`)
- Inno Setup 6+ ([jrsoftware.org](https://jrsoftware.org/isdl.php))

## Build Steps

```powershell
cd C:\ANDREAS\SCRIPT\zzluxora

# Step 1: Generate icon (one-time, skip if assets/zzluxora.ico exists)
python tools/make_ico.py

# Step 2: Build .exe (PyInstaller onedir)
python build.py
# Output: ../results/zzluxora-v8/

# Step 3: Build installer (Inno Setup)
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\zzluxora.iss
# Output: installer/Output/zzluxora-setup-v8.0.0.exe
```

## What the Installer Does

- Installs to `Program Files\zzluxora\`
- Creates Start Menu shortcut + optional desktop shortcut
- Registers `.zlx` file association
- **Clean install**: deletes old app folder before copying (anti-tumpuk)
- **Optional**: wipe `%APPDATA%\zzluxora\` during install (checkbox)

## Uninstaller

- Removes app folder from `Program Files\`
- Prompts: "Keep settings and data?" 
  - Yes → keeps `%APPDATA%\zzluxora\`
  - No → deletes all data permanently

## Data Locations

| What | Where |
|---|---|
| App (read-only) | `Program Files\zzluxora\` |
| Config | `%APPDATA%\zzluxora\config.ini` |
| Fixtures | `%APPDATA%\zzluxora\fixtures\` (copied on first run) |
| Chases | `%APPDATA%\zzluxora\chases\` |
| Programs | `%APPDATA%\zzluxora\programs\` |
| Pages | `%APPDATA%\zzluxora\pages\` |
| Presets | `%APPDATA%\zzluxora\presets\` |
