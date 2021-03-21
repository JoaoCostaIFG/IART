#!/usr/bin/env python3

from operator import itemgetter


class Graph:
    def __init__(self, root, vertices):
        self.root = root
        self.vertices = vertices

        self.prev_result = []
        self.result = []  # the latest result of running of the MST
        self.genEdges()

    def calcWeigth(self, source, target):
        # https://en.wikipedia.org/wiki/Chebyshev_distance
        return max(abs(source[0] - target[0]), abs(source[1] - target[1])) - 1

    # function to generate Edges
    def genEdges(self):
        self.V = len(self.vertices) + 1  # vertice number (+1 for the root node)

        # sort all the edges in non-decreasing order of their weight.
        # root is always node 0
        self.graph = sorted(
            [
                (i, j, self.calcWeigth(self[i], self[j]))
                for i in range(self.V)
                for j in range(i + 1, self.V)
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

    def kruskal(self, force=False):
        self.prev_result = self.result
        self.result = []

        if force:  # force a redraw
            self.genEdges()

        # create V subsets with single elements
        parent = [node for node in range(self.V)]
        rank = [0] * self.V

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
                self.result.append((u, v, w))
                self.union(parent, rank, x, y)

    def getInd(self, v):
        for i in range(self.V):
            if self[i] == v:
                return i
        return -1

    def __getitem__(self, key):
        if key == 0:
            return self.root
        return self.vertices[key - 1]

    def __str__(self):
        ret = ""
        for u, v, w in self.result:
            ret += "{} -- {} == {}\n".format(u, v, w)
        return ret

    #
    # FOR OUR PROBLEM
    # this will be used for an incremental tree (re)generation
    #
    def addVertex(self, v):
        # when calculating the minimum spanning tree of the tree with an extra vertex,
        # we can keep the old minimum spanning tree and add the edges for the new vertex
        self.graph = sorted(
            self.result
            + [(self.V, i, self.calcWeigth(v, self[i])) for i in range(self.V)],
            key=itemgetter(2),
        )

        self.V += 1

    def rmVertex(self, v):
        ## WARNING WIP
        v_ind = self.getInd(v)

        # save the graph entries we can keep
        # and the indices of the vertices that will need to be worked on
        to_keep = []
        to_update = set()
        for s, t, w in self.result:
            if s == v_ind:
                to_update.add(t)
            elif t == v_ind:
                to_update.add(s)
            else:
                to_keep.append((s, t, w))

        # TODO every index bigger than v_ind needs to be decreased

        self.V -= 1

        new_dists = [
            (i, ind, self.calcWeigth(self[ind], self[i]))
            for i in range(self.V)
            for ind in to_update
            if i != ind and i != v_ind
        ]

        self.graph = sorted(to_keep + new_dists, key=itemgetter(2))

    def goBack(self):
        # here we recover the previous (stable) state of the graph
        self.result = self.prev_result
        self.V -= 1

    def getBackboneLen(self, force=False):
        self.kruskal(force)

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


# around 300 random points test
if __name__ == "__main__":
    g = Graph((0, 0), [(1, 1), (5, 5), (9, 3)])
    g.kruskal()
    print(g)

    g.addVertex((2, 2))
    g.kruskal()
    print(g)
    g.vertices.append((2, 2))

    g.rmVertex((1, 1))
    g.vertices.remove((1, 1))
    g.kruskal()
    print(g)

    # Test 2
    #  g = Graph((0, 0), [(1, 1), (2, 2), (5, 5), (9, 3)])
    #  g.kruskal()
    #  print(g)

    #  g.rmVertex((1, 1))
    #  g.kruskal()
    #  print(g)
