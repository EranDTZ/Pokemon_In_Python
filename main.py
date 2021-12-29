import json
from types import SimpleNamespace

from src.Graph.GraphAlgo import GraphAlgo
from client_python.client import Client
import subprocess


class pokemon:
    def __init__(self, x, y, z, type, value, srcID, destID):
        self.x = x
        self.y = y
        self.z = z
        self.type = type
        self.value = value
        self.srcID = srcID
        self.destID = destID


class agent:
    def __init__(self, id, value, src, dest, speed, x, y, z):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.x = x
        self.y = y
        self.z = z



# Auto server open
subprocess.Popen(["powershell.exe", "java -jar Ex4_Server_v0.0.jar 15"])

# Host information
PORT = 6666
HOST = '127.0.0.1'

# Initiate connection
client = Client()
client.start_connection(HOST, PORT)
client.add_agent("{\"id\":2}")
client.add_agent("{\"id\":3}")
client.add_agent("{\"id\":4}")
client.add_agent("{\"id\":5}")

"""
get the map from the server and load it into GraphAlgo g
"""
jsons = client.get_graph()
with open("serverGraph.json", "w") as file:
    json.dump(eval(jsons), fp=file)
g = GraphAlgo()

g.load_from_json("serverGraph.json")
agents = json.loads(client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents
pokemons = [a.Agent for a in agents]
for a in agents:
    print()



 """
 Following function calculates the src and dest nodes of each pokemon
 """
pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
pokemons = [p.Pokemon for p in pokemons]
for p in pokemons:
    px, py, _ = eval(p.pos)
    for n in g.get_graph().get_all_v().values():
        srcx, srcy = n.pos[0], n.pos[1]
        for e in g.get_graph().all_out_edges_of_node(n.id):
            destx, desty = g.get_graph().get_all_v()[e].pos[0], g.get_graph().get_all_v()[e].pos[1]
            a = (srcy-desty)/(srcx-destx)
            b = srcy - a*srcx

            if (py == a*px+b) and (desty<srcy and p.type<0 or desty>srcy and p.type>0):
                print("Current pokemon is on current edge!")
                print("srcID:", n.id, ", DestID:", g.get_graph().get_all_v()[e].id, "| For pokemon:")
                print(p, "\n")
                # here we need to "attach" the src and dest IDs to the pokemon

