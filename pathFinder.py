# !/bin/python
import networkx as nx
from networkx.algorithms.connectivity import minimum_st_edge_cut

''' Build the paths from the flow network'''
def get_paths(previous,src,dst):
    current = src 
    finished = False
    paths = []
    while not finished:
        path = []
        while current != dst:
            path.append(current)
            succ = previous[current]
            if len(succ.keys()) == 0:
                finished = True
                break
            for n in succ.keys():
                if succ[n] > 0:
                    current = n
                    succ[n] -= 1
                    if succ[n] == 0:
                        del succ[n]
                        break
                else:
                    del succ[n]
        path.append(current) 
        if not finished:
            paths.append(path)
            current = src
    return paths

def n_paths(G,src,dst,n):
    result = nx.max_flow_min_cost(G,src,dst)
    paths = get_paths(result,src,dst)
    l = len(paths)
    if l < n:
        min_cut = egcut(nx.Graph(G),[1],[8],list())
        increment_capacity(G,min_cut,n-l)
        result = nx.max_flow_min_cost(G,src,dst)
        paths = get_paths(result,src,dst)
    return paths

        
''' Increment capacity on edge in minimum edge cut'''
def increment_capacity(G,min_cut,k):
    for cut in min_cut:
        for edge in cut:
            G[edge[0]][edge[1]]['capacity'] += k 

''' Create a subgraph by removing node in nodes '''
def create_subgraph(G,nodes):
    new_graph = nx.Graph()
    for node in G.nodes():
        if node not in nodes:
            new_graph.add_node(node)
            for neighbor in G.neighbors(node):
                if neighbor not in nodes:
                    new_graph.add_edge(node,neighbor)
    return new_graph

'''Set of all vertices adjacent to a vertex in nodes but not in nodes'''
def set_vertices(G,nodes):
    vx = set()
    for node in nodes:
        for neighbor in G.neighbors(node):
            if neighbor not in nodes:
                vx.add(neighbor)
    return vx

'''Set of all edges incident to a vertex in nodes but not in subgraph'''
def minimal_cutset(G,nodes):
    cutset = set()
    for node in nodes:
        for neighbor in G.neighbors(node):
            if neighbor not in nodes:
                cutset.add((node,neighbor))
    return cutset


''' Find reachable nodes from the source'''
def connected_component(G,src):
    cc = nx.bfs_predecessors(G,src).keys()
    cc.append(src)
    return set(cc)

''' [8,[]] => [] '''
def flat_list(l):
    nl = list()
    for item in l:
        if type(item) == list and len(item)!=0:
            nl.append(item[0])
        elif type(item) !=list:
            nl.append(item)
    return nl

''' s,t are a list'''
def egcut(G,s,t,res):
    if len(t) >= 2:
        t = flat_list(t)
    vx = set_vertices(G,s)
    subgraph = create_subgraph(G,s)
    cc = connected_component(subgraph,t[0]) 
    nodes = set(G.nodes())
    z = (nodes - set(s) - cc)

    if len((z & set(t)))!= 0 :
        return
    else:
        s = list((set(s) | z))
        vx = vx - z
        cutset = minimal_cutset(G,s)
        if len(res) == 0:
            res.append(cutset)
        elif len(res[0]) > len(cutset):
            del res[:]
            res.append(cutset)
        elif len(res[0]) == len(cutset):
            f = True
            for edge in cutset:
                if edge[0] != s[0] and edge[1] != t[0]:
                    f = False
            if f:
                res.append(cutset)

    n_vt = list()
    for v in (vx-set(t)):
        vx.remove(v)
        n_vs = list(s)
        n_t = list(t)
        n_vs.append(v)
        n_t.append(n_vt)
        egcut(G,n_vs,n_t,res)
        n_vt.append(v)
    return res

G = nx.DiGraph()
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)
G.add_node(7)
G.add_node(8)

G.add_edge(1,2,weight=1,capacity=1)
G.add_edge(2,1,weight=1,capacity=1)

G.add_edge(1,5,weight=1,capacity=1)
G.add_edge(5,1,weight=1,capacity=1)

G.add_edge(2,3,weight=1,capacity=1)
G.add_edge(3,2,weight=1,capacity=1)

G.add_edge(3,4,weight=1,capacity=1)
G.add_edge(4,3,weight=1,capacity=1)

G.add_edge(5,4,weight=1,capacity=1)
G.add_edge(4,5,weight=1,capacity=1)

G.add_edge(4,6,weight=1,capacity=1)
G.add_edge(6,4,weight=1,capacity=1)

G.add_edge(4,8,weight=1,capacity=1)
G.add_edge(8,4,weight=1,capacity=1)


G.add_edge(5,6,weight=1,capacity=1)
G.add_edge(6,5,weight=1,capacity=1)

G.add_edge(6,7,weight=1,capacity=1)
G.add_edge(7,6,weight=1,capacity=1)

G.add_edge(7,8,weight=1,capacity=1)
G.add_edge(8,7,weight=1,capacity=1)

print n_paths(G,1,8,3)


D = nx.DiGraph()
D.add_node(1)
D.add_node(2)
D.add_node(3)
D.add_node(4)
D.add_node(5)
D.add_node(6)
D.add_node(7)
D.add_node(8)

D.add_edge(1,2,weight=1,capacity=1)
D.add_edge(1,3,weight=1,capacity=1)
D.add_edge(2,4,weight=1,capacity=1)
D.add_edge(3,4,weight=1,capacity=1)
D.add_edge(4,5,weight=1,capacity=1)
D.add_edge(5,6,weight=1,capacity=1)
D.add_edge(5,7,weight=1,capacity=1)
D.add_edge(6,8,weight=1,capacity=1)
D.add_edge(7,8,weight=1,capacity=1)

print n_paths(D,1,8,2)
