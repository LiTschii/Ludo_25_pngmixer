# Ludo PNG Mixer - Duplex Edition

Ein Python-Tool zum Erstellen von duplex-kompatiblen PNG-Bildern mit A-Typ und B-Typ Motiven für beidseitiges Drucken.

## 🖨️ Duplex-Funktionalität

**Neue Hauptfunktion:** Das Tool erstellt **zwei separate Seiten** für beidseitiges Drucken:
- **Seite A**: Nur A-Typ Bilder (Common, Uncommon, Legendary)
- **Seite B**: Nur B-Typ Bilder (Normal, Special) - **automatisch gespiegelt** für Duplex

## 🚀 Features

- **A-Typ Bilder**: 3 Seltenheitsstufen
  - Common (a.png)
  - Uncommon (b.png) 
  - Legendary (c.png)

- **B-Typ Bilder**: 2 Varianten
  - Normal (xp.png)
  - Special (xpxd.png)

- **Konfigurierbare Parameter**:
  - **Gesamtanzahl Bilder** (muss gerade sein, Standard: 1000)
  - Verteilung der A-Typ Seltenheiten (Common/Uncommon/Legendary %)
  - B-Typ Special-Chance %
  - Alle Pfade und Einstellungen in JSON-Konfiguration

- **Duplex-Output**:
  - **Zwei separate PNG-Dateien**: `filename_page_A.png` und `filename_page_B.png`
  - **Mehrseiten-Support**: Automatisch mehrere Seiten bei vielen Bildern
  - DIN A4 Format (2480 x 3508 Pixel bei 300 DPI)
  - 6 Bilder pro Reihe (~166 Bilder pro Seite)
  - Automatische Spiegelung von Seite B für perfekte Ausrichtung

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

## 🔢 Bildanzahl-Konfiguration

### Standard-Anzahlen:
- **1000 Bilder** → 500 A-Typ + 500 B-Typ → 3 Seiten A + 3 Seiten B
- **500 Bilder** → 250 A-Typ + 250 B-Typ → 2 Seiten A + 2 Seiten B  
- **166 Bilder** → 83 A-Typ + 83 B-Typ → 1 Seite A + 1 Seite B
- **2000 Bilder** → 1000 A-Typ + 1000 B-Typ → 6 Seiten A + 6 Seiten B

### Beispiele:
```bash
# 1000 Bilder (Standard)
./cli.sh interactive

# 500 Bilder  
./cli.sh generate --total 500

# 2000 Bilder
./cli.sh generate --total 2000
```

## 🖨️ Duplex-Druckprozess

1. **Generieren der Seiten:**
   ```bash
   ./cli.sh interactive  # Setup
   ./cli.sh generate     # Erstellt page_A.png und page_B.png
   ```

2. **Drucken:**
   - 📄 Drucke **alle A-Seiten** (A_1.png, A_2.png, ...)
   - 🔄 Lege die Blätter umgedreht zurück in den Drucker
   - 📄 Drucke **alle B-Seiten** (B_1.png, B_2.png, ...)
   - ✅ Die Bilder sind perfekt ausgerichtet!

## 💻 CLI-Version (Empfohlen)

### 🚀 Shortcut mit cli.sh

```bash
# Setup mit Bildanzahl
./cli.sh interactive

# Schnelle Generierung mit anderer Anzahl
./cli.sh generate --total 500

# Konfiguration anzeigen 
./cli.sh config

# Hilfe anzeigen
./cli.sh --help
```

### 📋 Erweiterte Konfigurationsdatei

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
    "filename": "ludo_cards.png",
    "total_images": 1000,
    "width": 2480,
    "height": 3508,
    "images_per_row": 6,
    "duplex_mode": true
  }
}
```

### 🎯 Empfohlener Workflow

```bash
# 1. Setup (einmalig)
./cli.sh interactive
# -> Alle Bildpfade auswählen
# -> Anzahl Bilder festlegen (z.B. 1000)
# -> Wahrscheinlichkeiten festlegen
# -> Konfiguration speichern

# 2. Generierung (wiederholbar)
./cli.sh generate
# -> Erstellt: ludo_cards_page_A_1.png, page_A_2.png, ...
# -> Erstellt: ludo_cards_page_B_1.png, page_B_2.png, ...

# 3. Verschiedene Anzahlen testen
./cli.sh generate --total 500   # Weniger Karten
./cli.sh generate --total 2000  # Mehr Karten
```

### 🔧 Alle verfügbaren Befehle

```bash
# Interactive Setup
./cli.sh interactive

# Generiere mit Standard-Anzahl
./cli.sh generate

# Generiere mit spezifischer Anzahl
./cli.sh generate --total 500
./cli.sh generate --total 2000 --config meine_config.json

# Verwalte Konfiguration
./cli.sh config

# Zeige Beispiele und Berechnungen
./cli.sh examples

