# Ludo PNG Mixer - Duplex Edition

Ein Python-Tool zum Erstellen von duplex-kompatiblen PNG-Bildern mit A-Typ und B-Typ Motiven für beidseitiges Drucken.

## 🖨️ Duplex-Funktionalität

**Neue Hauptfunktion:** Das Tool erstellt jetzt **zwei separate Seiten** für beidseitiges Drucken:
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
  - Verteilung der A-Typ Seltenheiten (Common/Uncommon/Legendary %)
  - B-Typ Special-Chance %
  - Alle Pfade und Einstellungen in JSON-Konfiguration

- **Duplex-Output**:
  - **Zwei separate PNG-Dateien**: `filename_page_A.png` und `filename_page_B.png`
  - DIN A4 Format (2480 x 3508 Pixel bei 300 DPI)
  - 6 Bilder pro Reihe
  - Automatische Spiegelung von Seite B für perfekte Ausrichtung beim Duplex-Druck

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

## 🖨️ Duplex-Druckprozess

1. **Generieren der Seiten:**
   ```bash
   ./cli.sh interactive  # Setup
   ./cli.sh generate     # Erstellt page_A.png und page_B.png
   ```

2. **Drucken:**
   - 📄 Drucke `page_A.png` (A-Typ Bilder)
   - 🔄 Lege das Papier umgedreht zurück in den Drucker
   - 📄 Drucke `page_B.png` (B-Typ Bilder, automatisch gespiegelt)
   - ✅ Die Bilder sind perfekt ausgerichtet!

## 💻 CLI-Version (Empfohlen)

### 🚀 Shortcut mit cli.sh

```bash
# Erstmalige Einrichtung
./cli.sh interactive

# Seiten generieren
./cli.sh generate

# Konfiguration anzeigen
./cli.sh config

# Hilfe anzeigen
./cli.sh --help
```

### 📋 Konfigurationsdatei

Beispiel `png_mixer_config.json`:

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
    "width": 2480,
    "height": 3508,
    "images_per_row": 6,
    "duplex_mode": true
  }
}
```

### 🎯 Empfohlener Workflow

```bash
# 1. Einmalig: Konfiguration erstellen
./cli.sh interactive
# -> Alle Bildpfade auswählen
# -> Wahrscheinlichkeiten festlegen
# -> Konfiguration speichern

# 2. Seiten generieren (wiederholbar)
./cli.sh generate
# -> Erstellt: ludo_cards_page_A.png und ludo_cards_page_B.png

# 3. Drucken und fertig!
```

### 🔧 Alle verfügbaren Befehle

```bash
# Interactive Setup
./cli.sh interactive

# Generiere Duplex-Seiten aus Config
./cli.sh generate
./cli.sh generate --config meine_config.json

# Verwalte Konfiguration
./cli.sh config

# Zeige Beispiele
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
- **Duplex-Algorithmus**: 
  - Beide Seiten haben die gleiche Anzahl Bilder
  - Seite B wird automatisch horizontal gespiegelt
  - Perfekte Ausrichtung beim beidseitigen Druck garantiert
- **Zufällige Anordnung**: Bilder werden nach Wahrscheinlichkeit generiert und zufällig angeordnet

## 🎯 Verwendungsbeispiele

### Einfache Anwendung
```bash
# Alles in einem Schritt
./cli.sh interactive
# -> Führt durch: Bilder auswählen, Einstellungen, Generierung
# -> Ergebnis: page_A.png und page_B.png
```

### Verschiedene Kartensätze
```bash
# Setup für verschiedene Anlässe
./cli.sh interactive  # Speichere als christmas_config.json
./cli.sh interactive  # Speichere als halloween_config.json

# Schnelle Generierung
./cli.sh generate --config christmas_config.json
./cli.sh generate --config halloween_config.json
```

### Batch-Verarbeitung
```bash
#!/bin/bash
# Script für automatische Generierung

configs=("standard" "promo" "special")
for config in "${configs[@]}"; do
    ./cli.sh generate --config "${config}_config.json"
    echo "Generated ${config} cards"
done
```

## 🔧 Fehlerbehebung

### WSL Explorer Integration
```bash
# Nach der Generierung den Ordner öffnen
./cli.sh generate
explorer.exe .  # Öffnet Windows Explorer im aktuellen Verzeichnis
```

### Duplex-Testdruck
1. Drucke zuerst nur Seite A
2. Prüfe die Ausrichtung
3. Lege das Papier korrekt ein (beachte die Druckerrichtung)
4. Drucke Seite B
5. Überprüfe die Ausrichtung der Bilder

### Konfigurationsprobleme
```bash
# Reset der Konfiguration
rm png_mixer_config.json
./cli.sh interactive  # Neue Einrichtung

# Konfiguration anzeigen
./cli.sh config
```

## 📝 Changelog

### Version 2.1 - Duplex Edition
- 🖨️ **Duplex-Funktionalität**: Separate A- und B-Typ Seiten
- 🔄 **Automatische Spiegelung**: Seite B wird für perfekte Ausrichtung gespiegelt  
- ✨ **Verbesserte CLI**: Klarere Befehle und besseres Feedback
- 📊 **Duplex-Statistiken**: Übersicht über beide Seiten
- 🚀 **WSL-Integration**: `explorer.exe` Support für Windows-Ordner

### Version 2.0
- 📋 **Konfigurationsdatei**: Alle Argumente in JSON
- 🚀 **cli.sh Shortcut**: Automatisierte venv-Verwaltung
- 🔧 **Verbesserte Struktur**: Getrennte Befehle für Setup und Generierung

### Version 1.0  
- 🎨 GUI-Version mit tkinter
- 💻 Erste CLI-Version
- 📸 Gemischte PNG-Generierung

## 📄 Lizenz

MIT License

---

## 💡 Tipps für perfekten Duplex-Druck

1. **Drucker-Einstellungen:**
   - Verwende hohe Qualität (300 DPI)
   - Deaktiviere automatische Skalierung
   - Stelle "Tatsächliche Größe" ein

2. **Papier:**
   - Verwende qualitatives, schweres Papier (>160g/m²)
   - Markiere die Vorderseite mit einem Bleistiftpunkt

3. **Test:**
   - Mache immer einen Testdruck mit nur 1 Paar
   - Überprüfe die Ausrichtung vor dem Hauptdruck
   - Notiere die richtige Papierrichtung für deinen Drucker

4. **Schneiden:**
   - Die Karten sind automatisch richtig angeordnet
   - Schneide entlang der Rasterlinien
   - Jede Karte hat die A-Seite und B-Seite perfekt ausgerichtet
