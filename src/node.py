#!/usr/bin/env python3

from src.MinimumSpanningTree import Graph
from src.utils import getCoordsBetween
from src.board import Board
from random import randint


class Node:
    # pass a parent node (if any) and a new router that will be added to the solution
    def __init__(self, board, routers=[]):
        self.board = board
        self.cutof = 0  # number of routers included in solution
        self.val = 0
        self.cost = 0
        self.covered = set()
        self.routers = routers

        self.need_calc = True  # is the root => value 0
        self.need_calcBackbone = True

        self.backbones = []
        self.graph = Graph(self.board.backbone, [])

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

    # reproduce two solutions (for genetic algorithm)
    def reproduce(self, node):
        child = Node(self.board)  # We assume that node1 and node2 are in the same board
        for i in range(0, len(self.routers), 2):  # even
            child.routers.append(self.routers[i])
        for i in range(1, len(node.routers), 2):  # odd
            child.routers.append(node.routers[i])

        child.need_calcBackbone = True
        child.getValue(True, True)

        return child

    # generate a new mutation (for genetic algorithm)
    def mutate(self):
        #  indices = [i in for i in range(len(self.routers))]
        #  shuffle(indices)

        for pos in self.board.getRandomPos():
            i = randint(0, len(self.routers) - 1)
            new_routers = self.routers.copy()
            new_routers[i] = pos

            yield Node(self.board, new_routers)

    # get the cost of a solution
    # the cost is given by (R * Pr + Bb * Pb), where:
    # - R is the number of placed routers,
    # - Pr is the price of a router,
    # - Bb is the numbers of placed backbones (besides the initial one),
    # - Pb is the price of each backbone.
    def getCost(self):
        #  if self.need_calc:
        #  self.cost = (
        #  self.graph.getBackboneLen() * Board.pb + len(self.routers) * Board.pr
        #  )
        return self.cost

    # calculates and saves the cells covered by the given router
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

    # calculates the value of a solution
    # If cost is higher than the budget, B, the value of the solution is 0.
    # Otherwise, the value of a node follows the formula C * 1000 + (B - Cost),
    # where C is the numbered of cells covered by at least one router.
    def getValue(self):
        if not self.need_calc:
            return self.val

        # TODO router list

        for router in self.routers:
            self.graph.addVertex(router)
            new_cost = self.graph.getBackboneLen() * Board.pb + self.cutof * Board.pr
            if new_cost > Board.b:  # no more routers pls
                break

            self.getRouterCovered(router)
            self.cutof += 1
            self.cost = new_cost

        # cost = backbones * pb + routers * pr
        # score = 1000 * target + (B - cost)
        self.val = len(self.covered) * 1000 + (Board.b - self.cost)
        self.need_calc = False

        print(self.val, self.cutof, router[0:self.cutof])
        return self.val

    # calculates the positions of the backbones based on the minimum spanning tree
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

    # compares the value of 2 solutions
    def __gt__(self, other):
        return self.getValue() > other.getValue()

    # outputs the solution to a file according to the specification
    # - First line: The number of cells connected the backbone
    # - N next lines: the coordinates of these cells
    # - Next line: number of routers to be placed
    # - M next lines: the coordinates of these routers
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

    # if the argument 'draw_in_terminal' is True, the solution is drawn in the terminal
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
