# !/bin/python
import matplotlib.pyplot as plt
import networkx as nx
import pathFinder as pf
import cProfile
from tabulate import tabulate

'''{
Test on different graph  to compute several paths  

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

print pf.min_n_paths(N,1,9,3)
}'''


d = 4
c = d
w = pf.generate_cost(d)


s = 60
t = 61
def generate_random_graph(src,dst):
    random = nx.random_geometric_graph(s,0.14)
    for edge in random.edges():
        random.add_edge(edge[0],edge[1],weight = 1)

    random_graph = random.to_directed()
    for edge in random_graph.edges():
        random_graph[edge[0]][edge[1]]['capacity']=c
        random_graph[edge[0]][edge[1]]['weight']=w
    random_graph.add_node(s,demand=-d)
    random_graph.add_node(t,demand=d)
    for i in range(2):
        random_graph.add_edge(s,i,weight=w,capacity=c)
        random_graph.add_edge(i,s,weight=w,capacity=c)
        random_graph.add_edge(t,(s-1)-i,weight=w,capacity=c)
        random_graph.add_edge((s-1)-i,t,weight=w,capacity=c)
        random.add_edge(s,i,weight=1)
        random.add_edge(t,(s-1)-i,weight=1)
    return random_graph,random



fn = open('results/table2.txt','a+')
for i in range(50):
    try:
        random_graph,random = generate_random_graph(s,t)
        print "Number edges:%s"%len(random.edges())
        NG = pf.graph_transformation(random_graph,c)
        #nx.draw_networkx(NG,with_labels=True)
        flows = pf.capacity_scaling(NG)
        flows_ng = pf.negative_cycle_cancelling(random_graph,NG,s,t,d)
        f = pf.convert_flows(flows)
        f_ng = pf.convert_flows(flows)
        cp = pf.get_paths(f,s,t)
        ncp = pf.get_paths(f_ng,s,t)
        sp =  pf.shortest_path_disjoint(random,s,t,d)
        fn.write("\n-----------------------------------------\n")
        nx.write_edgelist(random,fn,data=True)
        fn.write("%s\n"%(sorted(cp,key= lambda x: pf.cost_path(random,x))))
        fn.write("%s\n"%(sorted(sp,key= lambda x: pf.cost_path(random,x))))
        fn.write("%s\n"%(sorted(ncp,key= lambda x: pf.cost_path(random,x))))
        cp_sum = sum(pf.cost_path(random,x) for x in cp)
        sp_sum = sum(pf.cost_path(random,x) for x in sp)
        ncp_sum = sum(pf.cost_path(random,x) for x in ncp)
        table = [["Capacity Scaling",len(cp),pf.common_edge(random,cp),pf.edge_usage(random,cp,d),pf.longest_path_cost(random,cp),cp_sum],["Iterative Shortest Path",len(sp),pf.common_edge(random,sp),pf.edge_usage(random,cp,d),pf.longest_path_cost(random,sp),sp_sum],["Negative CC",len(ncp),pf.common_edge(random,ncp),pf.edge_usage(random,ncp,d),pf.longest_path_cost(random,ncp),ncp_sum]]
        heading = ["Algorithms","#Paths","#Common Edges","#Use Edge","Cost longest path","Sum All path cost"]
        fn.write(tabulate(table,headers=heading))
        #plt.show()
    except nx.exception.NetworkXUnfeasible:
        print "No feasible solution"
fn.close



'''{
# Negative Cycle Detection
G = nx.MultiDiGraph()
G.add_nodes_from([0,1,2,3,4,5])
G.add_edge(0,1,weight=1)
G.add_edge(1,0,weight=1)
G.add_edge(1,2,weight=2)
G.add_edge(2,1,weight=-2)
G.add_edge(1,3,weight=2)
G.add_edge(3,1,weight=-2)
G.add_edge(2,3,weight=1)
G.add_edge(4,2,weight=-3)
G.add_edge(3,4,weight=1)
G.add_edge(4,3,weight=-1)
G.add_edge(4,5,weight=1)
distances = {}
pred = {}
pf.negative_edge_cycle(G,0,distances,pred)
print pred
print pf.get_cycle(G,pred,distances,0,5)
}'''

'''{
#Convex cost function problem
slopes_cheap = [1,2]
slopes_exp = [2,3]
breakpoints = [0,2,4]

G = nx.DiGraph()
G.add_node(1,demand=-4)
G.add_node(2)
G.add_node(3)
G.add_node(4,demand=4)
G.add_edge(1,2,weight=(breakpoints,slopes_exp),capacity=4)
G.add_edge(1,3,weight=(breakpoints,slopes_cheap),capacity=4)
G.add_edge(2,4,weight=(breakpoints,slopes_exp),capacity=4)
G.add_edge(3,4,weight=(breakpoints,slopes_cheap),capacity=4)
NG = pf.graph_transformation(G)
flows = pf.negative_cycle_cancelling(G,NG,1,4,4)
print pf.convert_flows(flows)
}'''

'''{
d = 3
c = 3
w = pf.generate_cost(d)

G = nx.DiGraph()
G.add_node(1,demand=-d)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)
G.add_node(7)
G.add_node(8,demand=d)


G.add_edge(1,2,weight=w,capacity=c)
G.add_edge(2,1,weight=w,capacity=c)

G.add_edge(1,5,weight=w,capacity=c)
G.add_edge(5,1,weight=w,capacity=c)

G.add_edge(2,3,weight=w,capacity=c)
G.add_edge(3,2,weight=w,capacity=c)

G.add_edge(3,4,weight=w,capacity=c)
G.add_edge(4,3,weight=w,capacity=c)

G.add_edge(5,4,weight=w,capacity=c)
G.add_edge(4,5,weight=w,capacity=c)

G.add_edge(4,6,weight=w,capacity=c)
G.add_edge(6,4,weight=w,capacity=c)

G.add_edge(4,8,weight=w,capacity=c)
G.add_edge(8,4,weight=w,capacity=c)

G.add_edge(5,6,weight=w,capacity=c)
G.add_edge(6,5,weight=w,capacity=c)

G.add_edge(6,7,weight=w,capacity=c)
G.add_edge(7,6,weight=w,capacity=c)

G.add_edge(7,8,weight=w,capacity=c)
G.add_edge(8,7,weight=w,capacity=c)

NG = pf.graph_transformation(G,c)

#flows = pf.capacity_scaling(NG)
flows = pf.negative_cycle_cancelling(G,NG,1,8,d)
f = pf.convert_flows(flows)
print pf.get_paths(f,1,8)
}'''
