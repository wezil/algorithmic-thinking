"""
Algorithmic Thinking: Project 2
Connected Components and Graph Resilience

This code implements an efficient breadth-
first search algorithm for determining
connected components in a graph as well
as the graph's resilience to removing nodes.

Author: Weikang Sun
Date: 6/23/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_7TXMr52VHl_3.py
"""

# sample graphs for module 2
import alg_module2_graphs as alg_graphs
# Queue class from PoC
import poc_queue


def bfs_visited(ugraph, start_node):
    """
    Input: undirected graph dictionary and 
    source node start_node
    
    Output: Set of all nodes visited by algorithm
    """
    
    # error check for start_node in ugraph
    if not ugraph.has_key(start_node):
        return set([])
    
    node_queue = poc_queue.Queue()
    visited = set([start_node])
    
    node_queue.enqueue(start_node)
    
    while len(node_queue) > 0:
        active_node = node_queue.dequeue()
        
        if ugraph.has_key(active_node):        
            for neighbor in ugraph[active_node]:
                if neighbor not in visited and ugraph.has_key(neighbor):
                    visited.add(neighbor)
                    node_queue.enqueue(neighbor)
    
    return visited


def cc_visited(ugraph):
    """
    Input: undirected graph dictionary
    
    Output: list of sets of connected components
    """
    
    remaining_nodes = ugraph.keys()
    connected_comp = []
    
    while remaining_nodes != []:
        active_node = remaining_nodes.pop()
        set_visited = bfs_visited(ugraph, active_node)
        connected_comp.append(set_visited)
        
        for node in set_visited:
            if node in remaining_nodes:
                remaining_nodes.remove(node)
    
    return connected_comp
    

def largest_cc_size(ugraph):
    """
    Input: undirected graph dictionary
    
    Output: integer value of the largest
    connected component in this graph
    """
    
    connected_comp = cc_visited(ugraph)
    max_length = 0
    
    # debug purposes
    # print connected_comp
    
    for set_cc in connected_comp:
        max_length = max(max_length, len(set_cc))
    
    return max_length


def compute_resilience(ugraph, attack_order):
    """
    Input: undirected graph dictionary and
    list of order of nodes to be removed
    
    Output: list of the largest connected
    component in graph after removing k'th
    node given in attack_order
    """
    
    resilience = [largest_cc_size(ugraph)]
    
    for attack_node in attack_order:
        if ugraph.has_key(attack_node):
            ugraph.pop(attack_node)
        
        resilience.append(largest_cc_size(ugraph))
    
    return resilience

    
    
# debug tests    
#ugraph = alg_graphs.GRAPH9
#print compute_resilience(ugraph, ugraph.keys())
