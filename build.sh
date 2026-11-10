#!/usr/bin/env bash
# Holt ScummC (auf festen Commit gepinnt), baut den Compiler und kompiliert game/.
# Benötigt: gcc, make, bison, flex, git, iconv
set -euo pipefail
cd "$(dirname "$0")"

SCUMMC_URL=https://github.com/AlbanBedel/scummc.git
SCUMMC_COMMIT=2f61ce0f7b5051e920876dc4b71935dc99f38fff

if [ ! -d vendor/scummc ]; then
  mkdir -p vendor
  git clone "$SCUMMC_URL" vendor/scummc
fi
git -C vendor/scummc checkout -q "$SCUMMC_COMMIT"

# Am gepinnten Commit liegen die Man-Pages in man/tools/, das Makefile sucht
# die XML-Dateien für die eingebaute Hilfe (scc_help.h usw.) aber in man/.
# Ohne diese Links bricht der Build mit "No rule to make target 'scc_help.h'" ab.
for f in vendor/scummc/man/tools/*.xml; do
  ln -sf "tools/$(basename "$f")" "vendor/scummc/man/$(basename "$f")"
done

# Die Binaries landen in vendor/scummc/build.<host>/<target>/
if ! ls vendor/scummc/build.*/*/scc >/dev/null 2>&1; then
  (cd vendor/scummc && ./configure && make -j"$(nproc)")
fi

make -C game

echo
echo "Fertig: game/build/tentacle.000 und game/build/tentacle.001"
echo "In ScummVM über 'Spiel hinzufügen' den Ordner game/build wählen"
echo "(wird als Day of the Tentacle erkannt)."
