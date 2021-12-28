import os
from random import random, randint
from unittest import TestCase

from src.GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
    global graph
    def test_load_from_json(self):
        g = GraphAlgo()
        self.assertEqual(True, g.load_from_json("testData\A0.json"))
        self.assertEqual(11, g.get_graph().v_size())
        self.assertEqual(False, g.load_from_json("testData\error.json"))
        self.assertEqual(11, g.get_graph().v_size())
        self.assertEqual(True, g.load_from_json("testData\A5.json"))
        self.assertEqual(48, g.get_graph().v_size())

    def test_save_to_json(self):
        g = GraphAlgo()
        g.load_from_json("testData/A0.json")
        g.get_graph().remove_node(4)
        self.assertEqual(True, g.save_to_json("testData/savetest.json"))
        f = GraphAlgo()
        self.assertEqual(True, f.load_from_json("testData/savetest.json"))
        self.assertEqual(10, f.get_graph().v_size())
        f.get_graph().remove_node(0)
        self.assertEqual(False, f.save_to_json(412))
        self.assertEqual(True, f.save_to_json("testData/savetest.json"))
        g.load_from_json("testData/savetest.json")
        self.assertEqual(9, g.get_graph().v_size())

    def test_shortest_path(self):
        g = GraphAlgo()
        for i in range(6):
            g.get_graph().add_node(i)

        g.get_graph().add_edge(0, 2, 9)
        g.get_graph().add_edge(5, 4, 100)
        g.get_graph().add_edge(4, 5, 100)
        g.get_graph().add_edge(0, 3, 13)
        g.get_graph().add_edge(2, 3, 1)
        g.get_graph().add_edge(3, 2, 1)
        g.get_graph().add_edge(5, 1, 0.5)
        g.get_graph().add_edge(1, 4, 0.5)
        g.get_graph().add_edge(3, 5, 10)

        self.assertEqual(11, g.shortest_path(3, 4)[0])

    def test_tsp(self):
        g = GraphAlgo()
        for i in range(6):
            g.get_graph().add_node(i)

        g.get_graph().add_edge(0, 2, 9)
        g.get_graph().add_edge(5, 4, 100)
        g.get_graph().add_edge(4, 5, 100)
        g.get_graph().add_edge(0, 3, 13)
        g.get_graph().add_edge(2, 3, 1)
        g.get_graph().add_edge(3, 2, 1)
        g.get_graph().add_edge(5, 1, 0.5)
        g.get_graph().add_edge(1, 4, 0.5)
        g.get_graph().add_edge(3, 5, 10)

        self.assertEqual(([0, 2, 3, 5, 1, 4], 21.0), g.TSP([0, 2, 3, 4]))

    def test_center_point(self):
        g = GraphAlgo()
        center_list = [7, 8, 0, 2, 6, 40]
        for i in range(6):
            g.load_from_json("testData/A"+str(i)+".json")
            self.assertEqual(center_list[i], g.centerPoint()[0])