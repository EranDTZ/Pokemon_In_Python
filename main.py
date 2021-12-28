from src.Graph.GraphAlgo import  GraphAlgo
from client_python.client import Client

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

client = Client()
client.start_connection(HOST, PORT)



json = client.get_graph()
print(json)

g = GraphAlgo()
print(g.load_from_json(json))
g.plot_graph()
