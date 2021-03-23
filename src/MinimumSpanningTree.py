#!/usr/bin/env python3

from operator import itemgetter


class Graph:
    def __init__(self, root, vertices=[]):
        self.root = root
        self.vertices = vertices
        self.result = []  # the latest result of running of the MST
        self.prev_result = []
        self.genEdges()

    def calcWeigth(self, source, target):
        # https://en.wikipedia.org/wiki/Chebyshev_distance
        return max(abs(source[0] - target[0]), abs(source[1] - target[1])) - 1

    # function to generate Edges
    def genEdges(self):

        # sort all the edges in non-decreasing order of their weight.
        # root is always node 0
        self.graph = sorted(
            [
                (i, j, self.calcWeigth(self[i], self[j]))
                for i in range(len(self))
                for j in range(i + 1, len(self))
            ],
            key=itemgetter(2),
        )

    # find set of an element i (uses path compression technique)
    def find(self, parent, i):
        while parent[i] != i:
            i = parent[i]
        return i

    # union of two sets of x and y (uses union by rank)
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        # attach smaller rank tree under root of
        # high rank tree (Union by Rank)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            # if ranks are same, then make one as root
            # and increment its rank by one
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        self.prev_result = self.result
        self.result = []

        # create V subsets with single elements
        parent = [node for node in range(len(self))]
        rank = [0] * len(self)

        i = 0
        e = 0
        # while there are still edges
        while e < len(self) - 1:
            # pick the smallest edge and increment the index for next iteration
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # include edge if it doesn't cause cycle, and increment the index
            # of result for next edge
            if x != y:
                e += 1
                self.result.append((u, v, w))
                self.union(parent, rank, x, y)

    def getInd(self, v):
        for i in range(len(self)):
            if self[i] == v:
                return i
        return -1

    def addVertex(self, v):
        self.graph = sorted(
            self.result
            + [(len(self), i, self.calcWeigth(v, self[i])) for i in range(len(self))],
            key=itemgetter(2),
        )

        self.vertices.append(v)

    def popVertex(self):
        self.result = self.prev_result
        if len(self.vertices) > 0:
            self.vertices.pop()

    def getBackboneLen(self):
        self.kruskal()

        ret = 0
        for s, t, w in self.result:
            ret += w  # current evaluation node weight

        to_visit = {0}  # start visit on root
        visited = set()
        while len(to_visit) != 0:
            next_node = to_visit.pop()
            visited.add(next_node)
            visited_someone = False  # nodes that visit others (parents) need a backbone
            for s, t, w in self.result:
                if s == next_node and t not in visited:
                    visited_someone = True
                    to_visit.add(t)
                elif t == next_node and s not in visited:
                    visited_someone = True
                    to_visit.add(s)
            if visited_someone:
                ret += 1

        return ret - 1  # init backbone doesn't need a backbone on top

    def __len__(self):
        return len(self.vertices) + 1

    def __getitem__(self, key):
        if key == 0:
            return self.root
        return self.vertices[key - 1]

    def __str__(self):
        ret = ""
        for u, v, w in self.result:
            ret += "{} -- {} == {}\n".format(u, v, w)
        return ret


# around 300 random points test
if __name__ == "__main__":
    g = Graph((0, 0), [(1, 1), (5, 5), (9, 3)])
    g.kruskal()
    print(g)
