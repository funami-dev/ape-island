# Ape Island - Makefile nach dem Vorbild von ScummCs examples/road
#
#   make            baut build/tentacle.000/.001 (läuft in
#                   unverändertem ScummVM als "Day of the Tentacle")
#   make scummc6    baut build/scummc6.000/.001 (für ein ScummVM mit
#                   ScummC-Patch, siehe vendor/scummc/patches)
#   make assets     Grafiken neu erzeugen (benötigt python3 + Pillow)
#   make clean

SCUMMC_DIR ?= ../vendor/scummc
BIN_DIR    ?= $(patsubst %/,%,$(firstword $(wildcard $(SCUMMC_DIR)/build.*/*/)))
INC_DIR    ?= $(SCUMMC_DIR)/include

SCC  = $(BIN_DIR)/scc
SLD  = $(BIN_DIR)/sld
COST = $(BIN_DIR)/cost
CHAR = $(BIN_DIR)/char

ASSETS = assets
B      = build

SRCS  = common.scc beach.scc
HDRS  = common.sch
OBJS  = $(SRCS:%.scc=$(B)/%.roobj)
CHARS = $(B)/vera-gui.char $(B)/vera.char $(B)/vera-small.char
COSTS = $(B)/devil.cost

# Die Quellen sind UTF-8, die Schriften (vera*.bmp) sind Latin-1:
# vor dem Kompilieren umwandeln.
LATIN1 = $(SRCS:%=$(B)/src/%) $(HDRS:%=$(B)/src/%)

SCC_FLAGS = -V 6 -I $(INC_DIR) -I $(B)/src -R $(B) -R $(ASSETS)

all: tentacle

tentacle: $(B)/tentacle.000 $(B)/tentacle.001
scummc6:  $(B)/scummc6.000 $(B)/scummc6.001

$(B) $(B)/src:
	mkdir -p $@

$(B)/src/%: % | $(B)/src
	iconv -f UTF-8 -t ISO-8859-1 $< > $@

$(B)/%.char: $(ASSETS)/%.bmp | $(B)
	$(CHAR) -ochar $@ -ibmp $<

$(B)/%.cost: $(ASSETS)/%.scost | $(B)
	$(COST) -o $@ -I $(ASSETS) -header $(B)/$*_anim.sch -prefix $*_anim_ $<

# Das Spiel hat keine Sounds, daher erzeugt sld keine .sou-Datei.

# Jede .roobj hängt von allen Headern, Schriften und Costumes ab - bei zwei
# Quelldateien ist das einfacher als scc -d.
$(B)/%.roobj: $(B)/src/%.scc $(LATIN1) $(CHARS) $(COSTS) $(wildcard $(ASSETS)/*)
	$(SCC) -o $@ $(SCC_FLAGS) $<

$(B)/tentacle.000: $(OBJS)
	$(SLD) -o $(B)/tentacle -key 0x69 $^
$(B)/tentacle.001: $(B)/tentacle.000 ;

$(B)/scummc6.000: $(OBJS)
	$(SLD) -o $(B)/scummc6 $^
$(B)/scummc6.001: $(B)/scummc6.000 ;

assets:
	python3 tools/gen_assets.py $(SCUMMC_DIR)/examples/road

clean:
	rm -rf $(B)

.PHONY: all tentacle scummc6 assets clean
.SECONDARY:
