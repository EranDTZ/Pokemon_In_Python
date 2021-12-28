import json

from src.Graph.GraphAlgo import  GraphAlgo
from client_python.client import Client
import subprocess

# Auto server open
subprocess.Popen(["powershell.exe", "java -jar Ex4_Server_v0.0.jar 0"])

# Host information
PORT = 6666
HOST = '127.0.0.1'

# Initiate connection
client = Client()
client.start_connection(HOST, PORT)


jsons = client.get_graph()

with open("serverGraph.json", "w") as file:
    json.dump(eval(jsons), fp=file)

g = GraphAlgo()
g.load_from_json("serverGraph.json")

g.plot_graph()  # temp line for debugging
