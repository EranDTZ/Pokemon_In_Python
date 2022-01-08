import json
import subprocess
from unittest import TestCase

import pygame
from pygame import display, RESIZABLE, MOUSEBUTTONDOWN, mouse

from algo import gameAlgo
from client_python.client import Client
from src.Graph.GraphAlgo import GraphAlgo


class TestgameAlgo(TestCase):


    def test_loadPoke(self):
        subprocess.Popen(["powershell.exe", "java -jar Ex4_Server_v0.0.jar 13"])
        PORT = 6666
        HOST = '127.0.0.1'
        client = Client()
        client.start_connection(HOST, PORT)
        jsons = client.get_graph()
        with open("../serverGraph.json", "w") as file:
            json.dump(eval(jsons), fp=file)
        g = GraphAlgo()
        g.load_from_json("serverGraph.json")
        WIDTH, HEIGHT = 1020, 720
        pygame.init()
        screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        clock = pygame.time.Clock()
        game = gameAlgo(g,client)
        pokelist=[{'Pokemon': {'value': 5.0, 'type': -1, 'pos': '35.20392770907119,32.10833067124629,0.0', 'srcID': 33, 'destID': 32}}, {'Pokemon': {'value': 8.0, 'type': -1, 'pos': '35.20622459040522,32.101281022067994,0.0', 'srcID': 17, 'destID': 16}}]

        self.assertEquals(game.loadPoke(pokelist),None)

    def test_loadAgent(self):
        subprocess.Popen(["powershell.exe", "java -jar Ex4_Server_v0.0.jar 13"])
        PORT = 6666
        HOST = '127.0.0.1'
        client = Client()
        client.start_connection(HOST, PORT)
        jsons = client.get_graph()
        with open("../serverGraph.json", "w") as file:
            json.dump(eval(jsons), fp=file)
        g = GraphAlgo()
        g.load_from_json("serverGraph.json")
        WIDTH, HEIGHT = 1020, 720
        pygame.init()
        screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        clock = pygame.time.Clock()
        game = gameAlgo(g, client)
        agents=[{'id': 0, 'value': 0.0, 'src': 6, 'dest': 15, 'speed': 1.0,
          'pos': '35.204587448193635,32.103100622679904,0.0'},
         {'id': 1, 'value': 0.0, 'src': 1, 'dest': 2, 'speed': 1.0, 'pos': '35.19320509838321,32.10624968164074,0.0'}]

        self.assertEquals(game.loadAgents(agents), [None, None])







