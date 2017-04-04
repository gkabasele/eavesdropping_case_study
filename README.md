# Eavesdropping Case Study 
Multipath routing strategy using SDN in ICS network to mitigate eavesdropping. The strategy used OpenFlow and leverage hard timeout to alternate between several paths.
To ensure there is always a matching rule, the strategy uses OpenFlow priority rules. 

### Path Selections
To select alternative paths such that they are as disjoint as possible and the paths are not costly. To accomodate with this two constraints we used the Capacity 
Scaling algorithm on a Convex flow problem.

### Plot graphs
You will find the results in the directory of the same name.
	*comparison.txt contains several graphs and the results of the comparison between the Capacity Scaling algorithm and a Iterative Shortest Path algorithm
	*graphs.txt contains only the graphs. If you wish to plot one of them, you can use the readGraph python script:
	```shell
	python readGraph.py <nbr_graph>
	```
	Where <nbr_graph> is the number of the graph
