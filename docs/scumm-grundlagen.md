# Wie SCUMM ein Spiel abbildet

- **Room**: ein Bildschirm mit Hintergrundbild, Walk-Boxes (begehbare Fläche), Objekten, Entry-/Exit-Scripts.
- **Object**: Hotspot im Raum mit Name, Position, Zuständen (Bilder) und einem `verb`-Handler.
- **Actor**: Figur mit Costume (Animation). `ego` ist der Spieler.
- **Verb**: Aktion (LookAt, PickUp, Use, TalkTo ...). Ein Klick bildet einen Satz: Verb + Objekt A (+ Objekt B).
- **Script**: Bytecode, der im Cooperative-Multitasking als Threads läuft (`startScript`, `breakHere`).
  Cutscenes unterbrechen die Spielersteuerung.
- **Variablen**: global (`VAR_*`, Bits, Ints) – so wird der Spielzustand gespeichert.
- **Dateien**: `.000` = Index (Verzeichnisse), `.001` = Daten (Räume, Scripts, Sounds).
