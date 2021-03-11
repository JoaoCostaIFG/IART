#!/usr/bin/env python3

from operator import itemgetter


class Graph:
    def __init__(self, root, vertices):
        self.vertices = vertices
        self.root = root
        self.V = len(vertices) + 1  # add root node
        self.genEdges()

    def calcWeigth(self, source, target):
        # OLD VERSION
        #  min_d = min(abs(source[0] - target[0]), abs(source[1] - target[1]))
        #  if source[0] < target[0]:
        #  x = source[0] + min_d
        #  else:
        #  x = source[0] - min_d
        #  if source[1] < target[1]:
        #  y = source[1] + min_d
        #  else:
        #  y = source[1] - min_d
        #  return min_d + abs(x - target[0]) + abs(y - target[1]) - 1
        # NEW VERSION
        # https://en.wikipedia.org/wiki/Chebyshev_distance
        return max(abs(source[0] - target[0]), abs(source[1] - target[1])) - 1

    # function to generate Edges
    def genEdges(self):
        # sort all the edges in non-decreasing order of their weight.
        # root is always node 0
        self.graph = sorted(
            [
                (0, i + 1, self.calcWeigth(self.root, self.vertices[i]))
                for i in range(len(self.vertices))
            ]
            + [
                (i + 1, j + 1, self.calcWeigth(self.vertices[i], self.vertices[j]))
                for i in range(len(self.vertices))
                for j in range(i + 1, len(self.vertices))
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
        self.result = []

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


# around 300 random points test
if __name__ == "__main__":
    g = Graph(
        (0, 0),
        [
            (1, 0),
            (2, -1),
            (1, 1),
            (5, 3),
            (6, 8),
            (6, 9),
            (34, 67),
            (45, 83),
            (46, 68),
            (45, 84),
            (33, 90),
            (46, 55),
            (76, 0),
            (72, 8),
            (21, 77),
            (0, 25),
            (50, 5),
            (82, 72),
            (18, 31),
            (88, 84),
            (53, 93),
            (8, 60),
            (56, 27),
            (57, 73),
            (25, 7),
            (80, 44),
            (42, 33),
            (50, 57),
            (97, 3),
            (83, 44),
            (64, 71),
            (37, 73),
            (42, 28),
            (31, 25),
            (89, 87),
            (29, 59),
            (61, 46),
            (79, 27),
            (26, 37),
            (87, 51),
            (53, 57),
            (25, 69),
            (95, 92),
            (17, 88),
            (91, 26),
            (58, 57),
            (91, 39),
            (53, 8),
            (40, 90),
            (22, 4),
            (74, 24),
            (63, 19),
            (10, 24),
            (85, 45),
            (6, 7),
            (23, 67),
            (16, 95),
            (30, 43),
            (60, 30),
            (86, 90),
            (61, 96),
            (14, 89),
            (90, 41),
            (47, 67),
            (24, 87),
            (54, 15),
            (56, 43),
            (41, 22),
            (57, 8),
            (78, 9),
            (51, 2),
            (81, 48),
            (72, 3),
            (1, 57),
            (55, 59),
            (76, 74),
            (97, 5),
            (57, 22),
            (49, 53),
            (61, 85),
            (62, 7),
            (31, 26),
            (94, 94),
            (87, 9),
            (65, 58),
            (10, 34),
            (29, 90),
            (57, 41),
            (24, 77),
            (98, 1),
            (57, 10),
            (7, 94),
            (70, 86),
            (5, 40),
            (26, 68),
            (50, 85),
            (43, 96),
            (31, 92),
            (14, 35),
            (41, 96),
            (5, 12),
            (82, 61),
            (58, 20),
            (29, 99),
            (84, 50),
            (52, 15),
            (59, 44),
            (40, 1),
            (91, 5),
            (28, 90),
            (11, 95),
            (49, 2),
            (91, 27),
            (40, 20),
            (24, 2),
            (66, 40),
            (86, 35),
            (25, 33),
            (36, 48),
            (33, 39),
            (9, 17),
            (59, 9),
            (49, 0),
            (8, 76),
            (69, 18),
            (36, 78),
            (63, 84),
            (15, 66),
            (48, 96),
            (93, 66),
            (6, 90),
            (11, 16),
            (16, 75),
            (59, 28),
            (85, 20),
            (21, 57),
            (36, 3),
            (64, 84),
            (82, 60),
            (8, 1),
            (18, 11),
            (98, 79),
            (98, 27),
            (78, 94),
            (61, 22),
            (23, 57),
            (24, 96),
            (35, 42),
            (59, 73),
            (37, 65),
            (58, 3),
            (54, 7),
            (62, 26),
            (27, 77),
            (62, 53),
            (35, 10),
            (16, 25),
            (40, 54),
            (98, 33),
            (91, 38),
            (69, 39),
            (60, 31),
            (6, 93),
            (85, 23),
            (31, 54),
            (43, 29),
            (17, 85),
            (4, 40),
            (91, 89),
            (17, 11),
            (23, 16),
            (15, 97),
            (88, 64),
            (23, 64),
            (78, 5),
            (79, 23),
            (67, 23),
            (54, 27),
            (8, 51),
            (32, 2),
            (66, 84),
            (25, 96),
            (39, 38),
            (56, 25),
            (44, 10),
            (0, 79),
            (43, 69),
            (8, 46),
            (5, 95),
            (20, 39),
            (81, 2),
            (54, 32),
            (39, 44),
            (81, 37),
            (80, 60),
            (2, 53),
            (26, 35),
            (57, 22),
            (78, 84),
            (86, 39),
            (14, 48),
            (36, 78),
            (71, 83),
            (96, 53),
            (63, 36),
            (33, 30),
            (21, 9),
            (8, 66),
            (20, 47),
            (26, 56),
            (64, 2),
            (41, 52),
            (36, 23),
            (98, 39),
            (62, 81),
            (34, 36),
            (6, 19),
            (57, 85),
            (87, 12),
            (8, 9),
            (5, 43),
            (56, 1),
            (2, 30),
            (18, 2),
            (3, 29),
            (95, 57),
            (20, 25),
            (60, 67),
            (71, 24),
            (17, 81),
            (97, 7),
            (48, 64),
            (18, 49),
            (38, 47),
            (25, 7),
            (28, 91),
            (53, 93),
            (29, 53),
            (75, 62),
            (35, 11),
            (90, 38),
            (78, 44),
            (68, 12),
            (41, 53),
            (59, 18),
            (1, 1),
            (21, 55),
            (69, 59),
            (34, 76),
            (48, 6),
            (34, 0),
            (71, 58),
            (17, 60),
            (71, 78),
            (31, 18),
            (99, 33),
            (7, 58),
            (72, 13),
            (10, 14),
            (77, 35),
            (46, 93),
            (82, 8),
            (83, 24),
            (20, 4),
            (60, 38),
            (17, 34),
            (4, 50),
            (99, 53),
            (99, 51),
            (75, 45),
            (23, 90),
            (52, 28),
            (86, 98),
            (75, 72),
            (85, 33),
            (88, 97),
            (2, 94),
            (10, 93),
            (26, 54),
            (28, 3),
            (26, 61),
            (13, 23),
            (5, 93),
            (75, 14),
            (69, 69),
            (60, 71),
            (44, 88),
            (74, 66),
            (19, 91),
            (36, 87),
            (55, 92),
            (67, 72),
            (0, 51),
            (91, 75),
            (34, 7),
            (86, 64),
            (50, 30),
            (50, 55),
            (22, 3),
            (84, 81),
            (3, 4),
            (90, 45),
            (67, 73),
            (80, 12),
            (35, 1),
            (44, 42),
            (50, 31),
        ],
    )
    print(g.getBackboneLen())
    print(g)
