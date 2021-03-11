#!/usr/bin/env python3

from MinimumSpanningTree import Graph


class Node:
    def __init__(self, board, node=None, new_router=None):
        self.board = board
        self.need_calc = True
        self.val = 0
        self.covered = set()

        self.parent = node
        self.router = new_router

        if self.parent:
            self.routers = self.parent.routers
            self.backbones = self.parent.backbones
        else:
            self.need_calc = False  # is the root => value 0
            self.routers = []
            self.backbones = []

    def addRouter(self, router):
        self.routers.append(router)

    def addBackBone(self, backbone):
        self.backbones.append(backbone)

    def genNeighbours(self):
        # Get random router to add to son
        available_pos = self.board.available_pos

        # TODO remove not in routers by removing router from possible coords on selection
        for pos in available_pos:
            son = Node(self.board, self, pos)
            yield son

    def getCost(self, pr, pb):
        # need pop to avoid side effects
        self.routers.append(self.router)
        graph = Graph(self.board.backbone, self.routers)
        self.routers.pop()

        return graph.getBackboneLen() * pb + (len(self.parent.routers) + 1) * pr

    # TODO vaue will need to use set union
    def getValue(self, pr=0, pb=0, b=0):
        if not self.need_calc:
            return self.val

        #  self.covered = set()

        # router range
        # TODO circle
        rowi = max(0, self.router[0] - self.board.r)
        coli = max(0, self.router[1] - self.board.r)
        rowf = min(self.board.h, self.router[0] + self.board.r + 1)
        colf = min(self.board.w, self.router[1] + self.board.r + 1)
        for row in range(rowi, rowf):
            for col in range(coli, colf):
                if self.board.board[row][col] != ".":  # check if is available pos
                    continue
                # check if is inside range
                if (
                    abs(self.router[0] - row) > self.board.r
                    or abs(self.router[1] - col) > self.board.r
                ):
                    continue

                has_wall = False
                for wall in self.board.walls:
                    # TODO maybe filter walls by range too
                    if (
                        min(row, self.router[0]) <= wall[0]
                        and wall[0] <= max(row, self.router[0])
                        and min(col, self.router[1]) <= wall[1]
                        and wall[1] <= max(col, self.router[1])
                    ):
                        has_wall = True
                        break
                if not has_wall:
                    self.covered.add((row, col))

        self.need_calc = False
        cost = self.getCost(pr, pb)
        if cost > b:
            self.val = 0
        else:
            # score = 1000 * target + (B - (backbones * pb + routers * pr))
            self.val = (len(self.parent.covered) + len(self.covered)) * 1000 + (
                b - cost
            )

        return self.val

    def commit(self):
        self.routers.append(self.router)
        self.covered = self.parent.covered.union(self.covered)
        # TODO maybe keep index somehow
        # TODO maybe iterating from the end makes the runtime faster
        self.board.available_pos.remove(self.router)

    def __str__(self):
        res = "Value is {}\n".format(self.val)

        for x in range(self.board.h):  # For each row
            for y in range(self.board.w):  # For each cell
                if (x, y) == self.board.backbone:
                    res += "B"
                elif (x, y) in self.routers:
                    res += "R"
                elif (x, y) in self.covered:
                    res += ":"
                elif (x, y) in self.backbones:
                    res += "b"
                else:
                    res += self.board.board[x][y]
            res += "\n"

        return res
