"""
Code for Application 3 of
Algorithmic Thinking Part 2

Author: Weikang Sun
Date: 7/23/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_j0MzNeCop8_15.py
"""

import math
import codeskulptor
import random
import user40_9ITqL4NrrPIcE4c as clustering
import simpleplot
import alg_cluster
import time
import urllib2

codeskulptor.set_timeout(3000)

###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def gen_random_clusters(num_clusters):
    """ 
    Function to generate a list of clusters randomly
    located in the square (+-1, +-1) with 
    population = 1 and risk = 1
    
    input: how many clusters to generate
    output: list of Cluster objects
    """
    
    width = 2.0
    lower = -1.0
    cluster_list = []
    
    for index in range(num_clusters):
        
        rand_point = (random.random() * width + lower,
                      random.random() * width + lower)
        cluster_list.append(alg_cluster.Cluster(
                set([index]), rand_point[0], rand_point[1], 1, 1))
        
    return cluster_list


def print_clusters(cluster_list):
    """ Helper function to print list of clusters """
    
    for cluster in cluster_list:
        print cluster
        
        
def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]

        
def application_part(part):
    """ function to run a question in the application """
    
    if part is 1:
        # get timings of slow_closest_pairs and fast_closest_pairs
        timing_slow = {}
        timing_fast = {}
        
        for num_clusters in range(2, 200):
            cluster_list = gen_random_clusters(num_clusters)
            
            the_time = time.time()
            clustering.slow_closest_pairs(cluster_list)
            timing_slow[num_clusters] = time.time() - the_time
        
            the_time = time.time()
            clustering.fast_closest_pairs(cluster_list)
            timing_fast[num_clusters] = time.time() - the_time
            
        simpleplot.plot_lines("Running Times of Two Cluster Closest-Pair Algorithms",
                              800, 600, "Number of Clusters", "Run-time (sec)",
                              [timing_slow, timing_fast], False,
                              ["slow_closest_pair", "fast_closest_pair"])
    elif part is 2:
        # get errors resulting from using clustering algorithms
        data_table = load_data_table(DATA_111_URL)
    
        singleton_list = []
        for line in data_table:
            singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
        #cluster_list = clustering.hierarchical_clustering(list(singleton_list), 9)
        cluster_list = clustering.kmeans_clustering(list(singleton_list), 9, 5)
        
        distortion = 0
        
        for cluster in cluster_list:
            distortion += cluster.cluster_error(data_table)
        
        print "Distortion:", distortion
    
    elif part is 3:
        # get quality of clusterings produced by algorithms 
        # as a function of clusters, using 111 data set
        data_table = load_data_table(DATA_896_URL)
    
        # k means
        singleton_list_kmns = []
        for line in data_table:
            singleton_list_kmns.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
        distortion_kmns = {}
        
        cluster_list = singleton_list_kmns
        
        for num_clusters in range(20, 5, -1):
            cluster_list = clustering.kmeans_clustering(cluster_list, num_clusters, 5)
            
            distortion = 0
            for cluster in cluster_list:
                distortion += cluster.cluster_error(data_table)
                
            distortion_kmns[num_clusters] = distortion
        
        # hierarchical
        singleton_list_hier = []
        
        for line in data_table:
            singleton_list_hier.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
        distortion_hier = {}
        
        cluster_list = singleton_list_hier
        
        for num_clusters in range(20, 5, -1):
            cluster_list = clustering.hierarchical_clustering(cluster_list, num_clusters)
        
            distortion = 0
            for cluster in cluster_list:
                distortion += cluster.cluster_error(data_table)
                
            distortion_hier[num_clusters] = distortion
        
        simpleplot.plot_lines("Distortion (error) of Two Clustering Algorithms on 896 Counties",
                              800, 600, "Number of Clusters", "Distortion",
                              [distortion_hier, distortion_kmns], False,
                              ["Hierarchical", "k-means"])
        
    pass

        
application_part(3)        
        
