# !/bin/python
import networkx as nx
import copy
import sys

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
            else:
                print "duplicate path"
            current = src
    return paths


''' From undirected graph to directed'''
def to_directed(G,src,dst,w,c):
    def _to_directed(G,dst,marked,cur,anc,DG,w,c):
        if cur == dst:
            DG.add_edge(anc,cur,weight=w,capacity=c)
        else:
             for n in G.neighbors(cur):
                if n not in marked:
                    DG.add_edge(cur,n,weight=w,capacity=c)
                    marked.add(n)
                    _to_directed(G,dst,marked,n,cur,DG,w,c)
                    marked.remove(n)
    marked = set([src])
    DG = nx.DiGraph()
    _to_directed(G,dst,marked,src,-1,DG,w,c)
    return DG

''' Find n maximally disjoint paths'''
def min_n_paths(G,src,dst,n):
    try:
        cost,result = nx.network_simplex(G)
        paths = get_paths(result,src,dst)
        return paths
    except nx.exception.NetworkXUnfeasible:
        result = nx.max_flow_min_cost(G,src,dst)
        flows = copy.deepcopy(result)
        paths = get_paths(result,src,dst)
        print paths
        l = len(paths)
        if l < n:
            min_cut = min_cut_edges(G,flows,src,dst)
            print min_cut
            increase_capacity(G,min_cut,n-l)
            #increase_cost(G,paths)
            try:
                cost,result = nx.network_simplex(G)
                paths = get_paths(result,src,dst)
                return paths
            except nx.exception.NetworkXUnfeasible:
                return paths
        return paths 


''' Naive approach to find maximally disjoint path'''
def shortest_path_disjoint(G,src,dst,n):
    paths = []
    CG = G.copy()
    for i in range(n):
        display_graph(CG)
        print "\n"
        path = nx.shortest_path(CG,source=src,target=dst)
        paths.append(path)
        increase_cost(CG,path)
    return paths

''' Display edges of the graph G'''
def display_graph(G):
    for edge in G.edges_iter(data=True):
        print edge

''' Increase cost of edge already used
def increase_cost(G,paths):
    for path in paths:
        for i in range(len(path)-1):
            G[path[i]][path[i+1]]['weight'] += 10
'''

def increase_cost(G,path):
    for i in range(len(path)-1):
        G[path[i]][path[i+1]]['weight'] +=10

''' Increase capacity on edge in minimum edge cut'''
def increase_capacity(G,min_cut,k):
    for edge in min_cut:
        if edge[1] in G[edge[0]]:
            G[edge[0]][edge[1]]['capacity'] += k 
        else:
            G[edge[1]][edge[0]]['capacity'] += k

''' Create a subgraph by removing node from nodes in G '''
def create_subgraph(G,nodes):
    new_graph = G.copy()
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

'''Set of all edges incident to a vertex in nodes but not in subgraph G'''
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

'''Compute cost of flow'''
def flow_cost(G,flows):
    cost = 0
    for head in flows:
        for tail in flows[head]:
            if flows[head][tail] >0:
                cost += flows[head][tail]*G[head][tail]['weight']
    return cost


'''Find edge belonging to a min s-t cut'''
def min_cut_edges(G,flows,s,t):
    cut_set = set()
    mincost =  flow_cost(G,flows)
    for head in flows:
        for tail in flows[head]:
            if flows[head][tail] > 0:
                new_graph = G.copy()
                new_graph.remove_edge(head,tail)
                new_flows = nx.max_flow_min_cost(new_graph,s,t)
                current_cost = flow_cost(G,new_flows)
                if current_cost < mincost:
                    cut_set.add((head,tail))
    return cut_set

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


'''convex cost function breakpoints [],slopes[]'''
def convex_flow_function(edge,breakpoints,slopes,flow):
    def segment_cost(edge,bp1,bp2,flow):
        if flow <= bp1:
            f = 0
        elif bp1 <= flow and flow <= bp2:
            f = flow - bp1
        elif flow >= bp2:
            f = bp2 - bp1
        return f
   
    flow_segment = []
    for i in range(len(breakpoints)-1):
        flow_segment.append(segment_cost(edge,breakpoints[i],breakpoints[i+1],flow))

    cost = sum([x*y for x,y in zip(flow_segment,slopes)])
    return cost
   
