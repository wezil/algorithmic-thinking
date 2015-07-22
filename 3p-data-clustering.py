"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane

cluster_list columns:
set of fips code (set of int)
x center (float)
y center (float)
population (int)
cancer risk (float)

Author: Weikang Sun
Date: 7/20/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_9ITqL4NrrPIcE4c.py
"""

import math
import alg_cluster
import urllib2


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def min_distance(tuple1, tuple2):
    """
    helper function to determine which tuple distance is smaller and returns that tuple
    tuples have form (distance, idx1, idx2)
    """
    
    if tuple1[0] < tuple2[0]:
        return tuple1
    else:
        return tuple2


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    
    # initialize distance to infinity
    closest_pair = (float("inf"), -1, -1)
    
    # iterate over all pairs of unique indices in cluster_list
    for idx_u in range(len(cluster_list)):
        for idx_v in range(len(cluster_list)):
            if idx_u != idx_v:
                # get distance between two clusters
                distance = pair_distance(cluster_list, idx_u, idx_v)
                
                # update tuple min distance
                closest_pair = min_distance(distance, closest_pair)
    
    return closest_pair


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    
    # initialize closest distance to infinity
    closest_pair = (float("inf"), -1, -1)
    size_list = len(cluster_list)
    
    # for small list simply use the slow algorithm
    if size_list <= 3:
        return slow_closest_pair(cluster_list)
    else:
        # compute midpoint and divide into two sub problems
        midpoint = size_list // 2
        # split cluster_list into two sub lists
        cluster_left = cluster_list[0 : midpoint]
        cluster_right = cluster_list[midpoint : ]
        
        # recursively find closest distance
        closest_left = fast_closest_pair(cluster_left)
        closest_right = fast_closest_pair(cluster_right)
        closest_right = (closest_right[0], closest_right[1] + midpoint, 
                              closest_right[2] + midpoint)

        # appropriately determine closest_pair
        closest_pair = min_distance(closest_left, closest_right)
        
        # compute center line of these clusters    
        center_line = 0.5 * (cluster_list[midpoint - 1].horiz_center() + 
                             cluster_list[midpoint].horiz_center())
        
        # determine the closest clusters in vertical distance
        closest_strip = closest_pair_strip(cluster_list, center_line, closest_pair[0])
        
        # appropriately determine closest_pair
        closest_pair = min_distance(closest_pair, closest_strip)
    
    return closest_pair


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    
    # get a list of all clusters within the strip of the center line
    index_list = [index for index in range(len(cluster_list))
                  if abs(cluster_list[index].horiz_center() - horiz_center) < half_width]
    # sort the index list by cooresponding cluster y coordiante        
    merge_sort_index(cluster_list, index_list)

    size_strip = len(index_list) 
    closest_pair = (float("inf"), -1 , -1)
    
    # for each index, iterate and check the next three indices up until the end
    for idx_u in range(size_strip - 1):
        for idx_v in range(idx_u + 1, min(idx_u + 4, size_strip)):
            strip_distance = pair_distance(cluster_list, index_list[idx_u], index_list[idx_v])
            closest_pair = min_distance(closest_pair, strip_distance)
    
    return closest_pair
            
 
def merge_sort_index(cluster_list, index_list):
    """
    Helper function for perfoming the merge sort algorithm on an indexed list 
    of clusters, based on their vertical positions
    
    Input: a master cluster list, and an index list to be sorted
    """
    
    if len(index_list) > 1:
        midpoint = len(index_list) // 2
        left = list(index_list[0: midpoint])
        right = list(index_list[midpoint: ])
        merge_sort_index(cluster_list, left)
        merge_sort_index(cluster_list, right)
        merge_index(cluster_list, left, right, index_list)

        
def merge_index(cluster_list, left, right, index_list):
    """
    Merging component of the merge sort algorithm comparing vertical position
    
    Input: left, right, and original index list, alongside the master list of clusters
    """
    
    idx_i = 0
    idx_j = 0
    idx_k = 0
    
    while idx_i < len(left) and idx_j < len(right):
        if cluster_list[left[idx_i]].vert_center() <= cluster_list[right[idx_j]].vert_center():
            index_list[idx_k] = left[idx_i]
            idx_i += 1
        else:
            index_list[idx_k] = right[idx_j]
            idx_j += 1
        idx_k += 1
        
    if idx_i == len(left):
        index_list[idx_k:] = right[idx_j:]
    else:
        index_list[idx_k:] = left[idx_i:]
    

def print_cluster(cluster_list):
    """ Helper method for printing list of clusters """
    
    for cluster in cluster_list:
        print cluster
        

######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    # make sure cluster list is sorted first
    merge_sort_cluster_x(cluster_list)
    
    # mutates cluster_list every iteration!
    while len(cluster_list) > num_clusters:
        closest_pair = fast_closest_pair(cluster_list)
        # get those two clusters from list
        cluster_i = cluster_list.pop(closest_pair[1])
        cluster_j = cluster_list.pop(closest_pair[2] - 1)
        # append to list the new merged cluster
        cluster_list.append(cluster_i.merge_clusters(cluster_j))
        # remember to resort the clusters now before calling fast_closest_pair
        merge_sort_cluster_x(cluster_list)
    
    return cluster_list


def merge_sort_cluster_x(cluster_list):
    """
    Helper function to merge sort a cluster_list based on 
    the x-center
    
    input: list of clusters
    """
    
    if len(cluster_list) > 1:
        midpoint = len(cluster_list) // 2
        left = list(cluster_list[0: midpoint])
        right = list(cluster_list[midpoint: ])
        merge_sort_cluster_x(left)
        merge_sort_cluster_x(right)
        merge_clusters_x(left, right, cluster_list)
        

def merge_clusters_x(left, right, cluster_list):
    """
    Helper function that is second part of merge sort algorithm
    Will sort by increasing x-coordinate in each cluster
    
    input: left half, right half, and original cluster_list
    """
    
    idx_i = 0
    idx_j = 0
    idx_k = 0
    
    while idx_i < len(left) and idx_j < len(right):
        if left[idx_i].horiz_center() < right[idx_j].horiz_center():
            cluster_list[idx_k] = left[idx_i]
            idx_i += 1
        else:
            cluster_list[idx_k] = right[idx_j]
            idx_j += 1
        idx_k += 1
        
        if idx_i == len(left):
            cluster_list[idx_k: ] = right[idx_j: ]
        else:
            cluster_list[idx_k: ] = left[idx_i: ]
            

######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    list_size = len(cluster_list)
    # sort by increasing total population
    cluster_list_copy = list(cluster_list)
    merge_sort_cluster_population(cluster_list_copy)
    # pick k initial cluster centers based on highest population clusters
    k_centers = cluster_list_copy[list_size - num_clusters: ]
    
    # iterate specified times
    for dummy_idx in range(num_iterations):
        # initialize list of k empty cluster sets
        k_clusters = [alg_cluster.Cluster(set([]), 0, 0, 0, 0)
                      for dummy_cluster in range(num_clusters)]
        
        # iterate over all clusters
        for cluster in cluster_list:
            # determine which center this cluster is closest to
            closest_center = (float("inf"), float("inf"))
            for center in k_centers:
                distance_to_center = pair_distance([center, cluster], 0, 1)
                closest_center = min_distance(closest_center, 
                                              (distance_to_center[0], 
                                               k_centers.index(center)))
            # merge this cluster into the cluster center
            k_clusters[closest_center[1]].merge_clusters(cluster)
            
        k_centers = list(k_clusters)
        
    return k_centers


def merge_sort_cluster_population(cluster_list):
    """
    Helper method to sort cluster list by population size using merge sort
    
    input: cluster list
    """
    
    if len(cluster_list) > 1:
        midpoint = len(cluster_list) // 2
        left = list(cluster_list[0: midpoint])
        right = list(cluster_list[midpoint: ])
        merge_sort_cluster_population(left)
        merge_sort_cluster_population(right)
        merge_cluster_population(left, right, cluster_list)
        

def merge_cluster_population(left, right, cluster_list):
    """
    Helper method to merge cluster list by population size
    
    input: left, right, and original cluster list to be sorted by pop
    """
    
    idx_i = 0
    idx_j = 0
    idx_k = 0
    
    while idx_i < len(left) and idx_j < len(right):
        if left[idx_i].total_population() < right[idx_j].total_population():
            cluster_list[idx_k] = left[idx_i]
            idx_i += 1
        else:
            cluster_list[idx_k] = right[idx_j]
            idx_j += 1
        idx_k += 1
        
        if idx_i == len(left):
            cluster_list[idx_k: ] = right[idx_j: ]
        else:
            cluster_list[idx_k: ] = left[idx_i: ]

