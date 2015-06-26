"""
Algorthmic Thinking: Application 2
This application will simulate an attack
on a network represented by an undirected
graph, by measuring the resilience of 
connected components as nodes are removed.

Auhor: Weikang Sun
Date: 6/23/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_WPPkwjgANP_39.py
"""

# general imports
import urllib2
import random
import time
import math

# CodeSkulptor import
import simpleplot
import codeskulptor
codeskulptor.set_timeout(1000)

# import fast UPA algorithm
import alg_upa_trial

# importing my own graph visualizer
import user40_HQvawPHV6L_4 as graph_view

# import precomputed values for network
import user40_wIliXlp4lC_7 as precomputed



############################################
# Provided code from App 2

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


###########
# New Code

def print_graph(ugraph):
    """
    debug code to print an undirected graph dictionary
    """
    
    for key in ugraph.keys():
        print str(key)+":", ugraph[key]
        

def make_complete_graph(num_nodes):
    """
    generates a complete undirected graph
    as a dictionary
    """
    
    ugraph = {}
    
    full_set = set(range(num_nodes))
    
    for node in full_set:
        ugraph[node] = full_set.difference(set([node]))
        
    return ugraph


def ER_undirected_generator(nodes, edge_prob):
    """
    generates a random undirected graph with
    given nodes and edge creation probability
    """
     
    # start with a full graph
    generated_graph = make_complete_graph(nodes)
    
    # iterate over every edge removing them with
    # probability 1 - edge_prob
    for tail in generated_graph.keys():
        for head in generated_graph[tail]:
            # head > tail  ensures same edge not checked twice
            # random.random()  checks removal probability
            if head > tail and random.random() > edge_prob:
                # must remove edge coorespondance in both nodes
                generated_graph[tail].remove(head)
                generated_graph[head].remove(tail)
    
    return generated_graph


def ER_undirected_generator2(nodes, edge_prob):
    """
    generates a random undirected graph with
    given nodes and edge creation probability
    
    Slightly modified from above algorithm where
    a complete graph generation is not necessary.
    This results in a faster generation of graph.
    """
    
    generated_graph = {}
    
    # fill in each node with blank first
    for node in range(nodes):
        generated_graph[node] = set([])
        
    for tail in range(nodes):
        # iterate over all "head" nodes larger than "tail"
        # each edge possibility is considered only once
        for head in range(tail + 1, nodes):
            if random.random() < edge_prob:
                # make sure to add edge to both nodes
                generated_graph[tail].add(head)
                generated_graph[head].add(tail)

    return generated_graph


def UPA_algorithm(complete_nodes, additional_nodes):
    """
    Implementation of the UPA algorithm which generates
    a complete graph with complete_nodes and appends
    additional_nodes with edge probability proportional
    to the existing edge count per node.
    
    Basically generates few "super nodes" with many edges
    """
    
    # generates the complete graph m nodes 
    complete_graph = make_complete_graph(complete_nodes)
    
    # creates the new UPA trial algorithm object
    upa_object = alg_upa_trial.UPATrial(complete_nodes)
    
    # iterate over n new nodes and connect them to existing graph
    for new_node in range(complete_nodes, complete_nodes + additional_nodes):
        # the set of all nodes this new_node will connect to
        complete_graph[new_node] = upa_object.run_trial(complete_nodes)
        
        # make sure both nodes in edge are updated
        for node in complete_graph[new_node]:
            complete_graph[node].add(new_node)

    return complete_graph


def compute_node_degrees(ugraph):
    """
    Returns a dictionary of degree number for 
    all nodes in the undirected graph
    """
    
    node_deg = {}
    
    # iterate over all dictionary keys to find size of 
    # adjacency list for each node
    for node in ugraph:
        node_deg[node] = len(ugraph[node])
        
    return node_deg


def degree_distribution(ugraph):
    """
    Returns an unnormalized distribution of
    the number of degrees in the undir graph
    """
    
    # get a list of all degree values for each node
    deg_list = compute_node_degrees(ugraph).values()
    
    deg_dist = {}
    
    for value in deg_list:
        # check existing key, increment if so
        if deg_dist.has_key(value):
            deg_dist[value] += 1
        # otherwise create new key:value pair
        else:
            deg_dist[value] = 1
    
    return deg_dist


def count_edges(ugraph):
    """
    Returns the number of edges in the undir graph
    """
    # get a list of all degree values for each node
    deg_list = compute_node_degrees(ugraph).values()
    
    # simply sum the number of degrees then divide by
    # 2 for double counting the edges
    return sum(deg_list) / 2


