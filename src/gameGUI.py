from src.Graph.GraphAlgo import GraphAlgo
from client_python.client import Client
import algo
from src.Graph.GraphAlgo import GraphAlgo

import pygame
from pygame import *


class gameGUI:


    def __init__(self, g: GraphAlgo, screen: pygame.display, client: Client):
        self.screen = screen
        self.g = g
        self.client = client
        self.min_x = min(list(g.get_graph().get_all_v().values()), key=lambda n: n.pos[0]).pos[0]
        self.min_y = min(list(g.get_graph().get_all_v().values()), key=lambda n: n.pos[1]).pos[1]
        self.max_x = max(list(g.get_graph().get_all_v().values()), key=lambda n: n.pos[0]).pos[0]
        self.max_y = max(list(g.get_graph().get_all_v().values()), key=lambda n: n.pos[1]).pos[1]
        self.FONT = pygame.font.SysFont('Arial', 20, bold=True)

    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        if x:
            return self.scale(data, 200, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return self.scale(data, 150, self.screen.get_height() - 50, self.min_y, self.max_y)

    def drawGraph(self):
        "draw nodes"
        for n in self.g.get_graph().get_all_v().values():
            srcx = self.my_scale(n.pos[0], x=True)
            srcy = self.my_scale(n.pos[1], y=True)
            pygame.draw.circle(self.screen, (100, 0, 0), (srcx, srcy), 20)
            id_srf = self.FONT.render(str(n.id), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(srcx, srcy))
            self.screen.blit(id_srf, rect)
            "draw edges"
            for e in self.g.get_graph().all_out_edges_of_node(n.id):
                destnode = self.g.get_graph().get_all_v().get(e)
                destx = self.my_scale(destnode.pos[0], x=True)
                desty = self.my_scale(destnode.pos[1], y=True)
                if (srcy > desty):
                    pygame.draw.line(self.screen, (200, 100, 50), (srcx + 5, srcy + 5), (destx + 5, desty + 5))

                    id_srf = self.FONT.render(str(self.g.get_graph().all_out_edges_of_node(n.id)[e]), True, Color(255, 255, 255))
                    rect = id_srf.get_rect(center=((srcx+destx)/2, (srcy+desty)/2))
                    self.screen.blit(id_srf, rect)
                else:
                    pygame.draw.line(self.screen, (200, 100, 50), (srcx - 5, srcy - 5), (destx - 5, desty - 5))


    def drawAgents(self, agents: list):
        for a in agents:
            x, y, _ = eval(a.get('pos'))
            pygame.draw.circle(self.screen, (0, 100, 0), (self.my_scale(x, x=True), self.my_scale(y, y=True)), 15)

    def drawPokes(self, dictpoke: dict):
        for curr in dictpoke:
            p = curr.get('Pokemon')
            x, y, _ = eval(p.get('pos'))
            if p.get('type') < 0:
                px, py = self.my_scale(x, x=True) - 15, self.my_scale(y, y=True) - 15
            else:
                px, py = self.my_scale(x, x=True) + 15, self.my_scale(y, y=True) + 15

            pygame.draw.circle(self.screen, (0, 100, 150), (px, py), 15)
            id_srf = self.FONT.render(str(p.get('srcID')) + " to " + str(p.get('destID')), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(px, py))
            self.screen.blit(id_srf, rect)

    def drawBackground(self):
        self.screen.fill(Color(0, 0, 0))
        borders = pygame.Rect(self.my_scale(self.min_x, x=True) - 50, self.my_scale(self.min_y, y=True) - 50,
                              self.screen.get_width() - (self.my_scale(self.min_x, x=True) - 50),
                              self.screen.get_height() - (self.my_scale(self.min_y, y=True) - 50))
        pygame.draw.rect(self.screen, (0, 200, 100), borders, 2)