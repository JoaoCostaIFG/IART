#!/usr/bin/env python3

# import png

from board import Board
from node import Node
from random import randint
from math import e as neper_num


class Solver:
    def __init__(self, h, w, r):
        self.steps = 0
        self.board = Board(h, w, r)
        self.pb = self.pr = self.b = self.steps = 0

    def setPrices(self, pb, pr, b):
        self.pb = pb
        self.pr = pr
        self.b = b

    def setBackbone(self, br, bc):
        self.board.setBackbone(br, bc)

    def setBoardInfo(self, info):
        # max range at which a router can be placed and still be in budget
        cable_range = (self.b - self.pr) / self.pb
        self.board.setBoardInfo(info, cable_range)

    def genRootNode(self):
        node = Node(self.board)
        node.val = self.b
        return node

    def isBetterSol(self, neighbor, current):
        return neighbor.getValue(self.pr, self.pb, self.b) > current.getValue(
            self.pr, self.pb, self.b
        )

    def hillClimbing(self):
        current = self.genRootNode()  # initial node

        while True:
            self.steps += 1
            neighbors = current.genNeighbours()  # neighbor generator
            found_better = False
            for neighbor in neighbors:
                if self.isBetterSol(neighbor, current):
                    found_better = True
                    current = neighbor
                    current.commit()  # update info of new chosen node
                    break
                else:
                    # remove rejected nodes (they won't ever help)
                    self.board.available_pos.remove(neighbor.router)

            print("Steps:", self.steps, "Val:", current.getValue())
            if not found_better:
                return current

    def steepestDescent(self):
        current = self.genRootNode()  # initial node

        while True:
            self.steps += 1
            neighbors = current.genNeighbours()
            best_neighbor = max(
                neighbors, key=lambda node: node.getValue(self.pr, self.pb, self.b)
            )
            print("Steps:", self.steps, "Val:", current.getValue())
            if not self.isBetterSol(best_neighbor, current):
                return current
            current = best_neighbor
            current.commit()  # update info of new chosen node

    def simulatedAnnealing(self, tk=1000):
        # K is our self.steps in our implementation
        # tk cooling schedule
        Mk = 10  # number of iterations for each temperature
        current = self.genRootNode()

        # Stopping criterion que decidi arbitrariamente, TODO Mudar
        while self.steps < 5:
            m = 0
            neighbours = current.genNeighbours()
            while m < Mk:
                s = next(neighbours)  # IMP THIS CAN THROW

                sValue = s.getValue(self.pr, self.pb, self.b)
                currentValue = current.getValue(self.pr, self.pb, self.b)
                if sValue > currentValue:
                    current = s
                    current.commit()  # update info of new chosen node
                else:
                    delta = sValue - currentValue
                    Ɛ = randint(0, 1)
                    if Ɛ <= neper_num ** (-delta / tk):
                        current = s
                        current.commit()  # update info of new chosen node
                m += 1
            self.steps += 1
        return current

    def toImage(self, filename, scale=1):
        img = self.board.toImage(scale)

        # TODO
        #  img = [[ord(c) for c in row] for row in self.board]
        with open(filename, "wb+") as f:
            w = png.Writer(self.board.w * scale, self.board.h * scale, greyscale=False)
            w.write(f, img)

    def __str__(self):
        return "Router price is {}. Backbone price is {}. Max budget is {}. Steps is {}\n".format(
            self.pr, self.pb, self.b, self.steps
        ) + str(
            self.board
        )


def importSolver(filename):
    with open(filename, "r") as f:
        # read H, W and R (board size and router range)
        solver = Solver(*map(int, f.readline().split()))
        # read Pb, Pr and B (prices and budget)
        solver.setPrices(*map(int, f.readline().split()))
        # read br and bc (intial backbone coordinates)
        solver.setBackbone(*map(int, f.readline().split()))
        # read board
        solver.setBoardInfo([list(c) for c in f.read().split()])
        print("Finished importing map")
    return solver


solver = importSolver("../input/simple.in")
#  solver = importSolver("../input/charleston_road.in")
# solver.toImage("../out.png", 100)

# Create Node with new router
#  nodeHill = solver.hillClimbing()
#  print(solver)
#  print(nodeHill)
#  nodeSteep = solver.steepestDescent()
#  print(solver)
#  print(nodeSteep)
nodeAnnealing = solver.simulatedAnnealing()
print(solver)
print(nodeAnnealing)
