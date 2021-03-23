#!/usr/bin/env python3

import src.png as png
from src.board import Board
from src.node import Node
from math import exp, floor
from random import random, choices, randint


class Solver:
    def __init__(self, h, w, r):
        self.steps = 0
        self.board = Board(h, w, r)
        self.steps = 0

    def setPrices(self, pb, pr, b):
        Board.pb = pb
        Board.pr = pr
        Board.b = b

    def setBackbone(self, br, bc):
        self.board.setBackbone(br, bc)

    def setBoardInfo(self, info):
        # max range at which a router can be placed and still be in budget
        cable_range = (Board.b - Board.pr) / Board.pb
        self.board.setBoardInfo(info, cable_range)

    def genRootNode(self):
        numRouters = floor(Board.b / Board.pr)
        pseudoSol = []

        for pos in self.board.getRandomPos():
            if len(pseudoSol) >= numRouters:
                break
            pseudoSol.append(pos)

        return Node(self.board, pseudoSol)

    def hillClimbing(self, max_iter=200):
        current = self.genRootNode()  # initial node

        while self.steps <= max_iter:
            self.steps += 1
            found_better = False

            for neighbor in current.mutate():
                if neighbor > current:
                    found_better = True
                    current = neighbor
                    break

            if not found_better:
                return current

            print(
                "Step:",
                self.steps,
                "Budget:",
                Board.b - current.getCost(),
                "Val:",
                current.getValue(),
            )

        return current

    def steepestDescentMax(self, node):
        neighbors = node.mutate()
        best_neighbor = next(neighbors)  # TODO this can throw

        for neighbor in neighbors:
            if neighbor > best_neighbor:
                best_neighbor = neighbor

        return best_neighbor

    def steepestDescent(self, max_iter=50):
        current = self.genRootNode()  # initial node

        while self.steps <= max_iter:
            self.steps += 1
            best_neighbor = self.steepestDescentMax(current)
            if best_neighbor <= current:
                return current
            current = best_neighbor

            print(
                "Step:",
                self.steps,
                "Budget:",
                Board.b - current.getCost(),
                "Val:",
                current.getValue(),
            )

        return current

    # returns the current temperature of the system based on the
    # initial temperature the fraction of the iterations performed
    def schedule(self, t):
        return float(t) * 0.9

    def simulatedAnnealing(self, init_temp=100000.0, mk=100):
        # K is our self.steps in our implementation
        t = init_temp
        current = self.genRootNode()

        while abs(t) >= 0.0001:
            self.steps += 1
            neighbors = current.mutate()
            for m in range(mk):
                neighbor = next(neighbors)
                # we choose when they are equal because delta == 0 => e = 1.0
                if neighbor >= current:
                    current = neighbor
                    neighbors = current.mutate()
                else:
                    # delta needs to be negative because we're maximizing
                    delta = neighbor - current
                    e = exp(delta / t)  # P function
                    if random() <= e:
                        current = neighbor
                        neighbors = current.mutate()
            # cool down
            t = self.schedule(t)

            print(
                "Step:",
                self.steps,
                "Budget:",
                Board.b - current.getCost(),
                "Val:",
                current.getValue(),
            )

        return current

    def generatePopulation(self, nPop):
        maxBudgetRouters = floor(Board.b / Board.pr)
        maxRouters = min(len(self.board.available_pos), maxBudgetRouters)

        res = []
        for i in range(nPop):
            node = Node(self.board)
            NRouters = randint(0, maxRouters)
            gennedRouters = choices(self.board.available_pos, k=NRouters)
            node.routers = gennedRouters
            node.graph.vertices = gennedRouters  # IMP routers and vertices are the same
            node.need_calcBackbone = True
            node.getValue(True, True)
            # yield node
            res.append(node)

        return res

    def geneticAlgorithm(self, nPop=10, it=10, mutateProb=0.2):
        population = self.generatePopulation(nPop)
        weights = [node.getValue() for node in population]

        for i in range(it):  # TODO Maybe change to time constraint?
            new_population = []
            new_weights = []
            for j in range(len(population)):
                node1 = choices(population, weights=weights).pop()
                node2 = choices(population, weights=weights).pop()
                child = node1.reproduce(node2)
                if random() < mutateProb:
                    child.mutate()
                new_population.append(child)
                new_weights.append(child.getValue())
            population = new_population
            weights = new_weights

        return max(population, key=lambda node: node.getValue())

    # scale is how many pixels the side of one 1 board cell takes in the output image
    # if a node is given, the solution represented by that node will be drawn
    # outputs the result to a file in the given path
    def toImage(self, filename, scale=1, node=None):
        if node:
            img = node.toImage(scale)
        else:
            img = self.board.toImage(scale)

        with open(filename, "wb+") as f:
            w = png.Writer(self.board.w * scale, self.board.h * scale, greyscale=False)
            w.write(f, img)

    def __str__(self):
        return "Router price: {}\nBackbone price: {}\nMax budget: {}\nSteps taken: {}\n".format(
            Board.pr, Board.pb, Board.b, self.steps
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


if __name__ == "__main__":
    #  solver = importSolver("../input/simple.in")
    solver = importSolver("../input/charleston_road_small.in")
    #  solver = importSolver("../input/rue_de_londres.in")
    #  solver = importSolver("../input/opera.in")
    #  solver = importSolver("../input/lets_go_higher.in")

    node = solver.hillClimbing()
    #  node = solver.steepestDescent()
    #  node = solver.simulatedAnnealing()
    #  node = solver.geneticAlgorithm()

    print(solver)
    print(node)
    #  print(node.__str__(True))
    #  solver.toImage("../out.png", 4, node)
