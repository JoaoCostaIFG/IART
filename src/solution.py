#!/usr/bin/env python3

from src.MinimumSpanningTree import Graph
from src.utils import getCoordsBetween
from src.board import Board
from random import shuffle, random, randrange


class Solution:
    # pass a parent sol (if any) and a new router that will be added to the solution
    def __init__(self, board, routers=[]):
        self.board = board
        self.cutoff = 0  # number of routers included in solution
        self.val = Board.b
        self.cost = 0
        self.covered = set()
        self.routers = routers

        self.need_calc = True  # is the root => value 0
        self.need_calcBackbone = True

        self.backbones = []
        self.graph = Graph(self.board.backbone, [])

    # returns a generator for the neighborhood of this Solution
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
        # each router is allowed to move in each of these directions until an empty space if found
        #
        for i in indices:  # iterate move indices
            router_ind = i // 8
            router = self.routers[router_ind]
            move = i % 8
            delta_r = delta_c = 0
            if move == 0:  # North
                delta_r = -1
            elif move == 1:  # North-East
                delta_r = -1
                delta_c = 1
            elif move == 2:  # East
                delta_c = 1
            elif move == 3:  # South-East
                delta_r = 1
                delta_c = 1
            elif move == 4:  # South
                delta_r = 1
            elif move == 5:  # South-West
                delta_r = 1
                delta_c = -1
            elif move == 6:  # West
                delta_c = -1
            elif move == 7:  # North-West
                delta_r = -1
                delta_c = -1

            # find first empty space in that direction
            new_pos = [router[0] + delta_r, router[1] + delta_c]
            while self.board.isCellInsideBoard(new_pos) and not self.board.isEmptyCell(
                new_pos
            ):
                new_pos[0] += delta_r
                new_pos[1] += delta_c

            # only keep new pos if it isn't duplicated and is available (inside the board and empty space)
            if (
                new_pos in self.routers
                or not self.board.isCellInsideBoard(new_pos)
                or not self.board.isEmptyCell(new_pos)
            ):
                continue

            new_routers = self.routers.copy()
            new_routers[router_ind] = tuple(new_pos)
            yield Solution(self.board, new_routers)

    # reproduce two solutions (for genetic algorithm)
    # using squares
    def crossover(self, sol):
        # calculate rectangle that will separate te vertices
        rect_size = [
            randrange(self.board.h // 40, self.board.h // 5),
            randrange(self.board.w // 40, self.board.w // 5),
        ]
        rect_center = self.board.getRandomPosOnce()
        rect_corner_tl = [
            max(0, rect_center[0] - (rect_size[0] // 2)),
            max(0, rect_center[1] - (rect_size[1] // 2)),
        ]
        rect_corner_br = [
            min(self.board.h, rect_corner_tl[0] + rect_size[0]),
            min(self.board.w, rect_corner_tl[1] + rect_size[1]),
        ]

        # checks if cell is inside the square calculated above
        def insideSquare(r):
            return (
                r[0] >= rect_corner_tl[0]
                and r[0] <= rect_corner_br[0]
                and r[1] >= rect_corner_tl[1]
                and r[1] <= rect_corner_br[1]
            )

        # checks if cell is outside the square calculated above
        def outsideSquare(r):
            return (
                r[0] < rect_corner_tl[0]
                or r[0] > rect_corner_br[0]
                or r[1] < rect_corner_tl[1]
                or r[1] > rect_corner_br[1]
            )

        # randomly attribute an order to the parents
        if random() < 0.5:
            parent1, parent2 = self, sol
        else:
            parent1, parent2 = sol, self

        # solutions of both routers
        sol1 = parent1.getSol()
        sol2 = parent2.getSol()

        # list of routers inside square in parent 1 and outside square in parent 2
        new_routers = list(filter(lambda r: insideSquare(r), sol1)) + list(
            filter(lambda r: outsideSquare(r), sol2)
        )

        cromossome_len = len(parent1.routers)
        if len(new_routers) > cromossome_len:
            # pop extra routers (need to mainting the cromossome length)
            new_routers = new_routers[:cromossome_len]
        else:
            # pad the cromossome with routers from the parents in order to have all
            # the cromossomes be the same size
            i = 0
            while len(new_routers) < cromossome_len:
                r1 = parent1.routers[i]
                r2 = parent2.routers[i]
                if r1 not in new_routers:
                    new_routers.append(r1)
                # verify len again because the previous append might have changed it
                if r2 not in new_routers and len(new_routers) < cromossome_len:
                    new_routers.append(r2)
                i += 1

        return Solution(self.board, new_routers)

    # reproduce two solutions (for genetic algorithm)
    # using single point crossover
    def crossover2(self, sol):
        if random() < 0.5:
            parent1, parent2 = self, sol
        else:
            parent1, parent2 = sol, self

        # single point crossover
        point = randrange(0, len(parent1.routers))

        new_routers = parent1.routers[0:point] + parent2.routers[point:]
        return Solution(self.board, new_routers)

    # reproduce two solutions (for genetic algorithm)
    # using random interleave of parents
    def crossover3(self, sol):
        new_routers = []
        if random() < 0.5:
            parent1, parent2 = self, sol
        else:
            parent1, parent2 = sol, self

        # solutions of both routers
        sol1 = parent1.getSol()
        sol2 = parent2.getSol()

        # random order list of routers inside cutoff of both solutions
        new_routers = sol1.copy()
        for r in sol2:
            if r not in new_routers:
                new_routers.append(r)
        shuffle(new_routers)

        i = 0
        cromossome_len = len(parent1.routers)
        while len(new_routers) < cromossome_len:
            r1 = parent1.routers[parent1.cutoff + i]
            r2 = parent2.routers[parent1.cutoff + i]
            if r1 not in new_routers:
                new_routers.append(r1)
            # verify len again because the previous append might have changed it
            if r2 not in new_routers and len(new_routers) < cromossome_len:
                new_routers.append(r2)
            i += 1

        return Solution(self.board, new_routers)

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
    def getValue(self, stop_on_val=True):
        if not self.need_calc:
            return self.val

        for router in self.routers:
            self.graph.addVertex(router)
            # +1 to cutoff because of the new router
            new_cost = (
                self.graph.getBackboneLen() * Board.pb + (self.cutoff + 1) * Board.pr
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

            # IMPORTANT if the statement below is left commented, the code can
            # be optimized in other ways, e.g.: inserting an initial batch of routers
            # for the first kruskal

            # We trim the solution when we find a bad router for performance reasons
            # this also allows the algortihms to run without trying to brute-force things
            if stop_on_val and new_val < self.val:  # no more routers pls => stop
                self.graph.popVertex()
                break

            self.cutoff += 1
            self.covered.update(router_cov)
            self.cost = new_cost
            self.val = new_val

        # cost = backbones * pb + routers * pr
        # score = 1000 * target + (B - cost)
        self.val = len(self.covered) * 1000 + (Board.b - self.cost)
        self.need_calc = False

        return self.val

    # return the array of routers that is part of the solution
    def getSol(self):
        return self.routers[0 : self.cutoff]

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
            f.write(str(self.cutoff) + "\n")
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
        res = "Score: {}\nCells covered/Total cells: {}/{} ({})\nRouters placed: {}\nCost/Budget: {}/{} ({})".format(
            self.getValue(),
            len(self.covered),
            len(self.board.available_pos),
            len(self.covered) - len(self.board.available_pos),  # negative value
            self.cutoff,
            self.cost,
            Board.b,
            Board.b - self.cost,  # positive value
        )

        if draw_in_terminal:
            res += "\n\n" + self.drawInTerminal()

        return res

    def drawInTerminal(self):
        res = ""
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
