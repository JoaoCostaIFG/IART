#!/usr/bin/env python3

from src.MinimumSpanningTree import Graph
from src.utils import getCoordsBetween
from src.board import Board
from random import shuffle


class Solution:
    # pass a parent sol (if any) and a new router that will be added to the solution
    def __init__(self, board, routers=[]):
        self.board = board
        self.cutof = 0  # number of routers included in solution
        self.val = Board.b
        self.cost = 0
        self.covered = set()
        self.routers = routers

        self.need_calc = True  # is the root => value 0
        self.need_calcBackbone = True

        self.backbones = []
        self.graph = Graph(self.board.backbone, [])

    def mutate(self):
        indices = [i for i in range(len(self.routers) * 8)]
        shuffle(indices)

        # Directions
        #
        #    7  0  1
        #     \ | /
        # 6 -- o  -- 2
        #    / | \
        #   5  4  3
        #
        for i in indices:  # iterate move indices
            router_ind = i // 8
            router = self.routers[router_ind]
            move = i % 8
            delta_r = delta_c = 0
            if move == 0:
                delta_r = -1
            elif move == 1:
                delta_r = -1
                delta_c = 1
            elif move == 2:
                delta_c = 1
            elif move == 3:
                delta_r = 1
                delta_c = 1
            elif move == 4:
                delta_r = 1
            elif move == 5:
                delta_r = 1
                delta_c = -1
            elif move == 6:
                delta_c = -1
            elif move == 7:
                delta_r = -1
                delta_c = -1

            new_pos = (router[0] + delta_r, router[1] + delta_c)
            # only keep new pos if it isn't duplicated and is available
            if new_pos in self.routers or self.board.getCell(new_pos) == "#":
                continue

            new_routers = self.routers.copy()
            new_routers[router_ind] = new_pos
            yield Solution(self.board, new_routers)

    # reproduce two solutions (for genetic algorithm)
    def crossover(self, sol):
        child = Solution(
            self.board
        )  # We assume that sol1 and sol2 are in the same board
        for i in range(0, len(self.routers), 2):  # even
            child.routers.append(self.routers[i])
        for i in range(1, len(sol.routers), 2):  # odd
            child.routers.append(sol.routers[i])

        child.need_calcBackbone = True
        child.getValue(True, True)

        return child

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

    # calculates the value of a solution
    # If cost is higher than the budget, B, the value of the solution is 0.
    # Otherwise, the value of a sol follows the formula C * 1000 + (B - Cost),
    # where C is the numbered of cells covered by at least one router.
    def getValue(self):
        if not self.need_calc:
            return self.val

        for router in self.routers:
            self.graph.addVertex(router)
            # +1 to cutof because of the new router
            new_cost = (
                self.graph.getBackboneLen() * Board.pb + (self.cutof + 1) * Board.pr
            )
            if new_cost > Board.b:  # no budget for this => stop
                self.graph.popVertex()
                break
            # calculate the new value using the coverage of the router
            # only counting the new covered spaces
            router_cov = self.board.getRouterCovered(router) - self.covered
            new_val = (len(self.covered) + len(router_cov)) * 1000 + (
                Board.b - new_cost
            )

            # TODO if statement below is left commented, the code can be optimized
            if new_val < self.val:  # no more routers pls => stop
                self.graph.popVertex()
                break

            self.cutof += 1
            self.covered.update(router_cov)
            self.cost = new_cost
            self.val = new_val

        # cost = backbones * pb + routers * pr
        # score = 1000 * target + (B - cost)
        self.val = len(self.covered) * 1000 + (Board.b - self.cost)
        self.need_calc = False

        return self.val

    def getSol(self):
        return self.routers[0 : self.cutof]

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

    # delta value
    def __sub__(self, other):
        return self.getValue() - other.getValue()

    # compares the value of 2 solutions
    def __gt__(self, other):
        return self.getValue() > other.getValue()

    def __le__(self, other):
        return not self.getValue() > other.getValue()

    def __lt__(self, other):
        return self.getValue() < other.getValue()

    def __ge__(self, other):
        return not self.getValue() < other.getValue()

    def __eq__(self, other):
        return self.getValue() == other.getValue()

    def __ne__(self, other):
        return not self.getValue() == other.getValue()

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
            f.write(str(self.cutof) + "\n")
            for r, c in self.getSol():
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
                elif (r, c) in self.getSol():  # routers
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
        res = "Score: {}\nCells covered/Total cells: {}/{}\nRouters placed:{}\nCost: {}".format(
            self.getValue(),
            len(self.covered),
            len(self.board.available_pos),
            self.cutof,
            self.cost,
        )

        if draw_in_terminal:
            res += "\n"
            if self.need_calcBackbone:
                self.calcBackbone()

            for x in range(self.board.h):  # For each row
                for y in range(self.board.w):  # For each cell
                    if (x, y) == self.board.backbone:
                        res += "B"
                    elif (x, y) in self.getSol():
                        res += "R"
                    elif (x, y) in self.backbones:
                        res += "b"
                    elif (x, y) in self.covered:
                        res += ":"
                    else:
                        res += self.board.board[x][y]
                res += "\n"

        return res
