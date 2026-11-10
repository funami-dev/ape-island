#!/usr/bin/env bash
# Holt ScummC (auf festen Commit gepinnt), baut den Compiler und kompiliert game/.
# Benötigt: gcc, make, bison >= 2.7, flex, git, iconv
# macOS: brew install bison  (wird automatisch gefunden)
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

# ScummC braucht Bison >= 2.7. macOS liefert nur Bison 2.3 mit; das von
# Homebrew ist "keg-only" und liegt nicht im PATH, also selbst einhängen.
if command -v brew >/dev/null 2>&1; then
  BREW_BISON="$(brew --prefix bison 2>/dev/null)/bin"
  if [ -x "$BREW_BISON/bison" ]; then
    export PATH="$BREW_BISON:$PATH"
  fi
fi
if [ "$(uname)" = Darwin ] && bison --version | head -1 | grep -q ' 2\.[0-6]\b\| 2\.[0-6]$'; then
  echo "Bison ist zu alt ($(bison --version | head -1))." >&2
  echo "Bitte installieren:  brew install bison" >&2
  exit 1
fi

JOBS="$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)"

# Die Binaries landen in vendor/scummc/build.<host>/<target>/
if ! ls vendor/scummc/build.*/*/scc >/dev/null 2>&1; then
  (cd vendor/scummc && ./configure && make -j"$JOBS")
fi

make -C game

echo
echo "Fertig: game/build/tentacle.000 und game/build/tentacle.001"
echo "In ScummVM über 'Spiel hinzufügen' den Ordner game/build wählen"
echo "(wird als Day of the Tentacle erkannt)."
