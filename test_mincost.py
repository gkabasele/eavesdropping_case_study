# !/bin/python
import networkx as nx
from networkx.algorithms.connectivity import minimum_st_edge_cut
import matplotlib.pyplot as plt
import pathFinder as pf
import cProfile
'''
G = nx.DiGraph()
G.add_node(1,demand=-3)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)
G.add_node(7)
G.add_node(8,demand=3)

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

print pf.min_n_paths(G,1,8,3)


D = nx.DiGraph()
D.add_node(1,demand=-2)
D.add_node(2)
D.add_node(3)
D.add_node(4)
D.add_node(5)
D.add_node(6)
D.add_node(7)
D.add_node(8,demand=2)

D.add_edge(1,2,weight=1,capacity=1)
D.add_edge(1,3,weight=1,capacity=1)
D.add_edge(2,4,weight=1,capacity=1)
D.add_edge(3,4,weight=1,capacity=1)
D.add_edge(4,5,weight=1,capacity=1)
D.add_edge(5,6,weight=1,capacity=1)
D.add_edge(5,7,weight=1,capacity=1)
D.add_edge(6,8,weight=1,capacity=1)
D.add_edge(7,8,weight=1,capacity=1)

print pf.min_n_paths(D,1,8,2)
'''
N = nx.DiGraph()
N.add_node(1,demand=-3)
N.add_node(2)
N.add_node(3)
N.add_node(4)
N.add_node(5)
N.add_node(6)
N.add_node(7)
N.add_node(8)
N.add_node(9,demand=3)

N.add_edge(1,2,weight=1,capacity=1)

N.add_edge(1,3,weight=1,capacity=1)

N.add_edge(2,5,weight=1,capacity=1)

N.add_edge(3,4,weight=1,capacity=1)

N.add_edge(4,8,weight=1,capacity=1)

N.add_edge(5,6,weight=1,capacity=1)

N.add_edge(5,7,weight=1,capacity=1)

N.add_edge(6,7,weight=1,capacity=1)

N.add_edge(6,9,weight=1,capacity=1)

N.add_edge(7,9,weight=1,capacity=1)

N.add_edge(8,9,weight=1,capacity=1)



'''print pf.min_n_paths(N,1,9,3)
'''

s = 15
t = 16
random_graph = nx.random_geometric_graph(s,0.2)
for edge in random_graph.edges():
    random_graph[edge[0]][edge[1]]['capacity']=1
    random_graph[edge[0]][edge[1]]['weight']=1
random_graph.add_node(s,demand=-3)
random_graph.add_node(t,demand=3)
for i in range(2):
    random_graph.add_edge(s,i,weight=1,capacity=1)
    random_graph.add_edge(t,(s-1)-i,weight=1,capacity=1)
pf.display_graph(random_graph)
print "Number edges:%s"%len(random_graph.edges())
directed = pf.to_directed(random_graph,s,t,3)
#print  pf.min_n_paths(directed,s,t,3)
cProfile.run('print pf.min_n_paths(directed,s,t,3)')
