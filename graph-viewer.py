"""
SimpleGUI object to visualize an undirected graph on the canvas

Author: Weikang Sun
Date: 6/23/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_HQvawPHV6L_4.py
"""

import simplegui
import math
import random


class GraphDrawer:
    """
    Class to draw an undirected graph visually on the canvas
    """
    
    def __init__(self, ugraph):
        """
        Initializes the visualizer with the given undirected graph
        as a dictionary
        """
        
        self._window_dimensions = [800, 800]
        self._node_radius = 25
        self._graph = ugraph
        self._random = False
        self._nodes = {}
        
        # creates an object for each node
        self.create_nodes()
        
        # assigns every node a position
        self.assign_node_pos()
        
        # frame stuffs
        frame = simplegui.create_frame("Graph Visualization", 
                                       self._window_dimensions[0],
                                       self._window_dimensions[1])
        frame.set_canvas_background("white")
        frame.set_draw_handler(self.draw_handler)
        
        frame.add_button("Uniform", self.uniform)
        frame.add_button("Random", self.random)

        frame.start()

        
    def create_nodes(self):
        """
        creates an object for each node and appends it
        to a dictionary cooresponding to the name: object
        """
        for node_name in self._graph:
            self._nodes[node_name] = (Node(node_name, self._graph[node_name]))
     
    
    def assign_node_pos(self):
        """
        assigns a position for each node object
        """
        
        size_graph = len(self._nodes)
        radius = min(self._window_dimensions[0], self._window_dimensions[1]) / 2 - 25
        
        for node_name in self._nodes:
            if self._random:
                # put nodes randomly on screen
                self._nodes[node_name].set_position([random.randrange(self._window_dimensions[0]),
                                                    random.randrange(self._window_dimensions[1])])
            else:
                # spread nodes evenly in a circle
                # does this by calculating the coordinates using polar geometry
                # given the index of the node around the circle
                position = [self._window_dimensions[0] / 2 
                            + radius * math.sin(2 * math.pi / size_graph * 
                                                self._nodes.keys().index(node_name)),
                            self._window_dimensions[1] / 2
                            - radius * math.cos(2 * math.pi / size_graph * 
                                                self._nodes.keys().index(node_name))]
    
                self._nodes[node_name].set_position(position)
    def uniform(self):
        """
        Button handler to toggle uniform node distribution (circle)
        """
        self._random = False
        self.assign_node_pos()
    
    
    def random(self):
        """
        Button handler to toggle random node distribution
        """
        self._random = True
        self.assign_node_pos()
     
    
    def draw_handler(self, canvas):
        """ draw handler """
        # draws the edges
        for head_name in self._nodes:
            for tail_name in self._nodes[head_name].get_edges():
                canvas.draw_line(self._nodes[head_name].get_position(),
                                 self._nodes[tail_name].get_position(), 2, "black")
                
        # draws the circles and names for the node
        for node_name in self._nodes:
            canvas.draw_circle(self._nodes[node_name].get_position(),
                               self._node_radius, 2, "black", "white")
            canvas.draw_text(self._nodes[node_name].get_name(), 
                             [self._nodes[node_name].get_position()[0] - 5,
                              self._nodes[node_name].get_position()[1] + 5],
                             25, "black")



class Node:
    """
    This is a node object which contains information about its location
    """
    
    def __init__(self, name, edges):
        """
        Initializes a node object which has the node name,
        a set of edges it is connected to, and a location
        """
        self._name = str(name)
        self._edges = edges
        self._position = []
        
        
    def get_position(self):
        """ returns the node position """
        return self._position
    
    
    def set_position(self, coord):
        """ sets the node position """
        self._position = coord
        
        
    def get_name(self):
        """ returns the node name """
        return self._name
    
    
    def get_edges(self):
        """ returns the set of edges connected to that node """
        return self._edges
