# main.py
#
# This file is the entry point for the program.



########## Declarations ##########

import sys
import parser
import color

from tools.graph import Graph
from tools.image import Image
from color import Colors
from command import Commands



########## Declarations ##########

class Node:
    def __init__(self, size):
        self.size = size
        self.color = None

class Edge:
    def __init__(self, cmd):
        self.cmd = cmd


def main(args):
    input_file = args[1]
    with open(input_file, 'r') as f:
        g = Graph()
        last_node = Node(0)
        start_node = last_node
        g.add_node(last_node)

        for argv in parser.parse(f.read()):
            cmd = Commands.map[argv[0].lower()]
            new_node = Node(0)

            if cmd == Commands.PUSH:
                last_node.size = int(argv[1])

            g.add_node(new_node)
            g.add_edge(last_node, new_node, cmd)
            last_node = new_node

        start_node.color = Colors.R0
        seen_nodes = [start_node]
        current_edges = g.out_edges(start_node)

        while current_edges:
            (source, target, cmd) = current_edges[0]
            current_edges.pop(0)
            target.color = color.command_next(source.color, cmd)
            for edge in g.out_edges(target):
                if not edge[1] in seen_nodes:
                    seen_nodes.append(edge[1])
                    current_edges.append(edge)

        width = len(g.nodes()) + 1
        height = max(3, max(n.size + 2 for n in g.nodes()))
        res = Image(width, height, (0, 0, 0))

        node = start_node
        column = 1
        while True:
            for row in range(1, max(2, 1 + node.size)):
                res.pixel_set(column, row, node.color.rgb())
            column += 1
            out_edges = g.out_edges(node)
            next_node = out_edges[0][1] if out_edges else None
            if not next_node:
                break
            node = next_node

        c1 = color.command_prev(start_node.color, Commands.POP)
        res.pixel_set(0, 0, c1.rgb())
        res.pixel_set(0, 1, c1.rgb())
        for row in range(0, height):
            res.pixel_set(width - 1, row, node.color.rgb())

        with open("out.ppm", 'w') as out:
            out.write(res.to_ppm_string())



########## Main ##########

if __name__ == "__main__":
    main(sys.argv)
