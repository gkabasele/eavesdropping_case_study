#! /bin/python

from bestPath import BestPath
from bhandari import Graph

if __name__=='__main__':

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
    
    path_computer.n_shortest_path(1,5,graph3,3)

    naive_path = path_computer.get_naive_solution()
    bhandari_path = path_computer.get_bhandari_solution()



    assert path_computer.objective_function(naive_path,graph3) == path_computer.objective_function(bhandari_path,graph3)
    
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

    path_computer.n_shortest_path(1,8,graph,2)

    naive_path = path_computer.get_naive_solution()
    bhandari_path = path_computer.get_bhandari_solution()

    assert path_computer.objective_function(naive_path,graph) < path_computer.objective_function(bhandari_path,graph) 
