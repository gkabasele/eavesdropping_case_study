#! /bin/python

from bestPath import BestPath
from bhandari import Graph

if __name__=='__main__':
    

    graph = Graph()
    graph.addNode(1)
    graph.addNode(2)
    graph.addNode(3)
    graph.addNode(4)
    graph.addNode(5)
    graph.addNode(6) 
    graph.addNode(7)
    graph.addNode(8)

    graph.addVertex(1,2,1)
    graph.addVertex(1,5,1)
    graph.addVertex(2,3,1)
    graph.addVertex(3,4,1)
    graph.addVertex(4,5,1)
    graph.addVertex(4,6,1)
    graph.addVertex(4,8,1)
    graph.addVertex(5,6,1)
    graph.addVertex(6,7,1)
    graph.addVertex(7,8,1)

    path_computer = BestPath()

    best_paths = [[1,2,3,4,8,],[1,5,6,7,8]]

    paths = path_computer.n_paths(1,8,graph,2)
    for path in paths:
        assert path in best_paths


    graph2 = Graph()
    graph2.addNode(1)
    graph2.addNode(2)
    graph2.addNode(3)
    graph2.addNode(4)
    graph2.addNode(5)
    graph2.addNode(6)

    graph2.addVertex(1,2,1)
    graph2.addVertex(1,5,2)
    graph2.addVertex(2,3,1)
    graph2.addVertex(2,6,2)
    graph2.addVertex(3,4,1)
    graph2.addVertex(3,5,1)
    graph2.addVertex(4,6,1)

    path_computer = BestPath()

    best_paths = [[1,5,3,4],[1,2,6,4]]
    
    paths = path_computer.n_paths(1,4,graph2,2)
    for path in paths:
        assert path in best_paths

    graph3 = Graph()
    graph3.addNode(1)
    graph3.addNode(2)
    graph3.addNode(3)
    graph3.addNode(4)
    graph3.addNode(5)

    graph3.addVertex(1,2,1)
    graph3.addVertex(1,3,1)
    graph3.addVertex(1,4,1)
    graph3.addVertex(2,3,1)
    graph3.addVertex(2,5,1)
    graph3.addVertex(3,4,1)
    graph3.addVertex(3,5,1)
    graph3.addVertex(4,5,1)

    path_computer = BestPath()

    best_paths = [[1,2,5],[1,3,5],[1,4,5]]
    
    paths = path_computer.n_paths(1,5,graph3,3)
    for path in paths:
        assert path in best_paths



    #Only two disjoint path are possible
    graph4 = Graph()
    graph4.addNode(1)
    graph4.addNode(2)
    graph4.addNode(3)
    graph4.addNode(4)
    graph4.addNode(5)
    graph4.addNode(6)
    graph4.addNode(7)
    graph4.addNode(8)

    graph4.addVertex(1,2,1)
    graph4.addVertex(1,3,1)
    graph4.addVertex(1,4,1)
    graph4.addVertex(2,5,1)
    graph4.addVertex(3,5,1)
    graph4.addVertex(4,7,1)
    graph4.addVertex(5,6,1)
    graph4.addVertex(6,8,1)
    graph4.addVertex(7,8,1)

    path_computer = BestPath()

    best_paths = [[1,2,5,6,8],[1,4,7,8],[1,3,5,6,8]]
    paths = path_computer.n_paths(1,8,graph4,3)
    for path in paths:
        assert path in best_paths
