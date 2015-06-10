"""
Application  of Module 1
Imports physics citation graph and performs analysis of the graph.

This app also generates graphs based on the DPA algorithm
which describes the hierarchical structure of networks 
(also known as scale-free, hierarchical model). 

Author: Weikang Sun
Date: 6/8/15

codeskulptor source:
http://www.codeskulptor.org/#user40_BnaovpCwUO_11.py
"""

# general imports
import urllib2
import simpleplot
import math
import random

# importing graph degree code
import user40_jdtGmYLlQ1_5 as deg_analysis

# import the fast DPA algorithm
import alg_dpa_trial

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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



def plot_indeg_distribution(graph_dictionary, ref_str, plot_type):
    """
    Part 1: graphs the log-log plot of the 
    normalized in-degree distribution for
    the input dictionary called ref_str
    """

    # gets the unnormalized distribution and normalizes it
    graph_dist = deg_analysis.in_degree_distribution(graph_dictionary)

    sum_total = 0.0
    for key in graph_dist.keys():
        sum_total += graph_dist[key]

    graph_dist_norm = {}
    for key in graph_dist.keys():
        graph_dist_norm[key] = graph_dist[key]/sum_total

    # creates the log/log data set
    graph_dist_log = {}
    for key in graph_dist_norm.keys():
        graph_dist_log[math.log(key, 10)] = math.log(graph_dist_norm[key], 10)

    # graph types    
    if plot_type == "LOGLOG":
        simpleplot.plot_scatter("LogLog of Normalized In-Degree Distribution for " + ref_str,
                                800, 600, "Log Degree", "Log Amount", [graph_dist_log])
    elif plot_type == "NORMAL":
        simpleplot.plot_scatter("Normalized In-Degree Distribution for " + ref_str,
                                800, 600, "Degree", "Amount", [graph_dist_norm])
    elif plot_type == "BARS":
        simpleplot.plot_bars("Bar Plot of Normalized In-Degree Distribution for " + ref_str,
                             800, 600, "Degree", "Amount", [graph_dist_norm])

def ER_directed_generator(nodes, edge_prob, ref_str):
    """
    Part 2: generates a random directed graph
    with node size node_size and
    an edge probability edge_prob 
    """
    
    nodeset = range(nodes)
    
    # generates the graph with appropriate edge probability
    generated_graph = {}
    
    for tail in nodeset:
        generated_graph[tail] = set([])
        for head in nodeset:
            if tail != head and random.random() < edge_prob:
                generated_graph[tail].add(head)
    
    # print_dic_lines(generated_graph)
    
    plot_indeg_distribution(generated_graph, "Directed ER() Graph", ref_str)

def num_graph_nodes(graph_dictionary):
    """
    Part 3: prints the number of keys or nodes in the graph
    
    Returns: the number of nodes
    """
    
    counter = 0
    for dummy_key in graph_dictionary.keys():
        counter += 1
        
    print "Number of nodes:", counter
    return counter
    
def graph_avg_outdeg(graph_dictionary):
    """
    Part 3: calculates the average out-degree
    for all the nodes in the graph
    
    Returns: the average out-degree of all nodes
    """
    
    # adds the number of citations for every node
    counter = 0
    for key in graph_dictionary.keys():
        counter += len(graph_dictionary[key])
    
    # take the average
    average = counter / float(len(graph_dictionary.keys()))
    
    print "Average out-degree:", average
    return average

def DPA_algorithm(complete_nodes, additional_nodes):
    """
    Implementation of the DPA algorithm which generates 
    a complete graph with complete_nodes and appends
    additional_nodes with certain probability
    """
    
    # generates the complete graph m nodes
    complete_graph = deg_analysis.make_complete_graph(complete_nodes)
    
    # creates the new DPA trial algorithm object
    dpa_object = alg_dpa_trial.DPATrial(complete_nodes)
    
    # adds a new node number with randomly chosen heads in updated graph
    for node in range(complete_nodes, complete_nodes + additional_nodes):
        complete_graph[node] = dpa_object.run_trial(complete_nodes)

    plot_indeg_distribution(complete_graph, "DPA Algorithm (m=13, n=27770)", "LOGLOG")
    
def print_dic_lines(dictionary):
    """
    helper method to print dictionary 
    for debugging purposes
    """
    
    for key in dictionary.keys():
        print dictionary[key]
    
def app_run_part(part_num):
    """
    simple method to execute a certain part 
    of the application 
    """
    #try:
    # plot the citation graph on Log log
    if part_num == 1:
        # this could take a while to generate
        citation_graph = load_graph(CITATION_URL)
        plot_indeg_distribution(citation_graph, "Physics Papers", "LOGLOG")

    # plot a generated directed ER graph
    elif part_num == 2:
        ER_directed_generator(500, 0.5, "LOGLOG")

    # display the citation graph node and out-deg info
    elif part_num == 3:
        # this could take awhile to generate
        citation_graph = load_graph(CITATION_URL)
        num_graph_nodes(citation_graph)
        graph_avg_outdeg(citation_graph)

    # generate a DPA graph generated with same parameters as citation graph
    elif part_num == 4:
        # citation_graph = load_graph(CITATION_URL)
        # DPA_algorithm(math.ceil(graph_avg_outdeg(citation_graph)),
        #               num_graph_nodes(citation_graph))

        DPA_algorithm(13, 27770)
            
#    except:
#        print "I'm afraid I cannot do that."

app_run_part(4)
