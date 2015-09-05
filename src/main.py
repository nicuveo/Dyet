# main.py
#
# This file is the entry point for the program.



##########################################
# Imports

import sys
import parser
import colors

from tools.graph import Graph
from tools.image import Image
from color import Colors
from command import Commands
from block import *



##########################################
# Declarations

def render(block_list):
    size = block_list.minimum_size()
    return block_list.render(size[0], size[1]).to_ppm_string()

def close(block_list):
    if block_list.blocks and block_list.blocks[-1].command != Commands.NOOP:
        block_list.blocks.append(NoopBlock())


def main(args):
    input_file = args[1]
    resulting_prog = BlockList()
    scope = [resulting_prog]
    container_scope = []

    with open(input_file, 'r') as f:
        for argv in parser.parse(f.read()):
            command = argv[0].lower()

            if command == "if":
                if_block = IfBlock()
                scope[-1].blocks.append(if_block)
                container_scope.append(if_block)
                scope.append(if_block.if_block)
            elif command == "while":
                while_block = WhileBlock()
                scope[-1].blocks.append(while_block)
                container_scope.append(while_block)
                scope.append(while_block.while_block)
            elif command == "else":
                if_block = container_scope[-1]
                close(scope.pop())
                scope.append(if_block.else_block)
            elif command == "end":
                close(scope.pop())
                container_scope.pop()
            elif command == "exit":
                scope[-1].blocks.append(EndBlock())
            elif command == "print":
                bl = BlockList()
                ow = WhileBlock()
                bl.blocks.append(LeafBlock(Commands.PUSH))
                bl.blocks.append(LeafBlock(Commands.NOT))
                for char in [char for char in reversed(" ".join(argv[1:]).replace("\\n", "\n").replace("\ ", " "))]:
                    bl.blocks.append(LeafBlock(Commands.PUSH, ord(char)))
                bl.blocks.append(ow)
                ow.while_block.blocks.append(LeafBlock(Commands.OUT_CHAR))
                ow.while_block.blocks.append(NoopBlock())
                bl.blocks.append(LeafBlock(Commands.POP))
                scope[-1].blocks.append(bl)
            elif command in Commands.map.keys() and not command in [Commands.POINTER, Commands.SWITCH, Commands.NOOP]:
                cmd = Commands.map[command]
                if len(argv) > 1:
                    scope[-1].blocks.append(LeafBlock(cmd, int(argv[1])))
                else:
                    scope[-1].blocks.append(LeafBlock(cmd))
            else:
                print("Unknown token '" + command + "'")
                exit(1)

        assert(len(scope) == 1)
        resulting_prog.blocks.append(EndBlock())
        resulting_prog.colorize(Colors.R0)
        print(render(resulting_prog))



##########################################
# Main

if __name__ == "__main__":
    main(sys.argv)
