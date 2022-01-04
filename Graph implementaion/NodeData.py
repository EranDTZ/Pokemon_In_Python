import random


class NodeData:
    def __init__(self, id: int, pos: tuple = None):
        """
        Constructor
        """
        self.tag = 0
        self.id = id
        if pos is None:
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            self.pos = (x, y)
        else:
            self.pos = eval(pos)


    def __repr__(self):
        return "Node ID:"+str(self.id)
