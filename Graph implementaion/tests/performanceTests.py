from random import randint

from src.GraphAlgo import GraphAlgo
from time import time

def pathPerformance():
    g = GraphAlgo()
    g.load_from_json("testData/1M.json")
    s = time()
    x = g.shortest_path(4, 888)
    f = time()
    overall = f-s
    print("finished in ", overall, " | Path: ", x, " | On graph ", g.name)

def tspPerformance():
    g = GraphAlgo()
    g.load_from_json("testData/1m.json")
    s = time()
    x = g.TSP([4, 5, 313, 888])
    f = time()
    overall = f-s
    print("finished in ", overall, " | TSP Path: ", x, " | On graph ", g.name)

def loadPerformance():
    g = GraphAlgo()

    s = time()
    b = g.load_from_json("testData/100k.json")
    f = time()

    overall = f-s
    print("finished in ", overall, " | Did it load? ", b, " | On graph ", g.name)

def savePerformance():
    g = GraphAlgo()
    g.load_from_json("testData/1m.json")
    s = time()
    b = g.save_to_json("testData/savePerformance.json")
    f = time()

    overall = f-s
    print("finished in ", overall, " | Did it save? ", b, " | On graph ", g.name)

def centerPerformance():
    g = GraphAlgo()
    g.load_from_json("testData/1k.json")
    s = time()
    x = g.centerPoint()
    f = time()

    overall = f-s
    print("finished in ", overall, "\n center is ", x, "\n On graph ", g.name)

def createK(k: int):
    nodesize = 1000*k
    g = GraphAlgo()
    for i in range(nodesize):
        g.get_graph().add_node(i)

    for i in range(nodesize):
        for j in range(10):
            dest = randint(0,nodesize)
            w = randint(1, 5)
            g.get_graph().add_edge(i, dest, w)
    g.save_to_json("testData/-INSERT NEW NAME HERE-.json")


if __name__ == '__main__':
   tspPerformance()