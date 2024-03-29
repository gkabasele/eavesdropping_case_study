# !/bin/python
from bhandari import Graph,DisjointPath
import copy
import heapq
import sys

# Tweaking coefficient according to traffic?
COST = 5            #10
COMMON_VERTEX = 7   # 3
MULTIPLIER = 100
NB_PATH = 6

class BestPath:
    def __init__(self):
        pass

    def remove_edge_along_path(self,path,graph):
        for i in range(0,len(path)-1):
            graph.remove_edge(path[i],path[i+1])
            graph.remove_edge(path[i+1],path[i])
            
    def increase_cost_along_path(self,path,graph):
        for i in range(0,len(path)-1):
            new_cost = MULTIPLIER*graph.cost_edge(path[i],path[i+1])            
            graph.increase_cost(path[i],path[i+1],new_cost)
            graph.increase_cost(path[i+1],path[i],new_cost)

    def no_existing_disjoint_path(self,disjoint,src,dst,graph,n):
        # Is it better to have n non disjoint path or n-1 disjoint path
        paths = []
        i = 1
        while len(paths) == 0 and i < n:
            (paths,shortest_path) = disjoint.disjoint_path_bhandari(src,dst,graph,n-i)
            i+=1

        bhandari_evaluation = self.objective_function(paths,graph)

        other_paths = [shortest_path]
        new_graph = copy.deepcopy(graph)
        self.increase_cost_along_path(shortest_path,new_graph)
        path = disjoint.get_path(src,dst,new_graph)
        other_paths.append(path)
        for i in range(n-2):
            new_graph = copy.deepcopy(new_graph)
            self.increase_cost_along_path(path,new_graph)
            path = disjoint.get_path(src,dst,new_graph)
            other_paths.append(path)

        naive_evaluation = self.objective_function(other_paths,graph)

        if naive_evaluation > bhandari_evaluation:
            return paths
        else:
            return other_paths

    def existing_disjoint_path(self,disjoint,graph,paths,shortest_path,n):
        bhandari_evaluation = self.objective_function(paths,graph)

        other_paths = [shortest_path]
        priority_path = self.common_edges_shortest_path(paths,shortest_path,graph)
        
        for i in range(n-1):
            # priority queue contains tuple (#common_link,cost,path)
            other_paths.append(heapq.heappop(priority_path)[2])

        naive_evaluation = self.objective_function(other_paths,graph)
        if naive_evaluation > bhandari_evaluation:
            return paths
        else:
            return other_paths


    def n_paths(self,src,dst,graph,n):
        disjoint = DisjointPath() 
        if len(graph.neighbor(src)) >= n and len(graph.neighbor(dst)) >=n:
            (paths,shortest_path) = disjoint.disjoint_path_bhandari(src,dst,graph,n)
            #Could not find n disjoint path
            if len(paths) == 0:
                return self.no_existing_disjoint_path(disjoint,src,dst,graph,n)
            else:
                return self.existing_disjoint_path(disjoint,graph,paths,shortest_path,n)
        else:
            return self.no_existing_disjoint_path(disjoint,src,dst,graph,n)
            
    def common_edges_shortest_path(self,paths,shortest_path,graph):
        edges = set()
        priority_path = []
        for i in range(len(shortest_path)-1):
            edges.add((shortest_path[i],shortest_path[i+1]))
            edges.add((shortest_path[i+1],shortest_path[i+1]))

        for path in paths:
            common_edges = 0
            path_cost = self.count_path_cost(path,graph)
            for i in range(len(path)-1):
                if (path[i],path[i+1]) in edges:
                    common_edges +=1
            heapq.heappush(priority_path,(common_edges,path_cost,path))

        return priority_path


    def count_common_edges(self,paths):
        edges = set()
        common_edges = 0
        for path in paths:
            for i in range(0,len(path)-1):
                if (path[i],path[i+1]) in edges:
                    common_edges +=1
                else:
                    edges.add((path[i],path[i+1]))
                    edges.add((path[i+1],path[i]))
        return common_edges

    def count_path_cost(self,path,graph):
        cost = 0
        if len(path) == 0:
            return sys.maxint
        for i in range(0,len(path)-1):
            cost+= graph.cost_edge(path[i],path[i+1])
        return cost

    def longest_path_cost(self,paths,graph):
        max_cost = 0
        for i in range(len(paths)):
            current_cost = self.count_path_cost(paths[i],graph)
            if current_cost > max_cost:
                max_cost = current_cost
        return max_cost


    def objective_function(self,paths,graph):
        common = COMMON_VERTEX * self.count_common_edges(paths)
        nb_path = NB_PATH * len(paths)
        cost = COST * self.longest_path_cost(paths,graph)
        return common + cost - nb_path


