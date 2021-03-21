#!/usr/bin/env python3

from src.MinimumSpanningTree import Graph
from src.utils import getCoordsBetween
from src.board import Board
from random import choice


class Node:
    # pass a parent node (if any) and a new router that will be added to the solution
    def __init__(self, board, node=None, new_router=None):
        self.board = board
        self.val = 0
        self.cost = 0
        self.covered = set()

        self.parent = node
        self.router = new_router

        if self.parent:
            self.need_calc = True
            self.need_calcBackbone = True

            self.routers = self.parent.routers
            self.backbones = self.parent.backbones
            self.covered.add(new_router)  # routers are always covered
            self.graph = self.parent.graph
        else:  # has no parent (grandparent)
            self.need_calc = False  # is the root => value 0
            self.need_calcBackbone = False

            self.routers = []
            self.backbones = []
            self.graph = Graph(self.board.backbone, self.routers)

    def genNeighbours(self):
        # ADD operator
        # prioritize positions that are outside the range of the current routers
        for pos in self.board.available_pos:
            if pos not in self.covered:
                son = Node(self.board, self, pos)
                yield son

        # remaining positions
        for pos in self.board.available_pos:
            if pos in self.covered:
                son = Node(self.board, self, pos)
                yield son

    def reproduce(self, node):
        child = Node(self.board)  # We assume that node1 and node2 are in the same board
        for i in range(0, len(self.routers), 2):  # even
            child.routers.append(self.routers[i])
        for i in range(1, len(node.routers), 2):  # odd
            child.routers.append(node.routers[i])

        child.need_calcBackbone = True
        child.getValue(True, True)

        return child

    def mutate(self):
        neighbours = self.genNeighbours()
        self = choice(list(neighbours))

    def getCost(self, force=False, redo=False):
        if not self.need_calc:
            return self.cost

        if not redo:
            self.graph.addVertex(self.router)
        # +1 because we didn't append the current router to the list
        self.cost = (
            self.graph.getBackboneLen(force) * Board.pb
            + (len(self.routers) + 1) * Board.pr
        )
        return self.cost

    def getRouterCovered(self, router):
        rowi = max(0, router[0] - self.board.r)
        coli = max(0, router[1] - self.board.r)
        rowf = min(self.board.h, router[0] + self.board.r + 1)
        colf = min(self.board.w, router[1] + self.board.r + 1)
        for row in range(rowi, rowf):
            for col in range(coli, colf):
                if self.board.board[row][col] != ".":  # check if is available pos
                    continue

                has_wall = False
                top = min(row, router[0])
                bot = max(row, router[0])
                left = min(col, router[1])
                right = max(col, router[1])
                for crow in range(top, bot + 1):
                    for ccol in range(left, right + 1):
                        if (crow, ccol) in self.board.walls:
                            has_wall = True
                            break
                if not has_wall:
                    self.covered.add((row, col))

    def getValue(self, force=False, redo=False):
        if force:
            self.need_calc = True
        if not self.need_calc:
            return self.val

        # router range
        if redo:
            for router in self.routers:
                self.getRouterCovered(router)
            cov_cnt = len(self.covered)
        else:
            self.getRouterCovered(self.router)
            cov_cnt = len(self.parent.covered.union(self.covered))

        cost = self.getCost(force, redo)

        # score is 0 if it is over budget
        # otherwise, score = 1000 * target + (B - (backbones * pb + routers * pr))
        self.val = 0 if cost > Board.b else cov_cnt * 1000 + (Board.b - cost)
        self.need_calc = False
        return self.val

    # call when it has been decided that this is the best vertex for the next step
    # e.g.: for printing or finding its neighbours
    def commit(self):
        self.routers.append(self.router)
        self.covered.update(self.parent.covered)
        # TODO maybe keep index somehow
        # TODO maybe iterating from the end makes the runtime faster
        self.board.available_pos.remove(self.router)

    # call to cleanup the side effects of evaluating this vertex
    # (when it wasn't the chosen one)
    def cleanup(self):
        self.graph.goBack()

    def calcBackbone(self):
        self.need_calcBackbone = False
        self.backbones = set()
        for (r1, r2, _) in self.graph.result:
            if r1 == 0:
                router1 = self.board.backbone
            else:
                router1 = self.routers[r1 - 1]

            if r2 == 0:
                router2 = self.board.backbone
            else:
                router2 = self.routers[r2 - 1]

            coords = tuple(getCoordsBetween(router1, router2))
            self.backbones.update(coords)

    def toFile(self, filename):
        if self.need_calcBackbone:
            self.calcBackbone()

        with open(filename, "w+") as f:
            f.write(str(len(self.backbones)) + "\n")
            for r, c in self.backbones:
                f.write(str(r) + " " + str(c) + "\n")
            f.write(str(len(self.routers)) + "\n")
            for r, c in self.routers:
                f.write(str(r) + " " + str(c) + "\n")

    # scale is how many pixels the side of one 1 board cell takes in the output image
    # returns a RGB pixel grid
    def toImage(self, scale=1):
        if self.need_calcBackbone:
            self.calcBackbone()

        img = []
        for r in range(self.board.h):
            row = ()
            for c in range(self.board.w):
                if (r, c) == self.board.backbone:  # initial backbone
                    next_pixel = (0xFF, 0x73, 0xFD)
                elif (r, c) in self.routers:  # routers
                    next_pixel = (0xB7, 0xFF, 0x73)
                elif (r, c) in self.backbones:  # backbones
                    next_pixel = (0xFF, 0x73, 0xB7)
                elif (r, c) in self.covered:  # covered
                    next_pixel = (0xFF, 0x96, 0x73)
                elif self.board.board[r][c] == ".":  # not covered
                    next_pixel = (0x75, 0x73, 0xFF)
                elif self.board.board[r][c] == "#":  # wall
                    next_pixel = (0xFF, 0xDE, 0x73)
                else:  # void
                    next_pixel = (0x17, 0x17, 0x17)
                row += next_pixel * scale
            for s in range(scale):
                img.append(row)
        return img

    def __str__(self, draw_in_terminal=False):
        res = "Value is {}. There are {} cells covered by {} routers. The budget spent was {}\n".format(
            self.getValue(), len(self.covered), len(self.routers), self.cost
        )

        if draw_in_terminal:
            if self.need_calcBackbone:
                self.calcBackbone()

            for x in range(self.board.h):  # For each row
                for y in range(self.board.w):  # For each cell
                    if (x, y) == self.board.backbone:
                        res += "B"
                    elif (x, y) in self.routers:
                        res += "R"
                    elif (x, y) in self.backbones:
                        res += "b"
                    elif (x, y) in self.covered:
                        res += ":"
                    else:
                        res += self.board.board[x][y]
                res += "\n"

        return res
