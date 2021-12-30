import json
import pygame
from pygame import *

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
client.add_agent("{\"id\":0}")


"""
get the map from the server and load it into GraphAlgo g
"""
jsons = client.get_graph()
with open("serverGraph.json", "w") as file:
    json.dump(eval(jsons), fp=file)
g = GraphAlgo()

g.load_from_json("serverGraph.json")

WIDTH, HEIGHT = 1080, 720
pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)


min_x = min(list(g.get_graph().get_all_v().values()), key=lambda n: n.pos[0]).pos[0]
min_y = min(list(g.get_graph().get_all_v().values()), key=lambda n: n.pos[1]).pos[1]
max_x = max(list(g.get_graph().get_all_v().values()), key=lambda n: n.pos[0]).pos[0]
max_y = max(list(g.get_graph().get_all_v().values()), key=lambda n: n.pos[1]).pos[1]


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 200, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 150, screen.get_height()-50, min_y, max_y)


epsilon = 0.00000001
client.start()
while client.is_running() == 'true':

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))
    borders = pygame.Rect(my_scale(min_x, x=True)-50, my_scale(min_y, y=True)-50, screen.get_width()-(my_scale(min_x, x=True)-50), screen.get_height()-(my_scale(min_y, y=True)-50))
    # my_scale(min_x, x=True), my_scale(min_y, y=True), my_scale(max_x, x=True), my_scale(max_y, y=True)
    pygame.draw.rect(screen, (0, 200, 100), borders, 2)

    """
    Following function calculates the src and dest nodes of each pokemon
    """
    dictpoke = eval(client.get_pokemons()).get('Pokemons')
    for curr in dictpoke:
        p = curr.get('Pokemon')
        px, py, _ = eval(p.get('pos'))
        mindist = float('inf')
        minsrcID = -1
        mindestID = -1
        for n in g.get_graph().get_all_v().values():
            srcx, srcy = n.pos[0], n.pos[1]
            srcid = n.id
            for e in g.get_graph().all_out_edges_of_node(n.id):
                destx, desty = g.get_graph().get_all_v()[e].pos[0], g.get_graph().get_all_v()[e].pos[1]
                destid = e
                a = (srcy-desty)/(srcx-destx)
                b = desty - a*destx
                #if 1==1: py = a*px + b ---> px = (py-b)\a
                #if (destid > srcid and p.get('type') > 0 or destid < srcid and p.get('type') < 0):
                if (px + epsilon > (py-b)/a > px - epsilon) and (py+epsilon > a * px + b > py-epsilon) and (destid > srcid and p.get('type') > 0 or destid < srcid and p.get('type') < 0):
                #if (srcx > px > destx or destx > px > srcx):
                    if mindist > a*px+b-py:
                        mindist = abs(a*px+b-py)
                        minsrcID = n.id
                        mindestID = g.get_graph().get_all_v()[e].id

        p['srcID'] = minsrcID
        p['destID'] = mindestID
    """
    Loading agents into a list called agents
    """
    tempagents = eval(client.get_agents()).get('Agents')
    agents = []
    for curr in tempagents:
        a = curr.get('Agent')
        agents.append(a)

    "move agents"
    for a in agents:
        if a.get('dest')==-1:
            if g.get_graph().v_size() != 0: next_node = (a.get('src')-1)%g.get_graph().v_size()
            client.choose_next_edge('{"agent_id":'+str(a.get('id'))+', "next_node_id":'+str(next_node)+'}')


    "draw nodes"
    for n in g.get_graph().get_all_v().values():
        srcx = my_scale(n.pos[0], x=True)
        srcy = my_scale(n.pos[1], y=True)
        pygame.draw.circle(screen, (100, 0, 0), (srcx, srcy), 20)
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(srcx, srcy))
        screen.blit(id_srf, rect)
        "draw edges"
        for e in g.get_graph().all_out_edges_of_node(n.id):

            destnode = g.get_graph().get_all_v().get(e)
            destx = my_scale(destnode.pos[0], x=True)
            desty = my_scale(destnode.pos[1], y=True)
            if (srcy > desty):
                pygame.draw.line(screen, (200,100,50), (srcx+5, srcy+5), (destx+5, desty+5))
            else:
                pygame.draw.line(screen, (200, 100, 50), (srcx-5, srcy-5), (destx-5, desty-5))

    "draw agents"
    for a in agents:
        x, y, _ = eval(a.get('pos'))
        pygame.draw.circle(screen, (0, 100, 0), (my_scale(x, x=True), my_scale(y, y=True)), 15)
    "draw pokes"
    for curr in dictpoke:
        p = curr.get('Pokemon')
        x, y, _ = eval(p.get('pos'))
        if p.get('type')<0:
            px, py = my_scale(x, x=True)-15, my_scale(y, y=True)-15
        else:
            px, py = my_scale(x, x=True)+15, my_scale(y, y=True)+15

        pygame.draw.circle(screen, (0, 100, 150), (px, py), 15)
        id_srf = FONT.render(str(p.get('srcID'))+" to "+str(p.get('destID')), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(px, py))
        screen.blit(id_srf, rect)
    print(agents)
    #clock.tick(60)
    display.update()
    client.move()
