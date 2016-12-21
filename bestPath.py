# !/bin/python
from bhandari import Graph,DisjointPath
import copy

BHAN = "bhandari"
NA = "naive"

# Tweaking coefficient according to traffic?
NB_PATH = 5
COST = 10
COMMON_VERTEX = 3

class BestPath:
    def __init__(self):
        self.solutions = {}

    def get_naive_solution(self):
        if NA in self.solutions:
            return self.solutions[NA]

    def get_bhandari_solution(self):
        if BHAN in self.solutions:
            return self.solutions[BHAN]


    def remove_edge_along_path(self,path,graph):
        for i in range(0,len(path)-1):
            graph.remove_edge(path[i],path[i+1])
            graph.remove_edge(path[i+1],path[i])

    def n_shortest_path(self,src,dst,graph,n):
        disjoint = DisjointPath() 
        (paths,shortest_path) = disjoint.disjoint_path_bhandari(src,dst,graph,n)
        self.solutions[BHAN] = paths

        other_paths = [shortest_path]
        new_graph = copy.deepcopy(graph)
        self.remove_edge_along_path(shortest_path,new_graph)
        #TODO what happens when no disjoint path possible
        for i in range(n-1):
            path = disjoint.get_path(src,dst,new_graph)

            if len(path) == 0:
                #if no path found we add a vertex
                i = len(path) - 1
                while len(path) == 0 and i > 0:
                    n = shortest_path(i)
                    prev = shortest_path(i-1)
                    previous_cost = graph.cost_edge(n,prev)
                    new_graph.addVertex(n,prev)
                    path = disjoint.get_path(src,dst,new_graph)
                    
            other_paths.append(path)
            new_graph = copy.deepcopy(new_graph)
            self.remove_edge_along_path(path,new_graph)
                        
        self.solutions[NA] = other_paths
        
    def count_common_vertex(self,paths):
        vertices = set()
        common_vertex = 0
        for path in paths:
            for i in range(0,len(path)-1):
                if (path[i],path[i+1]) in vertices:
                    common_vertex +=1
                else:
                    vertices.add((path[i],path[i+1]))
                    vertices.add((path[i+1],path[i]))
        return common_vertex

    def count_path_cost(self,path,graph):
        cost = 0
        for i in range(0,len(path)-1):
            cost+= graph.cost_edge(path[i],path[i+1])
        return cost

    def objective_function(self,paths,graph):
        common = COMMON_VERTEX * self.count_common_vertex(paths)
        nb_path = NB_PATH * len(paths)
        cost = COST * self.count_path_cost(paths[0],graph)
        return common + cost - nb_path