''' edge = {capacity:int, weight : (breakpoints,slopes)}'''
#cap is used to have diffent id when algo will reverse the edge
def graph_transformation(G,cap):
    NG = nx.MultiDiGraph()
    NG.add_nodes_from(G.nodes(data=True))
    for e in G.edges_iter(data='weight'):
        # e (node,node,(breakpoints,slopes))
        breakpoints,slopes= e[2]
        for i in range(len(breakpoints)-1):
            new_weight = slopes[i]      
            new_capacity = breakpoints[i+1]-breakpoints[i]
            if not NG.has_edge(e[1],e[0],key=i):
                NG.add_edge(e[0],e[1],weight=new_weight,capacity=new_capacity)
            else:
                NG.add_edge(e[0],e[1],key=cap+i,weight=new_weight,capacity=new_capacity)
    return NG

def build_residual_graph(G,flows=None):
    if flows is None:
        return G.copy()
    else:
        for u in flows:
            for v in flows[u]:
                for e in flows[u][v]:
                    f = flows[u][v][e]
                    # flow defined on original graph but G has edge that have been removed
                    if v in G[u] and e in G[u][v]:
                        G[u][v][e]['capacity']-=f
                        c,w = G[u][v][e].values()
                        if c <= 0:
                            G.remove_edge(u,v,key=e)
                        if not G.has_edge(v,u,key=e ):
                            G.add_edge(v,u,key=e,weight=-w,capacity=f)
                        else:
                            G[v][u][e]['capacity']+=f
                            
            
''' Find predecessors with a bfs '''
def exist_flow_path(G,s,t,pred):
    # BFS
    visited = {}
    for n in G.nodes_iter():
        visited[n] = (n == s)
    queue = [s]

    while queue:
        current = queue.pop(0)
        for n in G.neighbors(current):
            # Mulitgraph so several edge between two nodes
            for i in G[current][n]:
                c = G[current][n][i]['capacity']
                if not visited[n] and c > 0:
                    queue.append(n)
                    visited[n] = True
                    # Previous node and the edge to use
                    pred[n] = (current,i) 
    return visited[t]

def feasible_path(G,s,t,d):
    pred = {}
    path = []
    if exist_flow_path(G,s,t,pred): 
      path_capacity = d
      current = t
      path = [(current,0)]
      while current != s:
          #Find path bottleneck
          p,e = pred[current]
          c = G[p][current][e]['capacity']
          path_capacity = min(path_capacity,c)
          current = p
          path.insert(0,(current,e))
      return(path,path_capacity)
    else:
        pass

    

def feasible_flow(G,s,t,d):
    max_flow = d
    residual = build_residual_graph(G)
    flows = {}
    path = []
    path_capacity = d
    while True:
        if max_flow > 0:
            path,path_capacity = feasible_path(residual,s,t,max_flow)
            if path:
                for i in range(len(path)-1):
                    u,e = path[i]
                    v = path[i+1][0]
                    if path_capacity <= residual[u][v][e]['capacity']:
                            if u not in flows:
                                flows[u] = { v : {e : path_capacity}}
                            elif v not in flows[u]:
                                flows[u][v] = {e:path_capacity}
                            elif e not in flows[u][v]:
                                flows[u][v][e] = path_capacity
                            else:
                                flows[u][v][e] += path_capacity
                            build_residual_graph(residual,flows)
                max_flow -= path_capacity
            else:
                break
        else:
            break
    return flows

def build_convex_residual_graph(G,NG,flows):
    for u in flows:
        for v in flows[u]:
            for e in flows[u][v]:
                f = flows[u][v][e]
                c,w =  NG[u][v][e].values()
                if f >= c:
                    NG.remove_edge(u,v,key=e)
                    if not NG.has_edge(v,u,key=e):
                        NG.add_edge(v,u,key=e,weight= -w,capacity=c)
                    else:
                        NG[v][u][e]['weight']=-w

''' Detect if there is a negative edge cycle (Bellman Ford)'''
def negative_edge_cycle(G,s,distances,pred):
    for node in G.nodes_iter():
        if node == s:
            distances[node] = 0
        else:
            distances[node] = sys.maxint
    for i in range(len(G.nodes())-1):
        for u in G.nodes_iter():
            for v in G.neighbors(u):
                for e in G[u][v]:
                    tmp = distances[u] + G[u][v][e]['weight']
                    if tmp < distances[v]:
                        distances[v] = tmp
                        pred[v] = (u,e)

    #detecting negative cycle with last iteration
    for u in G.nodes_iter():
        for v in G.neighbors(u):
            for e in G[u][v]:
                if distances[v] > distances[u] + G[u][v][e]['weight']:
                    distances['start'] = v
                    return True
    return False

''' Check a node is already present in the cycle to make'''
def node_in_cycle(node,cycle):
    for i in range(len(cycle)):
        if cycle[i][0] == node[0]:
            cycle[i] = node
            del cycle[i+1:] 
            return True
    return False

