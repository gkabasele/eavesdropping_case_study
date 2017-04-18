# !/bin/python
from tabulate import tabulate
import networkx as nx
import pathFinder as pf

def packet_exposure(paths,G):
    edges = {}
    for edge in G.edges_iter():
        edges[edge] = 0
    for path in paths:
        for i in range(len(path)-1):
            if path[i] > path[i+1]:
                edges[(path[i+1],path[i])] +=1
            else:
                edges[(path[i],path[i+1])] +=1
    number_edge = len(G.edges())

    acc = 0
    for edge in edges:
        acc += (edges[edge] * (100/len(paths)))
    avg = float(acc)/number_edge
    upper = max(edges.values())
    lower = min(edges.values())
    print avg
    print "\n"


 


N = nx.Graph()

'''
N.add_nodes_from(range(1,24))
N.add_edges_from([(1,2),(1,3)],weight=1)
N.add_edges_from([(2,4),(2,5)],weight=1)
N.add_edges_from([(3,6)],weight=1)
N.add_edges_from([(4,7)],weight=1)
N.add_edges_from([(5,8),(5,9)],weight=1)
N.add_edges_from([(6,10)],weight=1)
N.add_edges_from([(7,11)],weight=1)
N.add_edges_from([(8,12),(8,13)],weight=1)
N.add_edges_from([(9,14)],weight=1)
N.add_edges_from([(10,14)],weight=1)
N.add_edges_from([(11,15)],weight=1)
N.add_edges_from([(12,16)],weight=1)
N.add_edges_from([(13,17)],weight=1)
N.add_edges_from([(14,17),(14,18)],weight=1)
N.add_edges_from([(15,19)],weight=1)
N.add_edges_from([(16,20),(16,17)],weight=1)
N.add_edges_from([(17,20)],weight=1)
N.add_edges_from([(18,21)],weight=1)
N.add_edges_from([(19,22)],weight=1)
N.add_edges_from([(20,23)],weight=1)
N.add_edges_from([(21,23)],weight=1)
N.add_edges_from([(22,24)],weight=1)
N.add_edges_from([(23,24)],weight=1)

src = 1
dst = 24
'''

N.add_nodes_from(range(1,30))
N.add_edges_from([(1,2),(1,4)],weight=1)
N.add_edges_from([(2,3),(2,5)],weight=1)
N.add_edges_from([(3,7)],weight=1)
N.add_edges_from([(4,6),(4,8)],weight=1)
N.add_edges_from([(5,10)],weight=1)
N.add_edges_from([(6,9),(6,11)],weight=1)
N.add_edges_from([(7,12)],weight=1)
N.add_edges_from([(8,13)],weight=1)
N.add_edges_from([(9,14)],weight=1)
N.add_edges_from([(10,12),(10,15)],weight=1)
N.add_edges_from([(11,14),(11,17)],weight=1)
N.add_edges_from([(12,15),(12,16)],weight=1)
N.add_edges_from([(13,17)],weight=1)
N.add_edges_from([(14,20)],weight=1)
N.add_edges_from([(15,19)],weight=1)
N.add_edges_from([(16,21)],weight=1)
N.add_edges_from([(17,19),(17,22)],weight=1)
N.add_edges_from([(18,22),(18,23)],weight=1)
N.add_edges_from([(19,21),(19,24)],weight=1)
N.add_edges_from([(20,25)],weight=1)
N.add_edges_from([(22,26)],weight=1)
N.add_edges_from([(23,27)],weight=1)
N.add_edges_from([(24,26)],weight=1)
N.add_edges_from([(25,27)],weight=1)
N.add_edges_from([(26,29)],weight=1)
N.add_edges_from([(27,28)],weight=1)
N.add_edges_from([(28,29)],weight=1)

src = 1
dst = 29



directed = N.to_directed() 


for i in range(1,6):
    d = i
    c = d
    w = pf.generate_cost(d)
    
    for edge in directed.edges():
        directed[edge[0]][edge[1]]['capacity']=c
        directed[edge[0]][edge[1]]['weight']=w

    directed.node[src]['demand'] = -d
    directed.node[dst]['demand'] = d


    NG = pf.graph_transformation(directed,c) 
    flows = pf.capacity_scaling(NG)
    f = pf.convert_flows(flows)
    cp = pf.get_paths(f,src,dst)
    sp = pf.shortest_path_disjoint(N,src,dst,i)


    print "%s\n"%(sorted(cp,key= lambda x: pf.cost_path(N,x)))
    print "%s\n"%(sorted(sp,key= lambda x: pf.cost_path(N,x)))
    cp_sum = sum(pf.cost_path(N,x) for x in cp)
    cp_avg = float(cp_sum)/d
    sp_sum = sum(pf.cost_path(N,x) for x in sp)
    sp_avg = float(sp_sum)/d
    table = [["Capacity Scaling",len(cp),pf.common_edge(N,cp),pf.edge_usage(N,cp,d),pf.longest_path_cost(N,cp),cp_sum,cp_avg],["Iterative Shortest Path",len(sp),pf.common_edge(N,sp),pf.edge_usage(N,sp,d),pf.longest_path_cost(N,sp),sp_sum,sp_avg]]
    heading = ["Algorithms","#Paths","#Common Edges","#Use Edge","Cost longest path","Sum All path cost","Average"]
    print tabulate(table,headers=heading)

    print "\n-----------------------------------------\n"

    packet_exposure(cp,N)
    packet_exposure(sp,N)
