from queue import PriorityQueue
import constant as const


class Graph:
    adjLists = {}
    def __init__(self, node, edge, isWeighted=False):
        self.node = node
        self.edge = edge
        self.isWeighted = isWeighted
    def setAdjList(self, a, b, w=None):
        if w == None:
            self.adjLists[a].append(b)
        else:
            self.adjLists[a].append([b, w])
    def getAdjList(self):
        return self.adjLists
    def dijkstra(self, start):
        self.distance = [const.INF for i in range (self.node)]
        self.visited = [False for i in range (self.node)]
        self.distance[start] = 0
        queue = PriorityQueue()
        queue.put([0, start])
        while not queue.empty():
            u = queue.get()
            a = u[1]
            if self.visited[a]:
                continue
            self.visited[a] = True
            for x in self.adjLists[a]:
                b = x[0]
                w = 1
                if self.isWeighted:
                    w = x[1]
                if self.distance[a]+w < self.distance[b]:
                    self.distance[b] = self.distance[a] + w
                    queue.put([self.distance[b], b])




G1 = Graph(3, 4)
G1.setEdges(1, 2, 3)
G1.setEdges(2, 3, 5)
G1.setEdges(3, 5)
print(G1.getEdges())

