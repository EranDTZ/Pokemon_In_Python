from src.Graph.NodeData import NodeData
from src.Interfaces.GraphInterface import GraphInterface


class DiGraph(GraphInterface):

    def __init__(self):
        """
        Constructor
        """
        self._nodes = {}        # The key is the ID of the node, value is NodeData
        self._edgesInto = {}    # The key is the ID of the dest node, value is {srcID: weight}
        self._edgesOutOf = {}   # The key is the ID of the src node, value is {destID: weight}
        self._mc = 0

    def __repr__(self):
        # return "Nodes:\n "+str(self._nodes)+"\n\nEdges:\n "+str(self._edgesInto)
        STR = "Graph: |V|="+str(self.v_size())+", |E|="+str(self.e_size())+"\n"
        for i in self._nodes.keys():
            if self.all_out_edges_of_node(i) is None:
                if self.all_in_edges_of_node(i) is None:
                    STR += str(i) + ": |edges out|=" + str(0) + "  |edges in|=" + str(0) + ", "
                else:
                    STR += str(i) + ": |edges out|=" + str(0) + "  |edges in|=" + str(len(self.all_in_edges_of_node(i))) + ", "
            else:
                if self.all_in_edges_of_node(i) is None:
                    STR += str(i) + ": |edges out|=" + str(len(self.all_out_edges_of_node(i))) + "  |edges in|=" + str(0) + ", "
                else:
                    STR += str(i) + ": |edges out|=" + str(len(self.all_out_edges_of_node(i))) + "  |edges in|=" + str(len(self.all_in_edges_of_node(i))) + ", "
        return STR
    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return len(self._nodes)

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        size = 0
        for i in self._nodes:
            if i in self._edgesInto.keys():
                size += len(self._edgesInto[i])
        return size

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        return self._nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        return self._edgesInto.get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        return self._edgesOutOf.get(id1)

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self._mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes does not exists the functions will do nothing
        """
        if id1 is id2:        # check if the IDs are the same
            return False
        if weight < 0:      # check if weight is valid
            return False
        if self._nodes.get(id1) is None or self._nodes.get(id2) is None:        # check if the nodes exist
            return False

        if id1 in self._edgesOutOf.keys():      # check if the edge already exists
            if id2 in self._edgesOutOf.get(id1):
                return False

        if id1 in self._edgesOutOf.keys():                  # check if id1 is already in the edgesOutOf dict
            self._edgesOutOf[id1].update({id2: weight})     # if it does, update the new edge
        else:
            self._edgesOutOf[id1] = {id2: weight}           # if it does not exists, initialize it with the new edge

        if id2 in self._edgesInto.keys():                   # check if id2 is already in the edgesInto dict
            self._edgesInto[id2].update({id1: weight})      # if it does, update the new edge
        else:
            self._edgesInto[id2] = {id1: weight}            # if it does not exists, initialize it with the new edge

        self._mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        if self._nodes.get(node_id):    # check if the ID is already taken
            return False
        n = NodeData(node_id, pos)      # create new node

        self._mc += 1
        self._nodes[node_id] = n
        return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        if node_id not in self._nodes.keys():   # check if the node exists
            return False

        if node_id in self._edgesOutOf.keys():  # check if the node has out edges going out of it
            for d in self._edgesOutOf[node_id]:     # for every out edge, go to the relevant edgesInto dict and delete
                self._mc += 1                       # the edge going from the deleted node to the current node (d)
                del self._edgesInto[d][node_id]

            del self._edgesOutOf[node_id]

        if node_id in self._edgesInto.keys():   # check if the node has edges going into it
            for d in self._edgesInto[node_id]:      # for every in edge, go to the relevant edgesOutOf dict and delete
                self._mc += 1                       # the edges going from the current node (d) to the deleted node
                del self._edgesOutOf[d][node_id]

            del self._edgesInto[node_id]

        del self._nodes[node_id]
        self._mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """

        if self._nodes.get(node_id1) is None or self._nodes.get(node_id2) is None:      # check if the nodes exists
            return False
        if node_id1 in self._edgesOutOf.keys():      # check if the specific edge exists, then remove it (inside the if)
            if node_id2 in self._edgesOutOf.get(node_id1):
                del self._edgesInto[node_id2][node_id1]
                del self._edgesOutOf[node_id1][node_id2]
                self._mc += 1
                return True

        return False
