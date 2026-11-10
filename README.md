# Ape Island – ein SCUMM-Durchstich

Minimales Adventure für ScummVM, gebaut mit [ScummC](https://github.com/AlbanBedel/scummc)
(SCUMM v6, Engine von Day of the Tentacle). Ziel: lernen, wie SCUMM den Spielablauf abbildet.

## Das Spiel
Ein Raum, ein Strand, ein Affe. Beasty sucht den Schatz von Ape Island:
Palme schütteln (Drück/Zieh), Kokosnuss nehmen, sie dem Affen geben – dann
lässt er dich an die Schatztruhe.

## Bauen
```bash
./build.sh
```
Benötigt gcc, make, bison, flex, git und iconv. Das Skript holt und baut ScummC
und kompiliert danach `game/` (alternativ `make -C game`).

Ergebnis: `game/build/tentacle.000` und `game/build/tentacle.001`. In ScummVM
über „Spiel hinzufügen“ den Ordner `game/build` wählen – ein unverändertes
ScummVM erkennt das Spiel als *Day of the Tentacle* (die Warnung zur unbekannten
Version kann man ignorieren). `make -C game scummc6` baut die Variante für ein
ScummVM mit ScummC-Patch.

## Aufbau
- `game/` – Spielquellen (`.scc`), nach dem Vorbild von ScummCs `examples/road`
  - `common.scc/.sch` – Verben, Inventar, Dialogsystem, `main` (aus road übernommen, eingedeutscht)
  - `beach.scc` – der Strand mit Palme, Kokosnuss, Affe und Truhe
  - `assets/` – Grafiken; `tools/gen_assets.py` erzeugt sie (`make -C game assets`, braucht Pillow)
- `docs/` – Erklärungen zum SCUMM-Modell
- `vendor/` – ScummC (wird von `build.sh` geholt, nicht eingecheckt)

Schriften, Cursor und der Teufel-Costume stammen aus dem road-Beispiel von ScummC
und stehen wie ScummC unter der GPL v2.
