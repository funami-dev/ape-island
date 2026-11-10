# Ape Island – ein SCUMM-Durchstich

Minimales Adventure für ScummVM, gebaut mit [ScummC](https://github.com/AlbanBedel/scummc)
(SCUMM v6, Engine von Day of the Tentacle). Ziel: lernen, wie SCUMM den Spielablauf abbildet.

## Bauen
```bash
./build.sh
```
Die erzeugten Dateien (`*.000`, `*.001`) in einen Ordner legen und in ScummVM mit
„Spiel hinzufügen“ laden.

## Aufbau
- `game/` – Spielquellen (`.scc`)
- `docs/` – Erklärungen zum SCUMM-Modell
- `vendor/` – ScummC (wird von `build.sh` geholt, nicht eingecheckt)
