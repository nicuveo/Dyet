# Makefile for dyet


SRC =					\
        src/tools/graph.py		\
        src/tools/image.py		\
        src/tools/image_builder.py	\
        src/tools/list_utils.py		\
        src/tools/math_utils.py		\
        src/decorators/assertions.py	\
        src/decorators/decorator.py	\
        src/decorators/empty.py		\
        src/decorators/enable.py	\
        src/decorators/main.py		\
        src/decorators/virtual.py	\
        src/blocks.py			\
        src/cells.py			\
        src/colors.py			\
        src/commands.py			\
        src/instructions.py		\
        src/parser.py			\
        src/patterns.py			\


all: $(SRC)

$(SRC):
	PYTHONPATH="src" /usr/bin/env python3 $@

.PHONY: $(SRC)


