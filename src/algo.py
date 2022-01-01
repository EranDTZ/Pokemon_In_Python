import time

from src.Graph.GraphAlgo import GraphAlgo
from client_python.client import Client
import time

class gameAlgo:
    def __init__(self, g: GraphAlgo, client: Client):
        self.g = g
        self.client = client

    def alocate(self, agents: list, dictpoke):
        "move agents"
        for a in agents:
            if a.get('dest')==-1:
                mindist = float('inf')
                closeddestID = -1
                closedtsrcID = -1
                for p in dictpoke:
                    srcID = p.get('Pokemon').get('srcID')
                    destID = p.get('Pokemon').get('destID')
                    agentPOS = a.get('src')


                    currdist = self.g.shortest_path(agentPOS, srcID)[0]
                    if currdist < mindist:
                        mindist = currdist
                        closedtsrcID = srcID
                        closeddestID = destID

                if agentPOS != closedtsrcID:
                    next_node = self.g.shortest_path(agentPOS, closedtsrcID)[1][1]
                    self.client.choose_next_edge(
                        '{"agent_id":' + str(a.get('id')) + ', "next_node_id":' + str(next_node) + '}')
                else:
                    next_node = closeddestID
                    self.client.choose_next_edge(
                        '{"agent_id":' + str(a.get('id')) + ', "next_node_id":' + str(next_node) + '}')

                # next_node = (a.get('src')+1)%self.g.get_graph().v_size()
                # self.client.choose_next_edge('{"agent_id":'+str(a.get('id'))+', "next_node_id":'+str(next_node)+'}')

    def loadPoke(self, dictpoke: dict):
        epsilon = 0.00000001
        #dictpoke = eval(self.client.get_pokemons()).get('Pokemons')
        for curr in dictpoke:
            p = curr.get('Pokemon')
            px, py, _ = eval(p.get('pos'))
            mindist = float('inf')
            minsrcID = -1
            mindestID = -1
            for n in self.g.get_graph().get_all_v().values():
                srcx, srcy = n.pos[0], n.pos[1]
                srcid = n.id
                for e in self.g.get_graph().all_out_edges_of_node(n.id):
                    destx, desty = self.g.get_graph().get_all_v()[e].pos[0], self.g.get_graph().get_all_v()[e].pos[1]
                    destid = e
                    a = (srcy - desty) / (srcx - destx)
                    b = desty - a * destx
                    if (px + epsilon > (py - b) / a > px - epsilon) and (py + epsilon > a * px + b > py - epsilon) and (
                            destid > srcid and p.get('type') > 0 or destid < srcid and p.get('type') < 0):
                        if mindist > a * px + b - py:
                            mindist = abs(a * px + b - py)
                            minsrcID = n.id
                            mindestID = self.g.get_graph().get_all_v()[e].id

            p['srcID'] = minsrcID
            p['destID'] = mindestID

    def loadAgents(self, tempagents: list):
        agents = []
        for curr in tempagents:
            a = curr.get('Agent')
            agents.append(a)
        return agents