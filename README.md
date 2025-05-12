# Ludo PNG Mixer

Ein Python-Tool zum Mischen von A-Typ und B-Typ PNG-Bildern mit konfigurierbarer Seltenheitsverteilung.

## 🚀 Features

- **A-Typ Bilder**: 3 Seltenheitsstufen
  - Common (a.png)
  - Uncommon (b.png) 
  - Legendary (c.png)

- **B-Typ Bilder**: 2 Varianten
  - Normal (xp.png)
  - Special (xpxd.png)

- **Konfigurierbare Parameter**:
  - Slider für A-Typ Verteilung (Common/Uncommon/Legendary %)
  - Slider für B-Typ Special-Chance %
  - 1:1 Verhältnis zwischen A- und B-Typ Bildern (verpflichtend)

- **Output**:
  - DIN A4 Format (2480 x 3508 Pixel bei 300 DPI)
  - 6 Bilder pro Reihe
  - Automatische Skalierung
  - PNG-Format

- **Zwei Modi verfügbar**:
  - 🖥️ **GUI-Version** (`png_mixer.py`) - für Desktop-Umgebungen
  - 💻 **CLI-Version** (`png_mixer_cli.py`) - für WSL/headless/server Umgebungen

## 📦 Installation

1. Repository klonen:
```bash
git clone https://github.com/LiTschii/Ludo_25_pngmixer.git
cd Ludo_25_pngmixer
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## 🖥️ GUI-Version (Desktop)

```bash
python png_mixer.py
```

## 💻 CLI-Version (WSL/Headless)

### Interaktiver Modus (Empfohlen für Einsteiger)
```bash
python png_mixer_cli.py interactive
```

### Batch-Modus (Für Automatisierung)
```bash
python png_mixer_cli.py batch \
  --common a.png \
  --uncommon b.png \
  --legendary c.png \
  --normal xp.png \
  --special xpxd.png \
  --a-common 70 \
  --a-uncommon 25 \
  --a-legendary 5 \
  --b-special 10 \
  --output result.png
```

### Verfügbare CLI-Befehle
```bash
# Interaktiver Modus
python png_mixer_cli.py interactive

# Batch-Modus mit allen Optionen
python png_mixer_cli.py batch [OPTIONS]

# Konfiguration verwalten
python png_mixer_cli.py config

# Beispiele anzeigen
python png_mixer_cli.py examples

# Hilfe anzeigen
python png_mixer_cli.py --help
```

## ⚙️ Konfigurationsdatei

Die CLI-Version kann Konfigurationen in JSON-Dateien speichern und laden:

```json
{
  "a_common": 70,
  "a_uncommon": 25,
  "a_legendary": 5,
  "b_special": 10
}
```

Verwendung:
```bash
# Konfiguration speichern
python png_mixer_cli.py config

# Mit gespeicherter Konfiguration arbeiten
python png_mixer_cli.py batch --config meine_config.json [andere optionen]
```

## 📋 Bildanforderungen

- **Format**: PNG
- **Auflösung**: $500 \times 500$ Pixel
- **A-Typ**: a.png (Common), b.png (Uncommon), c.png (Legendary)
- **B-Typ**: xp.png (Normal), xpxd.png (Special)

## 🧮 Technische Details

- **DIN A4**: $2480 \times 3508$ Pixel bei 300 DPI
- **Bilder pro Reihe**: 6
- **Bild-Ratio**: Immer 1:1 (A-Typ : B-Typ)
- **Automatische Skalierung**: Bilder werden proportional an die verfügbare Fläche angepasst
- **Zufällige Anordnung**: Die generierten Bilder werden gemischt und zufällig angeordnet

## 🎯 Verwendungsbeispiele

### CLI - Interaktiver Modus
```bash
python png_mixer_cli.py interactive
```
- Schritt-für-Schritt Anleitung
- Bildvalidierung
- Konfiguration mit Prompts
- Automatisches Speichern der Einstellungen

### CLI - Batch-Verarbeitung
```bash
# Einfache Ausführung mit Standardwerten
python png_mixer_cli.py batch \
  --common a.png --uncommon b.png --legendary c.png \
  --normal xp.png --special xpxd.png

# Mit benutzerdefinierten Wahrscheinlichkeiten
python png_mixer_cli.py batch \
  --common a.png --uncommon b.png --legendary c.png \
  --normal xp.png --special xpxd.png \
  --a-common 60 --a-uncommon 30 --a-legendary 10 \
  --b-special 20 \
  --output meine_karten.png
```

## 🔧 Fehlerbehebung

### XCB-Fehler in WSL
Falls die GUI-Version nicht funktioniert:
```bash
# Verwenden Sie die CLI-Version
python png_mixer_cli.py interactive
```

### Bilder werden nicht gefunden
```bash
# Überprüfen Sie die Pfade
ls -la *.png

# Verwenden Sie absolute Pfade
python png_mixer_cli.py batch --common /vollständiger/pfad/zu/a.png [...]
```

## 📄 Lizenz

MIT License
