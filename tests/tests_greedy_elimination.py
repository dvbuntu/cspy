import unittest
from time import time

from networkx import DiGraph, complete_graph
from numpy import array
from parameterized import parameterized

from cspy import GreedyElim


class TestsGreedyElimination(unittest.TestCase):
    """
    Tests for finding the resource constrained shortest
    path of simple DiGraph using the BiDirectional algorithm.
    Includes algorithm classification, and some exception handling.
    """

    def setUp(self):
        # Maximum and minimum resource arrays
        self.max_res, self.min_res = [4, 20], [0, 0]
        # Create simple digraph with appropriate attributes
        self.G = DiGraph(directed=True, n_res=2)
        self.G.add_edge('Source', 'A', res_cost=array([1, 2]), weight=-1)
        self.G.add_edge('A', 'B', res_cost=array([1, 0.3]), weight=-1)
        self.G.add_edge('B', 'C', res_cost=array([1, 3]), weight=-10)
        self.G.add_edge('B', 'Sink', res_cost=array([1, 2]), weight=10)
        self.G.add_edge('C', 'Sink', res_cost=array([1, 10]), weight=-1)

        self.result_path = ['Source', 'A', 'B', 'C', 'Sink']
        self.total_cost = -13
        self.consumed_resources = [4, 15.3]

    def test_simple(self):
        'algorithm = "simple" (default)'
        alg = GreedyElim(self.G, self.max_res, self.min_res)
        alg.run()
        self.assertEqual(alg.path, self.result_path)
        self.assertEqual(alg.total_cost, self.total_cost)
        self.assertTrue(all(alg.consumed_resources == self.consumed_resources))

    def test_astar(self):
        'algorithm = "astar"'
        alg = GreedyElim(self.G, self.max_res, self.min_res, algorithm="astar")
        alg.run()
        self.assertEqual(alg.path, self.result_path)
        self.assertEqual(alg.total_cost, self.total_cost)
        self.assertTrue(all(alg.consumed_resources == self.consumed_resources))

    def test_time_limit(self):
        'time limit parameter'
        alg = GreedyElim(self.G, self.max_res, self.min_res, time_limit=0.001)
        start = time()
        alg.run()
        self.assertTrue(time() - start <= 0.001)
        self.assertEqual(alg.path, self.result_path)
        self.assertEqual(alg.total_cost, self.total_cost)
        self.assertTrue(all(alg.consumed_resources == self.consumed_resources))

    def test_threshold(self):
        'test threshold parameter'
        alg = GreedyElim(self.G, self.max_res, self.min_res, threshold=100)
        alg.run()
        self.assertEqual(alg.path, ["Source", "A", "B", "Sink"])
        self.assertEqual(alg.total_cost, 8)
        self.assertTrue(all(alg.consumed_resources == [3, 4.3]))

    def test_time_limit_threshold(self):
        'time limit and threshold parameters'
        alg = GreedyElim(self.G,
                         self.max_res,
                         self.min_res,
                         time_limit=0.001,
                         threshold=100)
        start = time()
        alg.run()
        self.assertTrue(time() - start <= 0.001)
        self.assertEqual(alg.path, ["Source", "A", "B", "Sink"])
        self.assertEqual(alg.total_cost, 8)
        self.assertTrue(all(alg.consumed_resources == [3, 4.3]))

    def test_time_limit_raises(self):
        'Time limit of 0 raises an exception'
        alg = GreedyElim(self.G, self.max_res, self.min_res, time_limit=0)
        self.assertRaises(Exception, alg.run)
