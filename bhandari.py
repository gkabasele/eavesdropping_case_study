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
    
    def __init__(self):
        pass 

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

    def add_edge_to_set(self,path,links):
        edges = links
        for i in range(0,len(path)-1):
            if path[i] not in edges:
                edges[path[i]] = {}
            if path[i+1] not in edges:
                edges[path[i+1]] = {}

            if path[i+1] in edges[path[i]]:
                edges[path[i]][path[i+1]] = False
            elif path[i] in edges[path[i+1]]:
                edges[path[i+1]][path[i]] = False
            else:
                edges[path[i]][path[i+1]] = True
        return edges

    def get_disjoint_path(self,src,dst,links,k):
        disjoint_paths = []
        for i in range(k):
            path = []
            current = src
            while current != dst:
                path.append(current)
                find_succ = False
                i = 0
                while not find_succ:
                    succ = links[current].keys()[i]
                    if links[current][succ]:
                        links[current][succ] = False
                        find_succ = True
                        current = succ
                    else:
                        i+=1
            path.append(current)
            disjoint_paths.append(path)
        return disjoint_paths


    def disjoint_path_bhandari(self,src,dst,graph,k):
        links = {}
        path = self.get_path(src,dst,graph)

        self.add_edge_to_set(path,links)

        # Repeat k-1 times
        for i in range(k-1):
            new_graph = copy.deepcopy(graph)
            self.change_edge(path,new_graph)
            path2 = self.get_path(src,dst,new_graph,True)
            self.add_edge_to_set(path2,links)

        disjoint_path = self.get_disjoint_path(src,dst,links,k)

        return disjoint_path



if __name__ =='__main__':
    '''
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



    disjoint = DisjointPath()
    #disjoint_path = disjoint.disjoint_path_bhandari(1,8,graph,2)
    #print disjoint_path
    disjoint_path = disjoint.disjoint_path_bhandari(1,4,graph2,2)
    print disjoint_path