''' Get negative cycle from predecessor graph'''
def get_cycle(G,pred,distances,s,t):
    #TODO check if s is connected to t
    current = distances['start']
    cycle = []
    while True:
        p = pred[current]
        if node_in_cycle(p,cycle):
            return cycle
        cycle.insert(0,p)
        #current_cost+= G[p[0]][current][p[1]]['weight']
        current = p[0]
    '''
    # Go from the ancestor for which the distance has changed 
    current = t
    cycle = []
    current_cost = 0
    while current != s:
        # p ( node, edgeid)
        p = pred[current]
        if node_in_cycle(p,cycle):
            return cycle
        cycle.insert(0,p)
        current_cost+= G[p[0]][current][p[1]]['weight']
        current = p[0]
    if current in pred and current_cost != distances[t]:
        while current_cost != distances[t]:
            p = pred[current]
            if node_in_cycle(p,cycle):
                return cycle
            cycle.insert(0,p)
            current_cost += G[p[0]][current][p[1]]['weight']
            current = p[0]
    '''
    return cycle 

def node_flow(G,n,flows,out=True):
    if not out:
        in_flow = 0 
        for u,v,e in G.in_edges(n):
            if u in flows and v in flows[u] and e in flows[u][v][e]:
                in_flow += flows[u][v][e]
                return in_flow
    else:
        out_flow = 0
        for u,v,e in G.out_edges(n):
            if u in flows and v in flows[u] and e in flows[u][v][e]:
                out_flow += flows[u][v][e]
        return out_flow 

''' Find the minimum capacity in a negative cycle'''
def get_cycle_capacity(G,cycle):
    cap = sys.maxint
    for i in range(len(cycle)-1):
       # (node,edgeid)
       u = cycle[i]
       v = cycle[i+1]
       cap = min(cap,G[u[0]][v[0]][u[1]]['capacity']) 
    u = cycle[-1]
    v = cycle[0]
    cap = min(cap,G[u[0]][v[0]][u[1]]['capacity']) 
    return cap

def update_flow(u,v,e,flows,amount):
    if u not in flows:
        flows[u]= {}
    if v not in flows[u]:
        flows[u][v] = {}
    if e not in flows[u][v]:
        flows[u][v][e] = amount
    else:
        flows[u][v][e] += amount

    if flows[u][v][e] <= 0:
        flows[u][v].pop(e,None)

def augment_flow_along_cycle(G,flows,cycle,cap):
    for i in range(len(cycle)-1):
        # (node,edgeid)
        u,e = cycle[i]
        v,d = cycle[i+1]
        # edge has been reversed so we decrease the flow on the edge
        if G[u][v][e]['weight'] < 0:
            update_flow(v,u,e,flows,-cap)
        else:
            update_flow(u,v,e,flows,cap)
    u,e = cycle[-1]
    v,d = cycle[0]
    if G[u][v][e]['weight'] < 0:
        update_flow(v,u,e,flows,-cap)
    else:
        update_flow(u,v,e,flows,cap)


''' G is the original graph, NG is the transformed graph'''
''' k is the number of demanded paths,k^2 is the maximum cost
    m is the number of edge
    n is the number of node
    The objective function is bounded by mk^3 . Any cycle cancelling decreases
    the objective function by a strictly positive amount. Since all data are integral
    the algorithm terminates within(mk^3) iterations. The Bellman Ford is (nm) to 
    identify negative cycle so complexity is O(nm^2k^3)
'''
def negative_cycle_cancelling(G,NG,s,t,d):
    flows = feasible_flow(NG,s,t,d)
    residual = NG.copy()  
    build_convex_residual_graph(G,residual,flows)
    distances = {}
    pred = {}
    while negative_edge_cycle(residual,s,distances,pred):
        cycle = get_cycle(residual,pred,distances,s,t)
        cap = get_cycle_capacity(residual,cycle)
        augment_flow_along_cycle(residual,flows,cycle,cap)
        #FIXME create new graph while changing edge instead of copying
        residual = NG.copy()
        build_convex_residual_graph(G,residual,flows)
        distances = {}
        pred = {}

    return flows

def capacity_scaling(NG):
    flowCost,flows = nx.capacity_scaling(NG)
    return flows

''' Convert flows for convex cost function graph to original graph'''
def convert_flows(flows):
    f = {}
    for u in flows:
        for v in flows[u]:
            if u not in f:
                f[u] = {v:0}
            else:
                f[u].update({v:0})
            for e in flows[u][v]:
                f[u][v] += flows[u][v][e]
    return f

def generate_cost(n):
    slopes = [x*x for x in range(1,n+1)]
    breakpoints = [x for x in range(n+1)]
    return (breakpoints,slopes) 
