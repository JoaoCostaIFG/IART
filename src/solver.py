#!/usr/bin/env python3

import src.png as png
from src.board import Board
from src.solution import Solution
from math import exp, floor
from random import random, choices
from statistics import pstdev
from time import time


class Solver:
    def __init__(self, h, w, r):
        self.steps = 0
        self.board = Board(h, w, r)
        self.steps = 0

    def setPrices(self, pb, pr, b):
        Board.pb = pb
        Board.pr = pr
        Board.b = b
        self.max_router_num = floor(Board.b / Board.pr)

    def setBackbone(self, br, bc):
        self.board.setBackbone(br, bc)

    def setBoardInfo(self, info):
        # max range at which a router can be placed and still be in budget
        cable_range = (Board.b - Board.pr) / Board.pb
        self.board.setBoardInfo(info, cable_range)

    def genInitialSol(self):
        pseudoSol = []

        for pos in self.board.getRandomPos():
            if len(pseudoSol) >= self.max_router_num:
                break
            pseudoSol.append(pos)

        return Solution(self.board, pseudoSol)

    def logIteration(self, currentSol=None):
        print(
            "Step: {} - Cost/Budget: {}/{} - Score: {}".format(
                self.steps, currentSol.getCost(), Board.b, currentSol.getValue()
            )
        )

        #  if currentSol and self.steps % 10 == 0:
        #  print(currentSol.__str__(True), end="\n\n")

    def startTimer(self):
        self.start_time = time()

    def hillClimbing(self, current=None):
        print("Stochastic hillclimbing")
        self.startTimer()
        if not current:
            current = self.genInitialSol()  # initial sol

        #  while self.steps <= max_iter:
        while True:
            self.steps += 1
            found_better = False
            for neighbor in current.mutate():
                if neighbor > current:
                    found_better = True
                    current = neighbor
                    break

            if not found_better:
                print("Took:", time() - self.start_time)
                return current
            self.logIteration(current)

        print("Took:", time() - self.start_time)
        return current

    def steepestDescentMax(self, sol):
        neighbors = sol.mutate()
        best_neighbor = next(neighbors)  # TODO this can throw

        for neighbor in neighbors:
            if neighbor > best_neighbor:
                best_neighbor = neighbor

        return best_neighbor

    def steepestDescent(self, current=None):
        print("Steepest Descent hillclimbing")
        self.startTimer()
        if not current:
            current = self.genInitialSol()  # initial sol

        # while self.steps <= max_iter:
        while True:
            self.steps += 1
            best_neighbor = max(current.mutate())
            if best_neighbor <= current:
                return current
            current = best_neighbor
            self.logIteration(current)

        print("Took:", time() - self.start_time)
        return current

    # returns the standard deviation of the value of population_size (default 400)
    # initial solutions/states.
    # this is used to obtain the intial temperature to use for a problem
    def calculateInitialTemp(self, population_size=400):
        intial_values = []
        for i in range(population_size):
            sol = self.genInitialSol()
            intial_values.append(sol.getValue())
        return pstdev(intial_values)

    # returns the current temperature of the system based on the
    # initial temperature the fraction of the iterations performed
    def schedule(self, t):
        return float(t) * 0.90

    def simulatedAnnealing(self, current=None, min_temp=0.1, random_restart_chance=0.05):
        print(
            "Simulated Annealing. min_temp: {}. random restart chance: {}".format(
                min_temp, random_restart_chance
            )
        )
        print("Calculating the initial temperature.")
        self.startTimer()
        init_temp = self.calculateInitialTemp() // (4 / 3)
        t = init_temp
        iter_per_temp = self.max_router_num
        print(
            "Initial temperature is {}. Doing {} iteration(s) per temperature.".format(
                t, iter_per_temp
            )
        )

        if not current:
            current = self.genInitialSol()
        best = current
        best_temp = t
        while True:
            self.steps += 1
            neighbors = current.mutate()
            # for each temperature iterate max_router_num times
            for m in range(iter_per_temp):
                neighbor = next(neighbors)  # TODO this can throw
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
                # save best solution we got so far
                if current > best:
                    best = current
                    best_temp = t
            # cool down
            t = self.schedule(t)

            # random restart
            if random() < random_restart_chance:
                print("Restarting")
                current = best
                t = best_temp

            print("Temperature:", t, end=" - ")
            self.logIteration(current)

            # stop condition
            if abs(t) <= min_temp:  # this is the final iteration
                # if we had a better solution, go back and try again
                if current.getValue() < best.getValue():
                    print("Restarting")
                    current = best
                    t = best_temp
                else:
                    break

        print("Took:", time() - self.start_time)
        return best

    def generatePopulation(self, nPop):
        res = []
        for i in range(nPop):
            res.append(self.genInitialSol())

        return res

    def geneticAlgorithm(self, nPop=100, it=100, mutateProb=0.1):
        print(
            "Genetic algorithm. Population size: {}. Iterations: {}. Mutation probability: {}.".format(
                nPop, it, mutateProb
            )
        )
        self.startTimer()
        population = self.generatePopulation(nPop)
        weights = [sol.getValue() for sol in population]

        for self.steps in range(it):  # TODO Maybe change to time constraint?
            # save the previous best (elitism)
            prev_pop_best = max(population, key=lambda sol: sol.getValue())
            new_population = [prev_pop_best]
            new_weights = [prev_pop_best.getValue()]
            while len(new_population) < len(population):
                sol1, sol2 = choices(population, weights=weights, k=2)
                if sol1 == sol2:  # don't allow children with one self
                    continue
                child = sol1.crossover(sol2)
                if random() < mutateProb:
                    child = next(child.mutate())
                new_population.append(child)
                new_weights.append(child.getValue())
            population = new_population
            weights = new_weights

            self.logIteration(max(population, key=lambda sol: sol.getValue()))

        print("Took:", time() - self.start_time)
        return max(population, key=lambda sol: sol.getValue())

    # scale is how many pixels the side of one 1 board cell takes in the output image
    # if a sol is given, the solution represented by that sol will be drawn
    # outputs the result to a file in the given path
    def toImage(self, filename, scale=1, sol=None):
        if sol:
            img = sol.toImage(scale)
        else:
            img = self.board.toImage(scale)

        with open(filename, "wb+") as f:
            w = png.Writer(self.board.w * scale, self.board.h * scale, greyscale=False)
            w.write(f, img)

    def __str__(self):
        return (
            str(self.board)
            + "\n"
            + "Router price: {}\nBackbone price: {}\nMax budget: {}\nSteps taken: {}\n".format(
                Board.pr, Board.pb, Board.b, self.steps
            )
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

    sol = solver.hillClimbing()
    #  sol = solver.steepestDescent()
    #  sol = solver.simulatedAnnealing()
    #  sol = solver.geneticAlgorithm()

    print(solver)
    print(sol)
    #  print(sol.__str__(True))
    #  solver.toImage("../out.png", 4, sol)
