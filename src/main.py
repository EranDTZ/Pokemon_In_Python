import json
import time

import pygame
from pygame import *

import math
from gameGUI import gameGUI
from algo import gameAlgo
from src.Graph.GraphAlgo import GraphAlgo
from client_python.client import Client
import subprocess

# Auto server opener
subprocess.Popen(["powershell.exe", "java -jar Ex4_Server_v0.0.jar 1"])

# Host information
PORT = 6666
HOST = '127.0.0.1'

# Initiate connection
client = Client()
client.start_connection(HOST, PORT)

"""
get the map from the server and load it into GraphAlgo g
"""
jsons = client.get_graph()
with open("serverGraph.json", "w") as file:
    json.dump(eval(jsons), fp=file)
g = GraphAlgo()

g.load_from_json("serverGraph.json")

WIDTH, HEIGHT = 1020, 720
pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()


gameGUI = gameGUI(g, screen, client)
gameAlgo = gameAlgo(g, client)
print(client.get_info())

gameAlgo.center_agents()
client.start()
gameAlgo.updateclient(client)
gameGUI.updateclient(client)
print(client.time_to_end())
target = (int)(client.time_to_end())/100
i = 0


while client.is_running() == 'true':
    # check events
    if (int)(client.time_to_end()) == 0:
        client.stop_connection()
        exit(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == MOUSEBUTTONDOWN:
            if (0,60)<mouse.get_pos()<(150,80):
                print("bye")
                client.stop_connection()
                exit(0)
    clock.tick(100)

    """
    Following function calculates the src and dest nodes of each pokemon
    """
    dictpoke = eval(client.get_pokemons()).get('Pokemons')
    gameAlgo.loadPoke(dictpoke)


    """
    Loading agents into a list called agents
    """
    tempagents = eval(client.get_agents()).get('Agents')
    agents = gameAlgo.loadAgents(tempagents)

    "alocate agents"
    gameAlgo.alocate(agents, dictpoke)

    "refresh the screen"
    gameGUI.drawBackground()
    "draw graph"
    gameGUI.drawGraph()
    "draw agents"
    gameGUI.drawAgents(agents)
    "draw pokes"
    gameGUI.drawPokes(dictpoke)

    display.update()

    gameAlgo.move(agents, dictpoke, client)

print("OVER")
print(client.is_running())
