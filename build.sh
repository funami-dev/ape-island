#!/usr/bin/env bash
# Holt ScummC (auf festen Commit gepinnt), baut den Compiler und kompiliert game/.
# Benötigt: gcc, make, bison, flex, git
set -euo pipefail
cd "$(dirname "$0")"

SCUMMC_URL=https://github.com/AlbanBedel/scummc.git
SCUMMC_COMMIT=2f61ce0f7b5051e920876dc4b71935dc99f38fff

if [ ! -d vendor/scummc ]; then
  mkdir -p vendor
  git clone "$SCUMMC_URL" vendor/scummc
fi
git -C vendor/scummc checkout -q "$SCUMMC_COMMIT"

if [ ! -x vendor/scummc/build/scc ] && [ ! -x vendor/scummc/scc ]; then
  (cd vendor/scummc && ./configure && make -j"$(nproc)")
fi

echo "ScummC ist gebaut. Nächster Schritt (Spiel kompilieren) folgt, sobald game/ existiert."
