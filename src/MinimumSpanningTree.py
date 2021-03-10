#!/usr/bin/env python3


class Graph:
    def __init__(self, root, vertices):
        self.vertices = vertices
        self.root = root
        self.V = len(vertices) + 1  # add root node
        self.graph = []
        self.genEdges()

    def calcWeigth(self, source, target): # Nao tirar :)
        min_d = min(abs(source[0] - target[0]), abs(source[1] - target[1]))

        if source[0] < target[0]:
            x = source[0] + min_d
        else:
            x = source[0] - min_d

        if source[1] < target[1]:
            y = source[1] + min_d
        else:
            y = source[1] - min_d

        return min_d + abs(x - target[0]) + abs(y - target[1]) - 1

    # function to generate Edges
    def genEdges(self):
        # root is always node 0
        for i in range(len(self.vertices)):
            self.graph.append((0, i + 1, self.calcWeigth(self.root, self.vertices[i])))

        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                self.graph.append(
                    (i + 1, j + 1, self.calcWeigth(self.vertices[i], self.vertices[j]))
                )

        # sort all the edges in non-decreasing order of their weight.
        self.graph = sorted(self.graph, key=lambda item: item[2])

    # find set of an element i (uses path compression technique)
    def find(self, parent, i):
        curr = i
        while parent[curr] != curr:
            curr = parent[curr]
        return curr

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
        self.result = []

        # create V subsets with single elements
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        i = 0
        e = 0
        # while there are still edges
        while e < self.V - 1:
            # pick the smallest edge and increment the index for next iteration
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # include edge if it doesn't cause cycle, and increment the index
            # of result for next edge
            if x != y:
                e += 1
                self.result.append([u, v, w])
                self.union(parent, rank, x, y)

    def getBackboneLen(self):
        self.kruskal()

        ret = 0
        for s, t, w in self.result:
            ret += w  # current evaluation node weight

        to_visit = {0}
        visited = set()
        while len(to_visit) != 0:
            next_node = to_visit.pop()
            visited.add(next_node)
            visited_someone = False
            for s, t, w in self.result:
                if s == next_node and t not in visited:
                    visited_someone = True
                    to_visit.add(t)
                elif t == next_node and s not in visited:
                    visited_someone = True
                    to_visit.add(s)
            if visited_someone:
                ret += 1

        return ret - 1  # init backbone don't need a backbone

    def __str__(self):
        ret = ""
        for u, v, w in self.result:
            ret += "{} -- {} == {}\n".format(u, v, w)
        return ret


if __name__ == "__main__":
    g = Graph((0, 0), [(1, 0), (2, -1), (1, 1), (5, 3), (6, 8), (6, 9)])
    print(g.getBackboneLen())
    print(g)
