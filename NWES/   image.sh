#!/bin/bash

# Prüfen, ob ein Bild als Argument übergeben wurde
if [ $# -ne 1 ]; then
  echo "Verwendung: $0 <bilddatei>"
  exit 1
fi

bild="$1"

# Prüfen, ob die Datei existiert
if [ ! -f "$bild" ]; then
  echo "Datei '$bild' existiert nicht!"
  exit 2
fi

# Änderungsdatum der Datei auslesen
datum=$(date -r "$bild" +"%Y-%m-%d_%H-%M-%S")

# Ordnername aus Datum erstellen
ordner="Bilder_${datum}"

# Ordner erstellen, falls er nicht existiert
mkdir -p "$ordner"

# Bild in den Ordner verschieben
mv "$bild" "$ordner"

echo "Bild wurde in den Ordner '$ordner' verschoben."