from unittest import TestCase

from src.DiGraph import DiGraph


class TestDiGraph(TestCase):

    global graph

    def setUp(self) -> None:
        """
        initialize the graph for the tests
        """
        g = DiGraph()
        for i in range(6):
            g.add_node(i)

        g.add_edge(1, 2, 2)
        g.add_edge(1, 3, 2)
        g.add_edge(1, 4, 2)
        g.add_edge(1, 5, 2)
        g.add_edge(1, 0, 2)

        g.add_edge(0, 3, 2)

        self.graph = g


    def test_a(self):
        """
        test the get sizes functions
        """
        self.assertEqual(6, self.graph.v_size())
        self.assertEqual(6, self.graph.e_size())
        self.assertEqual(12, self.graph.get_mc())

    def test_b(self):
        """
        test the add edge function
        """
        self.assertEqual(False, self.graph.add_edge(0, 9, 2))
        self.assertEqual(False, self.graph.add_edge(0, 2, -2))
        self.assertEqual(True, self.graph.add_edge(0, 5, 3))
        self.assertEqual(13, self.graph.get_mc())

    def test_c(self):
        """
        test the add node function
        """
        self.assertEqual(False, self.graph.add_node(2))
        self.assertEqual(True, self.graph.add_node(6))
        self.assertEqual(13, self.graph.get_mc())

    def test_d(self):
        """
        test the remove node function
        """
        self.assertEqual(True, self.graph.add_node(6))
        self.assertEqual(False, self.graph.remove_node(9))
        self.assertEqual(True, self.graph.remove_node(6))
        self.assertEqual(14, self.graph.get_mc())
        self.assertEqual(True, self.graph.remove_node(0))
        self.assertEqual(17, self.graph.get_mc())

    def test_e(self):
        """
        test the remove edge function
        """
        self.assertEqual(False, self.graph.remove_edge(3, 9))
        self.assertEqual(False, self.graph.remove_edge(4, 5))
        self.assertEqual(12, self.graph.get_mc())
        self.assertEqual(True, self.graph.remove_edge(1, 3))
        self.assertEqual(13, self.graph.get_mc())