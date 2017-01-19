# !/bin/python
from bhandari import Graph,DisjointPath

if __name__ =='__main__':
    
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

    disjoint = DisjointPath()

    paths = [[1,5,6,7,8],[1,2,3,4,8]]

    (res,shortest_path) = disjoint.disjoint_path_bhandari(1,8,graph,2)
    for path in paths:
        assert path in res
    
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

    paths = [[1,2,6,4],[1,5,3,4]]

    (res,shortest_path) = disjoint.disjoint_path_bhandari(1,4,graph2,2)
    for path in paths: 
        assert path in res

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
    
    paths = [[1,2,5],[1,3,5],[1,4,5]]
    
    (res,shortest_path) = disjoint.disjoint_path_bhandari(1,5,graph3,3)
    for path in paths:
        assert path in res


    graph4 = Graph()
    graph4.addNode(1)
    graph4.addNode(2)
    graph4.addNode(3)
    graph4.addNode(4)
    graph4.addNode(5)

    graph4.addEdge(1,2,1,1)
    graph4.addEdge(2,3,1,1)
    graph4.addEdge(2,4,1,1)
    graph4.addEdge(3,5,1,1)
    graph4.addEdge(4,5,1,1)

    (res,shortest_path) = disjoint.disjoint_path_bhandari(1,5,graph4,2)
    assert res == []

