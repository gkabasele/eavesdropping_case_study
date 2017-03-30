# !/bin/python
import matplotlib.pyplot as plt
import networkx as nx
import pathFinder as pf
import os
import sys


def parse_result(res,graphs):
    for line in res:
        if "[" in line or "Alg" in line or "Cap" in line or "Ite" in line:
            pass
        else:
            graphs.write(line)

def parse_graph(graphs,nbr):
    current = 1
    bar = 0
    with open('results/tmp.txt','w+') as f:
        for line in graphs:

            if "--" in line:
                bar +=1
                if current == nbr and bar == 2:
                    break
                if bar == 2:
                    current += 1
                    bar = 0
            else:
                if current == nbr:
                    print line
                    f.write(line)
    with open('results/tmp.txt','r') as f:
        G=nx.read_edgelist(f)
        nx.draw_networkx(G,with_labels=True)
        plt.show()
    os.remove('results/tmp.txt')

result = open('results/comparison.txt','r')
graphs = open('results/graphs.txt','r+')

try:
    nbr = int(sys.argv[1])
    parse_graph(graphs,nbr)
    result.close()
    graphs.close()
except ValueError:
    print "argument must be an integer"
