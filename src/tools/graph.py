# graph.py
#
# This class represents a directed graph,
# implemented as an adjacency list.



########## Declarations ##########

class Graph:
    def __init__(self):
        self.__adjacency_maps = {}

    def nodes(self):
        return self.__adjacency_maps.keys()
    def edges(self):
        for (source, adjacency_map) in self.__adjacency_maps.items():
            for (target, edge) in adjacency_map.items():
                yield (source, target, edge)

    def edge(self, source, target):
        return self.__adjacency_maps[source][target]

    def preds(self, node):
        return [source for (source, target, _) in self.edges() if target == node]
    def in_edges(self, node):
        return [edge for edge in self.edges() if edge[1] == node]
    def succs(self, node):
        return self.__adjacency_maps[node].keys()
    def out_edges(self, node):
        return [edge for edge in self.edges() if edge[0] == node]

    def add_node(self, node):
        if not node in self.__adjacency_maps:
            self.__adjacency_maps[node] = {}
    def add_edge(self, source, target, edge):
        self.__adjacency_maps[source][target] = edge



########## Unit tests ##########

if __name__ == "__main__":
    import unittest

    class GraphTest(unittest.TestCase):
        def setUp(self):
            self.graph = Graph()
            self.graph.add_node(1)
            self.graph.add_node(1)
            self.graph.add_node(2)
            self.graph.add_node(3)
            self.graph.add_edge(1, 2,  1)
            self.graph.add_edge(2, 3,  1)
            self.graph.add_edge(1, 3,  2)
            self.graph.add_edge(3, 1, -2)
            self.graph.add_edge(1, 2,  1)

        def test_add_node(self):
            g = Graph()
            g.add_node(1)
            self.assertEqual(1, len(g.nodes()))
            g.add_node(2)
            self.assertEqual(2, len(g.nodes()))
            g.add_node(1)
            self.assertEqual(2, len(g.nodes()))

        def test_add_edge(self):
            self.assertEqual(4, len(list(self.graph.edges())))
            self.assertEqual(1, self.graph.edge(1, 2))

        def test_in_edges(self):
            self.assertEqual(1, len(self.graph.in_edges(1)))
            self.assertEqual(1, len(self.graph.in_edges(2)))
            self.assertEqual(2, len(self.graph.in_edges(3)))

        def test_out_edges(self):
            self.assertEqual(2, len(self.graph.out_edges(1)))
            self.assertEqual(1, len(self.graph.out_edges(2)))
            self.assertEqual(1, len(self.graph.out_edges(3)))

    unittest.main(verbosity = 0)
