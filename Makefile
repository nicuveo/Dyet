# Makefile for dyet


SRC =			\
./src/tools/graph.py	\
./src/tools/image.py	\
./src/command.py	\
./src/parser.py		\
./src/color.py		\
./src/block.py		\


all: $(SRC)

$(SRC):
	/usr/bin/env python3 $@

.PHONY: $(SRC)
