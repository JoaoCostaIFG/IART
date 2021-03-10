#!/usr/bin/env python3

# import png

from board import Board
from node import Node


class Solver:
    def __init__(self, h, w, r):
        self.board = Board(h, w, r)
        self.pb = self.pr = self.b = 0

    def setPrices(self, pb, pr, b):
        self.pb = pb
        self.pr = pr
        self.b = b

    def setBackbone(self, br, bc):
        self.board.setBackbone(br, bc)

    def genNode(self, routers=[], backbones=[]):
        return Node(self.board, routers, backbones)

    def hillClimbing(self):
        current = self.genNode()  # initial node

        while True:
            neighbors = current.genNeighbours()
            found_better = False
            for neighbor in neighbors:
                if (len(neighbor.routers) * self.pr <= self.b and
                        neighbor.getValue() > current.getValue()):  # (ಠ¿ಠ)
                    found_better = True
                    current = neighbor
                    break

            if not found_better:
                return current
            else:
                print("son covered =", current.getValue())
                print(current.covered, end="\n")

    def steepestDescent(self):
        current = self.genNode() # initial node

        while True:
            neighbors = current.genNeighbours()
            best_neighbor = max(neighbors)
            if not (len(best_neighbor.routers) * self.pr <= self.b and
                    best_neighbor.getValue() > current.getValue()):  # (ಠ¿ಠ)
                return current
            current = best_neighbor

    def toImage(self, filename, scale=1):
        img = self.board.toImage(scale)

        # TODO
        #  img = [[ord(c) for c in row] for row in self.board]
        with open(filename, "wb+") as f:
            w = png.Writer(self.board.w * scale,
                           self.board.h * scale, greyscale=False)
            w.write(f, img)

    def __str__(self):
        return "Router price is {}. Backbone price is {}. Max budget is {}\n".format(
            self.pr, self.pb, self.b
        ) + str(self.board)


def importSolver(filename):
    with open(filename, "r") as f:
        # read H, W and R (board size and router range)
        solver = Solver(*map(int, f.readline().split()))
        # read Pb, Pr and B (prices and budget)
        solver.setPrices(*map(int, f.readline().split()))
        # read br and bc (intial backbone coordinates)
        solver.setBackbone(*map(int, f.readline().split()))
        # read board
        solver.board.setBoard([list(c) for c in f.read().split()])
    return solver


solver = importSolver("../input/simple.in")
print(solver)
# solver.toImage("../out.png", 100)

# Create Node with new router
solver.hillClimbing()
