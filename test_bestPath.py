#! /bin/python
import cProfile, pstats, StringIO

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

    graph.addEdge(1,2,1,1)
    graph.addEdge(1,5,1,1)
    graph.addEdge(2,3,1,1)
    graph.addEdge(3,4,1,1)
    graph.addEdge(4,5,1,1)
    graph.addEdge(4,6,1,1)
    graph.addEdge(4,8,1,1)
    graph.addEdge(5,6,1,1)
    graph.addEdge(6,7,1,1)
    graph.addEdge(7,8,1,1)

    path_computer = BestPath()

    best_paths = [[1,2,3,4,8,],[1,5,6,7,8]]
    #only two disjoints path are possible

    paths = path_computer.n_paths(1,8,graph,3)
    for path in paths:
        assert path in best_paths

    graph2 = Graph()
    graph2.addNode(1)
    graph2.addNode(2)
    graph2.addNode(3)
    graph2.addNode(4)
    graph2.addNode(5)
    graph2.addNode(6)

    graph2.addEdge(1,2,1,1)
    graph2.addEdge(1,5,2,1)
    graph2.addEdge(2,3,1,1)
    graph2.addEdge(2,6,2,1)
    graph2.addEdge(3,4,1,1)
    graph2.addEdge(3,5,1,1)
    graph2.addEdge(4,6,1,1)

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

    graph3.addEdge(1,2,1,1)
    graph3.addEdge(1,3,1,1)
    graph3.addEdge(1,4,1,1)
    graph3.addEdge(2,3,1,1)
    graph3.addEdge(2,5,1,1)
    graph3.addEdge(3,4,1,1)
    graph3.addEdge(3,5,1,1)
    graph3.addEdge(4,5,1,1)

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

    graph4.addEdge(1,2,1,1)
    graph4.addEdge(1,3,1,1)
    graph4.addEdge(1,4,1,1)
    graph4.addEdge(2,5,1,1)
    graph4.addEdge(3,5,1,1)
    graph4.addEdge(4,7,1,1)
    graph4.addEdge(5,6,1,1)
    graph4.addEdge(6,8,1,1)
    graph4.addEdge(7,8,1,1)

    path_computer = BestPath()

    best_paths = [[1,2,5,6,8],[1,4,7,8]]
    paths = path_computer.n_paths(1,8,graph4,3)
    for path in paths:
        assert path in best_paths
    graph5 = Graph()
    graph5.addNode(1)
    graph5.addNode(2)
    graph5.addNode(3)
    graph5.addNode(4)
    graph5.addNode(5)
    graph5.addNode(6)
    graph5.addNode(7)
    graph5.addNode(8)
    graph5.addNode(9)
    graph5.addNode(10)

    graph5.addEdge(1,2,1,1)
    graph5.addEdge(1,3,1,1)
    graph5.addEdge(1,6,1,1)
    graph5.addEdge(1,9,1,1)
    graph5.addEdge(1,10,1,1)
    graph5.addEdge(2,3,1,1)
    graph5.addEdge(3,4,1,1)
    graph5.addEdge(3,8,1,1)
    graph5.addEdge(4,5,1,1)
    graph5.addEdge(4,6,1,1)
    graph5.addEdge(4,9,1,1)
    graph5.addEdge(5,6,1,1)
    graph5.addEdge(6,7,1,1)
    graph5.addEdge(6,8,1,1)
    graph5.addEdge(7,8,1,1)
    graph5.addEdge(8,9,1,1)
    graph5.addEdge(9,10,1,1)

    path_computer = BestPath()

    best_paths = [[10,9,4],[10,1,3,4]]
    paths = path_computer.n_paths(10,4,graph5,3)
    for path in paths:
        assert path in best_paths

    graph6 = Graph()
    graph6.addNode(1)
    graph6.addNode(2)
    graph6.addNode(3)
    graph6.addNode(4)
    graph6.addNode(5)
    graph6.addNode(6)
    graph6.addNode(7)

    graph6.addEdge(1,2,3,1)
    graph6.addEdge(1,3,1,1)
    graph6.addEdge(1,4,7,1)
    graph6.addEdge(2,3,1,1)
    graph6.addEdge(2,5,2,1)
    graph6.addEdge(2,7,9,1)
    graph6.addEdge(3,4,1,1)
    graph6.addEdge(3,5,3,1)
    graph6.addEdge(3,6,5,1)
    graph6.addEdge(4,6,1,1)
    graph6.addEdge(5,6,1,1)
    graph6.addEdge(5,7,1,1)
    graph6.addEdge(6,7,10,1)

    path_computer = BestPath()
    best_paths = [[1,2,7],[1,3,5,7],[1,4,6,7]]
    paths = path_computer.n_paths(1,7,graph6,3)
    for path in paths:
        assert path in best_paths
