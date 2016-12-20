# !/bin/python
import sys
import copy

# Graph composition
class Graph:

    def __init__(self, graph=None):
        if graph:
            self.graph = graph
        else:
            self.graph = {}

    def addNode(self, node):
        if node not in self.graph:
            self.graph[node] = {}

    def addVertex(self, node1, node2, cost):
        if node1 in self.graph and node2 in self.graph:
            self.graph[node1][node2] = cost 
            self.graph[node2][node1] = cost

    def vertices(self):
        return self.graph.keys()

    def cost_edge(self,node1,node2):
        return self.graph[node1][node2]

    def update_cost(self,node1,node2):
        cost = self.graph[node1][node2]
        self.graph[node1][node2] = -cost
    
    def remove_edge(self,node1,node2):
        del self.graph[node1][node2]

    def neighbor(self,node):
        return self.graph[node].keys()


class DisjointPath:
    
    def __init__(self, graph,k):
        self.graph = graph
        self.k = k


    def distances_init(self, nodes,src):
        distances = {}
        for node in nodes:
            if node == src:
                distances[src] = 0
            else:
                distances[node] = sys.maxint
        return distances
    
    def shortest_path_dijkstra(self,src,graph):
        path = {}
        nodes = set(graph.vertices())
        distances = self.distances_init(nodes,src)
        visited = distances.copy()

        while nodes:
            #find node with minimun distance
            closest = min(visited,key=visited.get)
            del visited[closest]
            nodes.remove(closest)
            for n in graph.neighbor(closest):
                tmp = distances[closest] + graph.cost_edge(closest,n)
                if tmp < distances[n]:
                    distances[n] = tmp
                    path[n] = closest 

        return (path,distances)

            

    def shortest_path_bellman_ford(self,src,graph):
        path = {}
        nodes = set(graph.vertices())
        distances = self.distances_init(nodes,src)
        for i in range(len(nodes)-1):
            for node in graph.vertices():
                for n in graph.neighbor(node):
                    tmp = distances[node] + graph.cost_edge(node,n)
                    if tmp < distances[n]:
                        distances[n] = tmp
                        path[n] = node
        
        for node in graph.vertices():
            for n in graph.neighbor(node):
                assert distances[n] <= distances[node] + graph.cost_edge(node,n)

        return (path,distances)

    def get_path(self, src, dst,graph,negative=False):
        if negative:
            (previous,distances) = self.shortest_path_bellman_ford(src,graph)
        else:
            (previous,distances) = self.shortest_path_dijkstra(src,graph)

        path = []
        path.insert(0,dst)
        current = dst
        traveled = 0
        while traveled <= distances[dst]:
            p = previous[current]
            if p == src:
                path.insert(0,p)
                return path
            else:
                path.insert(0,p)
                traveled += graph.cost_edge(p,current)
                current = p
        return


    def change_edge(self,path,new_graph):
        for i in range(0,len(path)-1):
            new_graph.remove_edge(path[i],path[i+1])
            new_graph.update_cost(path[i+1],path[i])


    def disjoint_path_bhandari(self,src,dst,graph):
        path = self.get_path(src,dst,graph)

        # Repeat k times

        new_graph = copy.deepcopy(self.graph)
        
        self.change_edge(path,new_graph)

        path2 = self.get_path(src,dst,new_graph,True)

        return (path,path2)



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
    
    '''
        2 ----------- 3
      /                 \
     /                   \
    1 ------- 5 --------- 4 -------8
              |          /         |
              |         /          |
              +------- 6 ----------7
    '''

    disjoint = DisjointPath(graph,2)
    (path,path2) = disjoint.disjoint_path_bhandari(1,8,graph)
    print path
    print path2
