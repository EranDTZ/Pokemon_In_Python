from src.Interfaces.GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph
from src.Interfaces import GraphInterface

import json
from typing import List
from queue import PriorityQueue
import itertools

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.backends.backend_agg as agg
import pygame
from pygame.locals import *
import easygui


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g = None):
        """
        Init the graph, prepares the variables for the GUI and gives it a name
        :param g:
        """
        if g is None:
            self._Graph = DiGraph()
        else:
            self._Graph = g

        self.name = ""
        self.centerToggle = False
        self.currList = []
        if self._Graph.e_size() > 200:
            self.edgeToggle = False
        else:
            self.edgeToggle = True


    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self._Graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        temp = self._Graph
        try:    # the following 7 lines are standard method of reading json file in python

            self._Graph = DiGraph()
            with open(file_name, "r") as file:
                data = json.load(file)
            for newNode in data.get("Nodes"):
                self._Graph.add_node(newNode.get("id"), newNode.get("pos"))

            for newEdge in data.get("Edges"):
                self._Graph.add_edge(newEdge.get("src"), newEdge.get("dest"), newEdge.get("w"))

            self.name = file_name.split("/")[len(file_name.split("/"))-1][:-5]
            # self.name = split the file_name by "/", then take the last split (which is the
            # file's name. then remove the last 5 characters, which are: ".json" for every
            # json file
            if self.edgeToggle:
                if self._Graph.e_size() > 200:
                    self.edgeToggle = False
                else:
                    self.edgeToggle = True

            return True


        except:
            self._Graph = temp
            return False

    def save_to_json(self, file_name: str) -> bool:
        """
        saves the graph into a new json file.
        The function WILL override any existing graph if the name is taken.
        :param file_name:
        :return:
        """
        try:
            nodes = []
            edges = []
            for currNode in self._Graph._nodes.values():
                nodes.append({"pos": str(currNode.pos), "id": currNode.id})

            for destNode in self._Graph._edgesInto.items():
                for srcNode in destNode[1].items():
                    edges.append({"src": srcNode[0], "w": srcNode[1], "dest": destNode[0]})


            graphdict = {}
            graphdict["Edges"] = edges
            graphdict["Nodes"] = nodes

            with open(file_name, "w") as file:
                json.dump(graphdict, fp=file)
            return True
        except:
            return False

    def dijkstra(self, id: int):
        """
        This function creates a dictionary 'D' which holds in tuples the distance for each node,
        and it's parent node in the path. The key is the destinations node of that particular path.

        This function is an direct implementation of Dijkstra's algorithm using Priority Queue.
        :param source id:
        :return: D
        """
        D = {}
        for node in self._Graph._nodes.keys():
            D[node] = float('inf'), node
        D[id] = 0, id

        currNode = id

        pq = PriorityQueue()
        pq.put((0, currNode))
        while not pq.empty():
            (currWeight, currNode) = pq.get()
            self._Graph._nodes.get(currNode).tag = 1
            if self._Graph._edgesOutOf.get(currNode) is not None:
                for neighborNode in self._Graph._edgesOutOf.get(currNode).keys():
                    if self._Graph._nodes.get(neighborNode).tag == 0:
                        if D[neighborNode][0] > D[currNode][0] + self._Graph._edgesOutOf.get(currNode).get(neighborNode):
                            pq.put((D[currNode][0] + self._Graph._edgesOutOf.get(currNode).get(neighborNode), neighborNode))
                            D[neighborNode] = D[currNode][0] + self._Graph._edgesOutOf.get(currNode).get(neighborNode), currNode

        for node in self._Graph._nodes:
            self._Graph._nodes.get(node).tag = 0

        return D

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Example:
#      >>> from GraphAlgo import GraphAlgo
#       >>> g_algo = GraphAlgo()
#        >>> g_algo.addNode(0)
#        >>> g_algo.addNode(1)
#        >>> g_algo.addNode(2)
#        >>> g_algo.addEdge(0,1,1)
#        >>> g_algo.addEdge(1,2,4)
#        >>> g_algo.shortestPath(0,1)
#        (1, [0, 1])
#        >>> g_algo.shortestPath(0,2)
#        (5, [0, 1, 2])
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """

        if self._Graph._nodes.get(id1) is None or self._Graph._nodes.get(id2) is None:
            return float('inf'), []

        pathDict = self.dijkstra(id1)
        if pathDict[id2][0] >= float('inf'):
            return pathDict[id2][0], []

        list = []
        currID = id2
        while currID is not id1:
            list.append(currID)
            currID = pathDict[currID][1]

        list.append(id1)
        list.reverse()

        return pathDict[id2][0], list

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        If the amount of stops in node_lst is fewer then 6, we will calculate each permutation.
        Else, (the amount of stops is greater then 5), we will use a greedy TSP algorithm.
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """
        if len(node_lst) < 6:   # then do all permutations
            currDict = {}
            for i in node_lst:
                if i in self._Graph._nodes.keys():
                    currDict[i] = self.dijkstra(i)

            minW = float('inf')
            minPermID = -1
            allPerm = list(itertools.permutations(node_lst))    #O(n!) when n<=5 (therefore O(120)) n*dijikstra * n!
            for i in range(len(allPerm)):
                currW = 0
                for j in range(len(node_lst)-1):
                    currW += currDict[allPerm[i][j]][allPerm[i][j+1]][0]
                if currW < minW:
                    minW = currW
                    minPermID = i


            final_list = []
            llist = []
            for j in range(len(allPerm[i])-1):
                llist.append(self.shortest_path(allPerm[minPermID][j], allPerm[minPermID][j+1])[1])

            for i in llist:
                for j in i:
                    if j not in final_list:
                        final_list.append(j)

            return final_list, minW
        else:
            return self.greedyTSP(node_lst)

    def greedyTSP(self, node_lst: List[int]) -> (List[int], float):     #O(n^2)
        """
        This greedyTSP algorithm is used when there are too many stops in the TSP query,
        it does NOT return the correct answer every time. But the time-complexity is acceptable.
        :param node_lst: list of stops.
        :return: A list of the nodes id's in the path, and the overall distance
        """
        currDict = {}
        list = []
        for i in node_lst:
            currDict[i] = self.dijkstra(i)


        currID = node_lst[0]
        node_lst.remove(currID)
        while len(node_lst) != 0:                   # for each node in the given list       O(n)
            closestW = float('inf')
            closestID = -1
            for n in currDict[currID]:              # for each neighbour of the current node O(n)
                if n in node_lst and n != currID:
                    if closestW > currDict[currID][n][0]:
                        closestW = currDict[currID][n][0]
                        closestID = n
            list.append(self.shortest_path(currID, closestID))
            currID = closestID
            node_lst.remove(closestID)

        sumw = 0
        final_list = []
        for i in list:
            sumw += i[0]
            for j in i[1]:
                if j not in final_list:
                    final_list.append(j)

        return final_list, sumw

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """
        # currID
        # currMax
        overallMin = float('inf')
        center = -1
        for currID in self._Graph._nodes:
            currDict = self.dijkstra(currID)
            maxID = max(currDict, key=currDict.get)
            maxW = currDict[maxID][0]
            if maxW >= float('inf'):
                return -1, float('inf')
            if maxW < overallMin:
                center = currID
                overallMin = maxW

        return center, overallMin

    def drawGraph(self): # https://www.southampton.ac.uk/~feeg1001/notebooks/Matplotlib.html
                         # http://www.pygame.org/wiki/MatplotlibPygame
        """
        This function calculate the matplotlib graph for the advanced GUI.
        :return: The graph itself ready to be presented in pygame.
        """
        fig, axes = plt.subplots(figsize=(7, 5))
        axes.set_title("Graph "+self.name+"", {'fontname': 'Courier New'}, fontsize=20)


        for node in self._Graph._nodes.values():
            plt.scatter(node.pos[0], node.pos[1], s=20, color="red")
            plt.text(node.pos[0]+0.00002, node.pos[1] + 0.00006, str(node.id), color="red", fontsize=10)

        if self.centerToggle:
            centerID = self.centerPoint()[0]
            if centerID != -1:
                node = self._Graph._nodes.get(centerID)
                plt.scatter(node.pos[0], node.pos[1], s=45, color="blue")

        for id in self.currList:
            node = self._Graph._nodes.get(id)
            plt.scatter(node.pos[0], node.pos[1], s=45, color="blue")

        ecount = 0
        if self.edgeToggle:
            for dest in self._Graph._nodes.values():
                currDict = self._Graph.all_out_edges_of_node(dest.id)
                destx = dest.pos[0]
                desty = dest.pos[1]
                if currDict is not None:
                    for currEdge in currDict:
                       srcx = self._Graph._nodes.get(currEdge).pos[0]
                       srcy = self._Graph._nodes.get(currEdge).pos[1]
                       plt.annotate("", xy=(srcx, srcy), xytext=(destx, desty), arrowprops=dict(arrowstyle="->"))
                       ecount += 1

        return fig

    def plot_graph(self) -> None:
        """
        This is the function that manage the GUI.
        First the user will be asked if he wants to use the advanced GUI (with buttons) or just
        draw the graph using just matplotlib.
        """
        GUI = easygui.boolbox("Do you want simple or advanced GUI?\n *advanced GUI is WIP and likely to crash when given wrong inputs\nbut do play with it :)", choices=("Advanced", "Simple"))
        if GUI:
            self.advancedGUI()
        else:
            fig, axes = plt.subplots(figsize=(7, 5))
            axes.set_title("Graph " + self.name + "", {'fontname': 'Courier New'}, fontsize=20)

            for node in self._Graph._nodes.values():
                plt.scatter(node.pos[0], node.pos[1], s=20, color="red")
                plt.text(node.pos[0] + 0.00002, node.pos[1] + 0.00006, str(node.id), color="red", fontsize=10)

            ecount = 0
            for dest in self._Graph._nodes.values():
                currDict = self._Graph.all_out_edges_of_node(dest.id)
                destx = dest.pos[0]
                desty = dest.pos[1]
                if currDict is not None:
                    for currEdge in currDict:
                        srcx = self._Graph._nodes.get(currEdge).pos[0]
                        srcy = self._Graph._nodes.get(currEdge).pos[1]
                        plt.annotate("", xy=(srcx, srcy), xytext=(destx, desty), arrowprops=dict(arrowstyle="->"))
                        ecount += 1

            if ecount != self._Graph.e_size():
                print("error has been occurred")
            else:
                plt.show()

    def advancedGUI(self)  -> None:
        """
        This function runs the advanced GUI.
        Creates the buttons and update the matplotlib that is presented in pygame.
        """
        matplotlib.use("Agg")

        fig = self.drawGraph()

        pygame.font.init()
        myfont = pygame.font.SysFont('Courier New', 15)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()



        pygame.init()

        window = pygame.display.set_mode((800, 500), DOUBLEBUF)
        screen = pygame.display.get_surface()

        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (0, 0))
        pygame.draw.rect(screen, (100, 150, 200), [700, 0, 100, 25])
        pygame.draw.rect(screen, (100, 200, 150), [700, 25, 100, 25])
        pygame.draw.rect(screen, (150, 100, 200), [700, 50, 100, 25])
        pygame.draw.rect(screen, (100, 150, 200), [700, 75, 100, 25])
        pygame.draw.rect(screen, (100, 200, 150), [700, 100, 100, 25])
        pygame.draw.rect(screen, (150, 100, 200), [700, 125, 100, 25])
        pygame.draw.rect(screen, (100, 150, 200), [700, 350, 100, 25])
        pygame.draw.rect(screen, (100, 200, 150), [700, 375, 100, 25])
        pygame.draw.rect(screen, (150, 100, 200), [700, 400, 100, 25])
        pygame.draw.rect(screen, (100, 150, 200), [700, 425, 100, 25])
        pygame.draw.rect(screen, (100, 200, 150), [700, 450, 100, 25])
        pygame.draw.rect(screen, (150, 100, 200), [700, 475, 100, 25])
        loadgraphtext = myfont.render("load", False, (0, 0, 0))
        savegraphtext = myfont.render("save", False, (0, 0, 0))
        centertext = myfont.render("center", False, (0, 0, 0))
        pathtext = myfont.render("path", False, (0, 0, 0))
        unpathtext = myfont.render("clear path", False, (0, 0, 0))
        tsptext = myfont.render("tsp", False, (0, 0, 0))
        removenodetext = myfont.render("remove node", False, (0, 0, 0))
        addnodetext = myfont.render("add node", False, (0, 0, 0))
        connecttext = myfont.render("connect", False, (0, 0, 0))
        disconnecttext = myfont.render("disconnect", False, (0, 0, 0))
        edgetext = myfont.render("show edges", False, (0, 0, 0))
        screen.blit(loadgraphtext, (705, 2.5))
        screen.blit(savegraphtext, (705, 30.5))
        screen.blit(centertext, (705, 57))
        screen.blit(pathtext, (705, 83))
        screen.blit(unpathtext, (702, 100))
        screen.blit(tsptext, (705, 127))
        screen.blit(removenodetext, (702, 350))
        screen.blit(addnodetext, (705, 375))
        screen.blit(connecttext, (702, 400))
        screen.blit(disconnecttext, (705, 425))
        screen.blit(edgetext, (705, 450))
        pygame.display.flip()
        crashed = False
        updated = False
        while not crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 700 < pos[0] < 800 and 0 < pos[1] < 25:
                        graphname = easygui.enterbox("Enter the name of the graph you want to load\n NO NEED to enter data/... or ..json")
                        self.load_from_json("data/"+graphname+".json")
                        self.currList = []
                        updated = True
                    if 700 < pos[0] < 800 and 75 > pos[1] > 50:
                        if self.centerToggle:
                            self.centerToggle = False
                        else:
                            self.centerToggle = True
                        updated = True
                    if 700 < pos[0] < 800 and 50 > pos[1] > 25:
                        newname = easygui.enterbox("Name your graph\n DO NOT add .json\n you WILL override the existing graph")
                        self.save_to_json(newname)
                    if 700 < pos[0] < 800 and 100 > pos[1] > 75:
                        src = int(easygui.enterbox("Enter your source ID\n enter an empty string for removing current path"))
                        dest = int(easygui.enterbox("Enter your destination ID\n enter an empty string for removing current path"))
                        self.currList = self.shortest_path(src, dest)[1]
                        updated = True
                    if 700 < pos[0] < 800 and 125 > pos[1] > 100:
                        self.currList = []
                        updated = True
                    if 700 < pos[0] < 800 and 150 > pos[1] > 125:
                        stops = int(easygui.enterbox("how many STOPS do you want to make?"))
                        self.currList = []
                        tsplist = []
                        for i in range(stops):
                            tsplist.append(int(easygui.enterbox("enter a stop "+str(i+1)+"/"+str(stops))))
                        self.currList = self.TSP(tsplist)[0]
                        updated = True
                    if 700 < pos[0] < 800 and 375 > pos[1] > 350:
                        self._Graph.remove_node(int(easygui.enterbox("Which node to remove?")))
                        updated = True
                    if 700 < pos[0] < 800 and 400 > pos[1] > 375:
                        pos = ""
                        ID = int(easygui.enterbox("Enter new ID\n Make sure this ID is not taken"))
                        x = easygui.enterbox("Enter X \n enter -1 for random location")
                        if x != "-1":
                            y = easygui.enterbox("Enter Y")
                            pos = x+","+y+","+"0"
                        else:
                            pos = None
                        self._Graph.add_node(ID, pos)
                        updated = True

                    if 700 < pos[0] < 800 and 425 > pos[1] > 400:
                        src = int(easygui.enterbox("Enter source ID\nMake sure it exists"))
                        dest = int(easygui.enterbox("Enter destination ID\nMake sure it exists"))
                        weight = float(easygui.enterbox("Enter weight\n positive (and zero) values only"))
                        self._Graph.add_edge(src, dest, weight)
                        updated = True

                    if 700 < pos[0] < 800 and 450 > pos[1] > 425:
                        src = int(easygui.enterbox("Enter source ID\nMake sure it exists"))
                        dest = int(easygui.enterbox("Enter destination ID\nMake sure it exists"))
                        self._Graph.remove_edge(src, dest)
                        updated = True

                    if 700 < pos[0] < 800 and 475 > pos[1] > 450:
                        if self.edgeToggle:
                            self.edgeToggle = False
                        else:
                            self.edgeToggle = True
                        updated = True

                if updated:
                    plt.close(fig)
                    fig = self.drawGraph()
                    canvas = agg.FigureCanvasAgg(fig)
                    canvas.draw()
                    renderer = canvas.get_renderer()
                    raw_data = renderer.tostring_rgb()
                    surf = pygame.image.fromstring(raw_data, size, "RGB")
                    screen.blit(surf, (0, 0))
                    pygame.display.flip()
                    updated = False