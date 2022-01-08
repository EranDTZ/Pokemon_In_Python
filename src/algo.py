import math

from src.Graph.GraphAlgo import GraphAlgo
from client_python.client import Client

class gameAlgo:
    def __init__(self, g: GraphAlgo, client: Client):
        self.g = g
        self.client = client
        self.ID = 0
        self.lastdis = 0
        self.lasttte = (int)(self.client.time_to_end())
        self.i = 0

    def center_agents(self):
        agentnum = (int)(self.client.get_info().split(",")[8].split(":")[1].split("}")[0]) # microsoft call me for work 050-3331464
# 0 is pokemons, 1 is 'is logged in', 2 is moves, 3 is grade, 4 is game level, 5 is max user level, 6 is id, 7 is graph, 8 is num of agents
        tempgraph = GraphAlgo()
        tempgraph.load_from_json("serverGraph.json")
        j=0
        for i in range(agentnum):
            center = str(tempgraph.centerPoint()[0])
            while center == '-1':
                while j not in tempgraph.get_graph().get_all_v():
                    j+=1
                center = str(j)
            self.client.add_agent("{\"id\":" + center + "}")
            tempgraph.get_graph().remove_node(tempgraph.centerPoint()[0])

    def alocate(self, agents: list, listpoke: list):
        "move agents"
        for a in agents:
            if a.get('dest')==-1:
                mindist = float('inf')
                closeddestID = -1
                closedtsrcID = -1
                for p in listpoke:
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
                    self.client.choose_next_edge('{"agent_id":' + str(a.get('id')) + ', "next_node_id":' + str(next_node) + '}')
                else:
                    next_node = closeddestID
                    self.client.choose_next_edge('{"agent_id":' + str(a.get('id')) + ', "next_node_id":' + str(next_node) + '}')


    def loadPoke(self, dictpoke: dict):
        epsilon = 0.00000001
        listpoke = []
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
            listpoke.append(p)
        sorted(listpoke, key=lambda p: p['value'])

    def loadAgents(self, tempagents: list):
        agents = []
        for curr in tempagents:
            a = curr.get('Agent')
            agents.append(a)
        return agents

    def move(self, agents, dictpoke, client):
        ss = False
        pokeflag = False
        for a in agents:
            if a.get('speed')>1: s = True
            if a.get('speed')>4: ss = True

        for a in agents:
            src = a.get('src')
            dest = a.get('dest')
            pos = a.get('pos')
            x, y, _ = eval(pos)

            if dest != -1:
                destx, desty, _ = self.g.get_graph().get_all_v().get(dest).pos
                srcx, srcy, _ = self.g.get_graph().get_all_v().get(src).pos
                weight = self.g.get_graph().all_out_edges_of_node(src).get(dest)

                for curr in dictpoke:
                    p = curr.get('Pokemon')
                    if p.get('srcID') == src:
                        destx, desty, _ = eval(p.get('pos'))
                        pokeflag = True
                currdist = math.sqrt((x - destx) ** 2 + (y - desty) ** 2)
                if pokeflag:
                    currtte = (int)(client.time_to_end())
                    epsilon = 0.001
                    if ((a.get('speed') ** 1.3) * weight * 0.00000251413213 * (self.lasttte - currtte)) > currdist - epsilon:
                        self.lasttte = currtte
                        self.client.move()
                    self.lastdis = currdist
        if not pokeflag:
            if ss:
                if self.i == 1:
                    self.client.move()
                    self.i=0
                else:
                    self.i+=1
            else:
                if self.i == 2:
                    self.client.move()
                    self.i=0
                else:
                    self.i+=1


    def updateclient(self, client: Client):
        self.client = client
        self.lasttte = (int)(client.time_to_end())