def average_degree(ugraph):
    """
    Returns the average degree from the undirected
    graph distribution
    """
    
    # get list of degree values for each node 
    deg_list = compute_node_degrees(ugraph).values()
    
    # simply return the average of the list values
    return sum(deg_list) / float(len(deg_list))
    
    
def calculate_ER_probability(ugraph):
    """
    Returns the appropriate probability p for an
    arbitrary undirected graph such that a 
    generated ER graph with this p will yield
    approximately the same number of edges
    """
    
    num_edges = count_edges(ugraph)
    num_nodes = len(ugraph.keys())
    # definition of a complete graph
    max_edges = num_nodes * (num_nodes - 1) / 2
    
    return num_edges / float(max_edges)


def random_order(ugraph):
    """
    returns a list of random node order
    """
    
    nodes = ugraph.keys()
    random.shuffle(nodes)
    
    return nodes


def bfs_visited2(ugraph, start_node):
    """
    Input: undirected graph dictionary and 
    source node start_node
    
    Output: Set of all nodes visited by algorithm
    
    This is slightly modified from project 2
    to not include external Queue class references
    (a small computational improvement)
    """
    
    node_queue = []
    visited = set([start_node])
    
    node_queue.append(start_node)
    
    while len(node_queue) > 0:
        active_node = node_queue.pop(0)
        
        if ugraph.has_key(active_node):        
            for neighbor in ugraph[active_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    node_queue.append(neighbor)
    
    return visited


def cc_visited2(ugraph):
    """
    Input: undirected graph dictionary
    
    Output: list of sets of connected components
    
    This is slightly modified to not include a pop()
    statement as was in Project 2 (a small 
    computational improvement)
    """
    
    remaining_nodes = ugraph.keys()
    connected_comp = []
    
    while remaining_nodes != []:
        active_node = remaining_nodes[0]
        set_visited = bfs_visited2(ugraph, active_node)
        connected_comp.append(set_visited)
        
        for node in set_visited:
            remaining_nodes.remove(node)
    
    return connected_comp
    

def largest_cc_size(ugraph):
    """
    Input: undirected graph dictionary
    
    Output: integer value of the largest
    connected component in this graph
    """
    
    connected_comp = cc_visited2(ugraph)
    max_length = 0
    
    # debug purposes
    # print connected_comp
    
    for set_cc in connected_comp:
        max_length = max(max_length, len(set_cc))
    
    return max_length


def compute_resilience2(ugraph, attack_order):
    """
    input: undirected graph dictionary and
    list of order of nodes to be removed
    
    return: list of the largest connected
    component in graph after removing k'th
    node given in attack_order
    
    hopefully this algorithm is faster because of
    node removal code used in this app
    """
    
    res_list = [largest_cc_size(ugraph)]
    
    for attack_node in attack_order:
        delete_node(ugraph, attack_node)
        
        print "nodes left:", len(ugraph.keys())
        res_list.append(largest_cc_size(ugraph))
    
    return res_list


def fast_targeted_order(ugraph):
    """
    Faster algorithm for determining the proper
    node attack order by choosing the highest
    degree nodes first
    """
    
    new_graph = copy_graph(ugraph)
    
    # assumes no skipped node numbers
    num_nodes = len(ugraph)
    
    # make list of set of nodes with degree k
    degree_sets = [set([]) for dummy_idx in range(num_nodes)]
    
    # dictionary that is {node: degree}
    node_deg = compute_node_degrees(ugraph)
    
    # populate list with set of nodes with given degree
    for node in node_deg:
        degree = node_deg[node]
        degree_sets[degree].add(node)
    
    attack_order = []
    # iterate starting with the highest degrees
    for degree in range(num_nodes - 1, -1, -1):
        # keep picking nodes from this highest degree
        while degree_sets[degree] != set([]):
            target_node = degree_sets[degree].pop()

            # update degree_sets with all modified neighbor degrees
            for neighbor in new_graph[target_node]:
                neighbor_deg = len(new_graph[neighbor])

                degree_sets[neighbor_deg].remove(neighbor)
                degree_sets[neighbor_deg - 1].add(neighbor)
            
            # add this node to the attack list
            attack_order.append(target_node)
            # remove this node from the graph
            delete_node(new_graph, target_node)

    return attack_order


def runtime_targeted_UPA(func, num_nodes):
    """
    algorithm that check the run time of both
    targeted_order and fast_targeted_order
    for UPA graphs given n = num_edges and m = 5
    
    Returns the number of seconds to compute
    """
    
    ugraph = UPA_algorithm(5, num_nodes)
    
    # time check block for algorithm
    start = time.time()
    
    func(ugraph)
    
    return time.time() - start


def app2_questions(number):
    if number == 0:
        # debug code
        graph = ER_undirected_generator(50, 0.1)
        start = time.time()
        print compute_resilience2(graph, random_order(graph))
        print
        print "ms to compute:", (time.time() - start) * 1000
    
    elif number == 1:
        network_graph = load_graph(NETWORK_URL)
        # Network Graph Properties:
        # 3047 edges
        # 1239 nodes
        # average degree = 4.92
        #  computed from average_degree
        # ER p = 0.00397292620945
        #  computed from calculate_ER_probability()
        
#        print "total edges in network:", count_edges(network_graph)
#        print

        ER_graph = ER_undirected_generator2(1239, 0.00397292620945)
#        print "total edges in ER graph:", count_edges(ER_graph)
#        print "total nodes in ER graph:", len(ER_graph)
#        print
        
        # choose m approx to be half the average degree
        # this yields a higher edge count in UPA because
        # m is slightly larger in order to be an integer
        deg_m = 3
        UPA_graph = UPA_algorithm(deg_m, 1239 - deg_m)
#        print "total edges in UPA graph:", count_edges(UPA_graph)
#        print "total nodes in UPA graph:", len(UPA_graph)
        
        # this code is used to compute the resilience lists
#        res_graph1 = compute_resilience2(network_graph, random_order(network_graph))
#        res_graph2 = compute_resilience2(ER_graph, random_order(ER_graph))
#        res_graph3 = compute_resilience2(UPA_graph, random_order(UPA_graph))

        # print res_graph
        
        # import precomputed lists 
        res_network = precomputed.res_network_rand
        res_ER = precomputed.res_ER_rand
        res_UPA = precomputed.res_UPA_rand
        
        simpleplot.plot_lines("Resilience of Real Network, ER, and UPA Graphs to a Random Attack",
                              800, 600, "Number of nodes removed", "Largest connected component remaining",
                              [list(enumerate(res_network)),
                               list(enumerate(res_ER)),
                               list(enumerate(res_UPA))],
                              False, ["Real Network", "ER Graph (p = 0.003973)", "UPA Graph (m = 3, n = 1236)"])
    
    elif number == 2:
        # block of code to compute run times
#        tar_order_runtimes = []
#        for num_edges in range(10, 1000, 10):
#            tar_order_runtimes.append(runtime_targeted_UPA(fast_targeted_order, num_edges))
#        print tar_order_runtimes

        # import precomputed values for run times
        tar_order_runtimes = precomputed.tar_order_runtimes
        fast_tar_order_runtimes = precomputed.fast_tar_order_runtimes
        
        total_nodes = range(10, 1000, 10)
        
        simpleplot.plot_lines("Run times of Targeted Order Algorithms on UPA Graph m = 5 (CodeSkulptor)",
                              800, 600, "Number of Additional Nodes n", "Run-time (seconds)",
                              [zip(total_nodes, tar_order_runtimes),
                               zip(total_nodes, fast_tar_order_runtimes)],
                              False, ["Standard Targeted Order", "Fast Targeted Order"])
    
    elif number == 3:
        network_graph = load_graph(NETWORK_URL)
        ER_graph = ER_undirected_generator2(1239, 0.00397292620945)
        deg_m = 3
        UPA_graph = UPA_algorithm(deg_m, 1239 - deg_m)

        # block of code to compute resilience
#        tar_order_list = fast_targeted_order(UPA_graph)
#        res_graph_tar = compute_resilience2(UPA_graph, tar_order_list)
#        print res_graph_tar

        # load precomputed values
        res_network_tar = precomputed.res_network_tar
        res_ER_tar = precomputed.res_ER_tar
        res_UPA_tar = precomputed.res_UPA_tar
        
        simpleplot.plot_lines("Resilience of Real Network, ER, and UPA Graphs to a Targeted Attack",
                              800, 600, "Number of nodes removed", "Largest connected component remaining",
                              [list(enumerate(res_network_tar)),
                               list(enumerate(res_ER_tar)),
                               list(enumerate(res_UPA_tar))],
                              False, ["Real Network", "ER Graph (p = 0.003973)", "UPA Graph (m = 3, n = 1236)"])
    


# graph_obj = graph_view.GraphDrawer(make_complete_graph(18))

app2_questions(3)

