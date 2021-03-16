#!/usr/bin/env python3

import png

from board import Board
from node import Node
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
        node = Node(self.board)
        node.val = Board.b
        return node

    def stopCondition(self, current, cells_to_cover):
        return len(current.covered) < cells_to_cover and Board.b - current.getCost() > Board.pr

    def isBetterSol(self, neighbor, current):
        return neighbor.getValue() > current.getValue()

    def hillClimbing(self):
        current = self.genRootNode()  # initial node
        cells_to_cover = len(self.board.available_pos)

        while self.stopCondition(current, cells_to_cover):
            self.steps += 1
            neighbors = current.genNeighbours()  # neighbor generator
            found_better = False

            for neighbor in neighbors:
                if self.isBetterSol(neighbor, current):
                    found_better = True
                    neighbor.commit()  # update info of new chosen node
                    current = neighbor
                    break
                else:
                    # remove rejected nodes (they won't ever help)
                    neighbor.cleanup()  # cleanup the unused node
                    self.board.available_pos.remove(neighbor.router)
            neighbors.close()

            if not found_better:
                return current

        return current

    def steepestDescentMax(self, node):
        neighbors = node.genNeighbours()
        best_neighbor = next(neighbors)  # TODO this can throw

        best_neighbor.getValue()
        best_neighbor.cleanup()  # cleanup to check others

        for neighbor in neighbors:
            is_better = False
            if self.isBetterSol(neighbor, best_neighbor):
                is_better = True
            neighbor.cleanup()  # cleanup previous best
            if is_better:
                best_neighbor = neighbor
        neighbors.close()

        return best_neighbor

    def steepestDescent(self):
        current = self.genRootNode()  # initial node
        cells_to_cover = len(self.board.available_pos)

        while self.stopCondition(current, cells_to_cover):
            self.steps += 1
            best_neighbor = self.steepestDescentMax(current)
            if not self.isBetterSol(best_neighbor, current):
                # no need to cleanup (already performed that operation)
                return current

            # we have a new best, but need to recalculate him to save the new graph
            # so we force recalculation
            best_neighbor.getValue(True)
            best_neighbor.commit()
            current = best_neighbor

        return current

    # returns the annealing schedule
    def temperature(self, init_temp, frac):
        #  if Ɛ <= neper_num ** (-delta / tk):
        return init_temp * frac

    def simulatedAnnealing(self, init_temp=1000.0, kmax=5):
        # K is our self.steps in our implementation
        current = self.genRootNode()
        neighbours = current.genNeighbours()

        for self.steps in range(kmax):
            neighbor = next(neighbours)
            was_chosen = False

            if current.getValue() < neighbor.getValue():
                was_chosen = True
            elif Board.b - neighbor.getCost() >= 0:
                # solution is feasible
                delta = neighbor.getValue() - current.getValue()
                t = self.temperature(init_temp, float(self.steps + 1) / kmax)
                Ɛ = exp(-delta / t)
                if random() < Ɛ:
                    was_chosen = True

            if was_chosen:
                current = neighbor
                current.commit()  # update info of new chosen node
                neighbours = current.genNeighbours()
            else:  # node wasn't chosen => cleanup
                neighbor.cleanup()

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
            node.need_calcBackbone = True
            node.getValueAll(True)
            # yield node
            res.append(node)
        return res

    def geneticAlgorithm(self, nPop=10, it=3, mutateProb=20):
        population = self.generatePopulation(nPop)
        weights = [node.getValue() for node in population]
        for i in range(it): # TODO Maybe change to time constraint?
            new_population = []
            new_weights = []
            print(weights)
            for j in range(len(population)):
                node1 = choices(population, weights=weights).pop()
                node2 = choices(population, weights=weights).pop()
                child = node1.reproduce(node2)
                if (random() < mutateProb):
                    child.mutate()
                new_population.append(child)
                new_weights.append(child.getValue())
            population = new_population
            weights = new_weights
        return max(population, key=lambda node: node.getValue())




    def toImage(self, filename, scale=1, node=None):
        if node:
            img = node.toImage(scale)
        else:
            img = self.board.toImage(scale)

        # TODO
        #  img = [[ord(c) for c in row] for row in self.board]
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
    #  solver = importSolver("../input/charleston_road.in")
    solver = importSolver("../input/rue_de_londres.in")
    #  solver = importSolver("../input/opera.in")
    #  solver = importSolver("../input/lets_go_higher.in")

    node = solver.geneticAlgorithm()
    #  node = solver.steepestDescent()
    #  node = solver.simulatedAnnealing()
    #  node = solver.simulatedAnnealing(100000, 500)

    print(solver)
    print(node)
    #  print(node.__str__(True))
    #  solver.toImage("../out.png", 4, node)
