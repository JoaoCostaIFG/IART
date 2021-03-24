#!/usr/bin/env python3

from os import listdir, path
from src.solver import importSolver


def getInt(upper, lower=0, str="Please select a valid option"):
    answer = ""
    while not answer.isdigit() or (int(answer) < lower or int(answer) >= upper):
        print(str)
        answer = input()
        print()
    return int(answer)


def getYorN():
    answer = None
    while not (answer == "y" or answer == "n"):
        print("[Y/n]", end=" ")
        answer = input().lower()
        if answer == "":
            answer = "y"
    return answer == "y"


def selectOption(op_list):
    for i in range(len(op_list)):
        print(str(i) + " - " + op_list[i])
    return getInt(len(op_list))


def selectInputFile():
    global FILE_PATH
    files = listdir(FILE_PATH)
    return files[selectOption(files)]


def selectAlgorithm():
    algorithms = [
        "Hill Climbing",
        "Steepest Descent",
        "Simulated Annealing",
        "Genetic Algorithm",
    ]
    return algorithms[selectOption(algorithms)]


FILE_PATH = path.join(".", "input")

if __name__ == "__main__":
    #  solver = importSolver("input/charleston_road.in")
    solver = importSolver("input/charleston_road_small.in")

    #  sol = solver.hillClimbing()
    #  sol = solver.steepestDescent()
    sol = solver.simulatedAnnealing()
    print(solver)
    print(sol.__str__(True))
    solver.toImage("out.png", 4, sol)

    #  algorithm = selectAlgorithm()
    #  file = selectInputFile()

    #  solver = importSolver(path.join(FILE_PATH, file))

    #  if algorithm == "Hill Climbing":
    #  sol = solver.hillClimbing()
    #  elif algorithm == "Steepest Descent":
    #  sol = solver.steepestDescent()
    #  elif "Simulated Annealing":
    #  sol = solver.simulatedAnnealing()
    #  elif "Genetic Algorithm":
    #  sol = solver.geneticAlgorithm()

    #  print(solver)
    #  print("\n\nDo you want to preview the map?", end=" ")
    #  if getYorN():
    #  print(sol.__str__(True))

    #  print("\n\nDo you want to export to png?", end=" ")
    #  if getYorN():
    #  print("Type the name of the image to export:", end=" ")
    #  image = input()
    #  if image[-4:-2] != ".png":  # append '.png' to the file name if not present
    #  image += ".png"
    #  solver.toImage(image, 4, sol)

    #  print("\n\nDo you want to export the solution to a file?", end=" ")
    #  if getYorN():
    #  print("Type the name of the file to export:", end=" ")
    #  filename = input()
    #  if filename[-4:-2] != ".txt":  # append '.txt' to the file name if not present
    #  filename += ".txt"
    #  sol.toFile(filename)
