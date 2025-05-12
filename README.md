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
  - Alle Pfade und Einstellungen in JSON-Konfiguration

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

3. CLI-Script ausführbar machen:
```bash
chmod +x cli.sh
```

## 🖥️ GUI-Version (Desktop)

```bash
python png_mixer.py
```

## 💻 CLI-Version (WSL/Headless)

### 🚀 Shortcut mit cli.sh

Das `cli.sh` Script bietet eine bequeme Kurzform und verwaltet automatisch die Virtual Environment:

```bash
# Interaktiver Modus
./cli.sh interactive

# Generieren mit Konfigurationsdatei
./cli.sh generate

# Konfiguration verwalten
./cli.sh config

# Hilfe anzeigen
./cli.sh --help
```

### 📋 Neue erweiterte Konfigurationsdatei

Alle Einstellungen werden jetzt in einer strukturierten JSON-Datei gespeichert:

```json
{
  "paths": {
    "a_common": "a.png",
    "a_uncommon": "b.png", 
    "a_legendary": "c.png",
    "b_normal": "xp.png",
    "b_special": "xpxd.png"
  },
  "distribution": {
    "a_common": 70,
    "a_uncommon": 25,
    "a_legendary": 5,
    "b_special": 10
  },
  "output": {
    "filename": "ludo_mixed_output.png",
    "width": 2480,
    "height": 3508,
    "images_per_row": 6
  }
}
```

### 🎯 Empfohlener Workflow

```bash
# 1. Einmalig: Konfiguration erstellen
./cli.sh interactive

# 2. Bilder generieren (wiederholbar)
./cli.sh generate

# 3. Konfiguration ansehen/bearbeiten
./cli.sh config
```

### 🔧 Alle verfügbaren Befehle

```bash
# Interaktiver Setup (empfohlen für erste Verwendung)
./cli.sh interactive

# Bilder aus Konfigurationsdatei generieren
./cli.sh generate
./cli.sh generate --config meine_config.json

# Konfiguration verwalten
./cli.sh config
./cli.sh config --config meine_config.json

# Beispiele und Hilfe anzeigen
./cli.sh examples
./cli.sh --help

# Ohne cli.sh (direkt mit Python)
python png_mixer_cli.py interactive
python png_mixer_cli.py generate --config my_config.json
```

## 📋 Bildanforderungen

- **Format**: PNG
- **Auflösung**: $500 \times 500$ Pixel
- **A-Typ**: a.png (Common), b.png (Uncommon), c.png (Legendary)
- **B-Typ**: xp.png (Normal), xpxd.png (Special)

## 🧮 Technische Details

- **DIN A4**: $2480 \times 3508$ Pixel bei 300 DPI
- **Bilder pro Reihe**: 6 (konfigurierbar)
- **Bild-Ratio**: Immer 1:1 (A-Typ : B-Typ)
- **Automatische Skalierung**: Bilder werden proportional an die verfügbare Fläche angepasst
- **Zufällige Anordnung**: Die generierten Bilder werden gemischt und zufällig angeordnet

## 🎯 Verwendungsbeispiele

### Erstmalige Einrichtung
```bash
# Schritt 1: Konfiguration erstellen
./cli.sh interactive
# -> Führt durch Bildauswahl und Einstellungen
# -> Speichert alles in png_mixer_config.json

# Schritt 2: Bilder generieren
./cli.sh generate
# -> Verwendet gespeicherte Konfiguration
```

### Mehrere Konfigurationen verwenden
```bash
# Verschiedene Konfigurationen erstellen
./cli.sh interactive
# -> Konfiguration als 'set1_config.json' speichern

# Mit spezifischer Konfiguration arbeiten
./cli.sh generate --config set1_config.json
./cli.sh config --config set1_config.json
```

### Automatisierung/Scripting
```bash
#!/bin/bash
# Automatisch mehrere Varianten generieren

# Lade verschiedene Konfigurationen und generiere
./cli.sh generate --config christmas_cards.json
./cli.sh generate --config halloween_cards.json
./cli.sh generate --config standard_cards.json
```

## 🔧 Fehlerbehebung

### XCB-Fehler in WSL
Falls die GUI-Version nicht funktioniert:
```bash
# Verwenden Sie die CLI-Version
./cli.sh interactive
```

### Bilder werden nicht gefunden
```bash
# Überprüfen Sie die Pfade
./cli.sh config

# Bei Problemen: Interaktiven Modus verwenden
./cli.sh interactive
```

### Virtual Environment Probleme
```bash
# cli.sh verwaltet das venv automatisch
# Falls Probleme auftreten:
source .venv/bin/activate
pip install -r requirements.txt
```

## 📝 Changelog

### Version 2.0
- ✨ **Neue CLI-Struktur**: Alle Argumente in Konfigurationsdatei
- 🚀 **cli.sh Shortcut**: Automatisierte venv-Verwaltung
- 📊 **`generate` Befehl**: Separate Generierung von Setup
- 🔧 **Erweiterte Konfiguration**: Strukturierte JSON mit Pfaden und Output-Einstellungen
- ⚡ **Verbesserte UX**: Klarere Befehle und weniger Redundanz

### Version 1.0  
- 🎨 GUI-Version mit tkinter
- 💻 Erste CLI-Version mit direkten Argumenten
- 📸 PNG-Generierung mit konfigurierbaren Wahrscheinlichkeiten

## 📄 Lizenz

MIT License