# Hilfe
./cli.sh --help
```

## 📋 Bildanforderungen

- **Format**: PNG
- **Auflösung**: $500 \times 500$ Pixel
- **A-Typ**: a.png (Common), b.png (Uncommon), c.png (Legendary)
- **B-Typ**: xp.png (Normal), xpxd.png (Special)

## 🧮 Technische Details

- **DIN A4**: $2480 \times 3508$ Pixel bei 300 DPI
- **Bilder pro Reihe**: 6
- **Bilder pro Seite**: ~166 (6 Spalten × ~28 Reihen)
- **Duplex-Algorithmus**: 
  - Beide Seiten haben die gleiche Anzahl Bilder
  - Seite B wird automatisch horizontal gespiegelt
  - Perfekte Ausrichtung beim beidseitigen Druck garantiert
  - Multi-Page-Support bei großen Mengen
- **Bildaufteilung**: 50% A-Typ, 50% B-Typ
- **Zufällige Anordnung**: Bilder werden nach Wahrscheinlichkeit generiert und zufällig angeordnet

## 🎯 Verwendungsbeispiele

### Verschiedene Kartensätze

```bash
# Kleine Sets (Prototyping)
./cli.sh generate --total 166    # 1 Seite A + 1 Seite B

# Standard Sets
./cli.sh generate --total 500    # 2-3 Seiten pro Typ  
./cli.sh generate --total 1000   # 3-4 Seiten pro Typ

# Große Sets (Produktion)
./cli.sh generate --total 2000   # 6-7 Seiten pro Typ
./cli.sh generate --total 3000   # 9-10 Seiten pro Typ
```

### Verschiedene Anlässe

```bash
# Setup für verschiedene Anlässe
./cli.sh interactive  # Speichere als christmas_config.json
./cli.sh interactive  # Speichere als halloween_config.json

# Generierung mit verschiedenen Mengen
./cli.sh generate --config christmas_config.json --total 500
./cli.sh generate --config halloween_config.json --total 1000
```

### Batch-Verarbeitung

```bash
#!/bin/bash
# Script für automatische Generierung verschiedener Mengen

totals=(166 500 1000 2000)
for total in "${totals[@]}"; do
    ./cli.sh generate --total "$total" --config standard.json
    echo "Generated $total images"
done
```

## 🔧 Fehlerbehebung

### WSL Explorer Integration
```bash
# Nach der Generierung den Ordner öffnen
./cli.sh generate
explorer.exe .  # Öffnet Windows Explorer im aktuellen Verzeichnis
```

### Ungerade Anzahl
Das System korrigiert automatisch ungerade Zahlen:
```bash
# 1001 wird automatisch zu 1002
./cli.sh generate --total 1001
# ⚠️ Total images must be even. Using 1002 instead.
```

### Mehrseiten-Druck
Bei vielen Bildern entstehen mehrere Seiten:
```bash
# Beispiel: 2000 Bilder
# Ausgabe:
# - ludo_cards_page_A_1.png, page_A_2.png, ..., page_A_6.png
# - ludo_cards_page_B_1.png, page_B_2.png, ..., page_B_6.png
```

**Drucktipps:**
1. Drucke alle A-Seiten als einen Job
2. Die Reihenfolge merken (A_1 zuerst, A_6 zuletzt)
3. Stapel umdrehen und B-Seiten drucken
4. Darauf achten, dass B_1 auf die Rückseite von A_1 kommt

## 📝 Changelog

### Version 2.2 - Configurable Count
- 🔢 **Konfigurierbare Bildanzahl**: Standard 1000, muss gerade sein
- 📄 **Multi-Page-Support**: Automatisch mehrere Seiten bei Bedarf
- ✨ **Bessere CLI**: `--total` Option für schnelle Änderungen
- 📊 **Erweiterte Statistiken**: Seitenanzahl und Verteilung
- 🔄 **Intelligente Korrektur**: Ungerade Zahlen werden automatisch angepasst

### Version 2.1 - Duplex Edition
- 🖨️ **Duplex-Funktionalität**: Separate A- und B-Typ Seiten
- 🔄 **Automatische Spiegelung**: Seite B wird für perfekte Ausrichtung gespiegelt
- 🚀 **WSL-Integration**: `explorer.exe` Support für Windows-Ordner

### Version 2.0
- 📋 **Konfigurationsdatei**: Alle Argumente in JSON
- 🚀 **cli.sh Shortcut**: Automatisierte venv-Verwaltung

### Version 1.0  
- 🎨 GUI-Version mit tkinter
- 💻 Erste CLI-Version
- 📸 Gemischte PNG-Generierung

## 📄 Lizenz

MIT License

---

## 💡 Tipps für optimalen Duplex-Druck

### 1. **Bildanzahl planen:**
```bash
# Kleine Tests: 166 Bilder (1 Seite pro Typ)
./cli.sh generate --total 166

# Standard-Produktion: 1000 Bilder  
./cli.sh generate --total 1000

# Große Auflagen: 2000+ Bilder
./cli.sh generate --total 2000
```

### 2. **Drucker-Einstellungen:**
- Verwende hohe Qualität (300 DPI)
- Deaktiviere automatische Skalierung
- Stelle "Tatsächliche Größe" ein
- Bei mehreren Seiten: Stapelreihenfolge beachten

### 3. **Papier-Management:**
- Verwende qualitatives Papier (>160g/m²)
- Markiere die erste Seite für Orientierung
- Bei vielen Seiten: Seiten nummerieren

### 4. **Qualitätskontrolle:**
- Immer einen Testdruck mit 166 Bildern machen
- Ausrichtung prüfen bevor große Mengen gedruckt werden
- Erste und letzte Seite kontrollieren
