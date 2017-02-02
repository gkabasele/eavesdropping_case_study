# !/bin/python
import networkx as nx

''' Build the paths from the flow network'''
def get_paths(previous,src,dst):
    current = src 
    finished = False
    paths = []
    while not finished:
        path = []
        while current != dst:
            path.append(current)
            try:
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
            except IndexError:
                print "Graph:%s,current:%s"%(previous,current)
                return
        path.append(current) 
        if not finished:
            if path not in paths:
                paths.append(path)
            current = src
    return paths

''' From undirected graph to undirected'''
def to_directed(G,src,dst,n):
    DG = nx.DiGraph()
    for node in G.nodes():
        if node == src:
            DG.add_node(node,demand=-n)
        elif node == dst:
            DG.add_node(node,demand=n)
        else:
            DG.add_node(node)
        for neighbor in G.neighbors(node):
            if type(neighbor) == int:
                c = G[node][neighbor]['capacity']
                w = G[node][neighbor]['weight']
                DG.add_edge(node,neighbor,capacity=c,weight=w)
    return DG

''' Find n maximally disjoint paths'''
def min_n_paths(G,src,dst,n):
    try:
        cost,result = nx.network_simplex(G)
        paths = get_paths(result,src,dst)
        return paths
    except nx.exception.NetworkXUnfeasible:
        result = nx.max_flow_min_cost(G,src,dst)
        paths = get_paths(result,src,dst)
        l = len(paths)
        if l < n:
            undirected = nx.Graph(G)
            min_cut = egcut(undirected,[src],[dst],list())
            increase_capacity(G,min_cut,n-l)
            increase_cost(G,paths)
            try:
                cost,result = nx.network_simplex(G)
                paths = get_paths(result,src,dst)
                return paths
            except nx.exception.NetworkXUnfeasible:
                return paths
        return paths 

''' Display edges of the graph G'''
def display_graph(G):
    #for edge in G.edges():
    #    print "%s w:%s c:%s" % (edge,G[edge[0]][edge[1]]['weight'],G[edge[0]][edge[1]]['capacity'])
    for edge in G.edges():
        print edge

''' Increase cost of edge already used'''
def increase_cost(G,paths):
    for path in paths:
        for i in range(len(path)-1):
            G[path[i]][path[i+1]]['weight'] += 1
        
''' Increase capacity on edge in minimum edge cut'''
def increase_capacity(G,min_cut,k):
    hist = []
    for cut in min_cut:
        for edge in cut:
            if edge not in hist:
                if edge[1] in G[edge[0]]:
                    G[edge[0]][edge[1]]['capacity'] += k 
                else:
                    G[edge[1]][edge[0]]['capacity'] += k
                hist.append(edge)

''' Create a subgraph by removing node in nodes '''
def create_subgraph(G,nodes):
    new_graph = nx.Graph(G)
    new_graph.remove_nodes_from(nodes)
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
    #Step 1 set of all vertices, adjacent to a vertex in s but not in s
    vx = set_vertices(G,s)

    #Step 2 Subgraph = G/s
    subgraph = create_subgraph(G,s)
    #Step 3 
    cc = connected_component(subgraph,t[0]) 
    nodes = set(G.nodes())
    z = (nodes - set(s) - cc)
    #Step 4
    if len((z & set(t)))!= 0 :
        return
    else:
        #Step 5
        s = list((set(s) | z))
        #Step 6
        vx = vx - z
        #Step 7-8
        cutset = minimal_cutset(G,s)
        if len(res) == 0:
            res.append(cutset)
        elif len(res[0]) > len(cutset):
            del res[:]
            res.append(cutset)
        elif len(res[0]) == len(cutset):
            res.append(cutset)

    #Step 9
    n_vt = list()
    #Step 10-11
    for v in (vx-set(t)):
        vx.remove(v)
        n_vs = list(s)
        n_t = list(t)
        n_vs.append(v)
        n_t.append(n_vt)
        #Step 12
        egcut(G,n_vs,n_t,res)
        #Step 13
        n_vt.append(v)
    return res


