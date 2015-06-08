"""
Degree distribution for graphs
Project 1, Algorithmic Thinking (Part 1)
This is a simple set of methods to analyze
the degree distribution of directed graphs

Author: Weikang Sun
Date: 6/4/15

Codeskulptor source:
http://www.codeskulptor.org/#user40_jdtGmYLlQ1_4.py

"""

# project 1 example directed graphs
EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])}
EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]), 
             3: set([0]), 
             4: set([1]), 
             5: set([2]), 
             6: set([])}
EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([7]),
             4: set([1]),
             5: set([2]), 
             6: set([]), 
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    """
    Returns a complete graph given n num_nodes
    n*(n-1)/2 edges will be generated
    """
    
    _digraph = {}
    
    # creates a set with all nodes
    _full_set = set(range(num_nodes))
    
    # simply remove own node for each node set
    for node in range(num_nodes):
        _digraph[node] = _full_set.difference(set([node]))

    return _digraph

def compute_in_degrees(digraph):
    """
    Returns a dictionary of number of 
    in-degrees for all nodes in the graph
    """
    
    _node_indeg = {}
    
    # creates the init 0 indegree node dic
    for key in digraph.keys():
        _node_indeg[key] = 0
    
    # iterates over all set values in the dictionary
    for key in digraph.keys():
        for head in digraph[key]:
            _node_indeg[head] += 1
    
    return _node_indeg

def in_degree_distribution(digraph):
    """
    Returns an unnormalized distribution
    of the number of in-degrees in the graph
    """
    
    # calls compute_in_degrees(), get in-degree list
    _indeg_list = compute_in_degrees(digraph).values()
    
    _indeg_dist = {}
    
    for value in _indeg_list:
        # check existing key, increment if so
        if _indeg_dist.has_key(value):
            _indeg_dist[value] += 1
        # otherwise create new key:value pair
        else:
            _indeg_dist[value] = 1
        
    return _indeg_dist   
