# Ludo PNG Mixer

Ein Python-Tool zum Mischen von A-Typ und B-Typ PNG-Bildern mit konfigurierbarer Seltenheitsverteilung.

## Features

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

## Installation

1. Repository klonen:
```bash
git clone https://github.com/LiTschii/Ludo_25_pngmixer.git
cd Ludo_25_pngmixer
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## Verwendung

1. Script starten:
```bash
python png_mixer.py
```

2. Bilder laden:
   - Lade alle 5 erforderlichen Bilder (alle müssen $500 \times 500$ Pixel PNG sein)
   - A-Typ: a.png, b.png, c.png
   - B-Typ: xp.png, xpxd.png

3. Konfiguration anpassen:
   - Verwende die Slider um die Seltenheitsverteilung anzupassen
   - A-Typ Prozentsätze müssen in Summe > 0 sein (werden automatisch normalisiert)
   - B-Typ Special-Chance bestimmt die Wahrscheinlichkeit für das Special-Motiv

4. PNG generieren:
   - Klicke "Generate Mixed PNG"
   - Wähle Speicherort für das Ergebnis

## Technische Details

- **DIN A4**: $2480 \times 3508$ Pixel bei 300 DPI
- **Bilder pro Reihe**: 6
- **Bild-Ratio**: Immer 1:1 (A-Typ : B-Typ)
- **Automatische Skalierung**: Bilder werden proportional an die verfügbare Fläche angepasst
- **Zufällige Anordnung**: Die generierten Bilder werden gemischt und zufällig angeordnet

## Lizenz

MIT License
