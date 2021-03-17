from os import listdir, path
FILE_PATH = path.join(".", "input")
def getInt(upper, lower=0, str="Please select a valid option"):
    print(str)
    answer = input()
    while not answer.isdigit() or (int(answer) < lower or int(answer) >= upper):
        print(str)
        answer = input()
    return int(answer)

def getYorN():
    print("Y or N")
    answer = input()
    while not (answer.lower() == "y" or answer.lower() == "n"):
        print("Y or N")
        answer = input()
    return answer.lower() == "y"


def selectOption(l):
    for i in range(len(l)):
        print(str(i) + "- " + l[i])
    
    return getInt(len(l))
    
def selectInputFile():
    files = listdir(FILE_PATH)
    return files[selectOption(files)]

def selectAlgorithm():
    algorithms = ["Hill Climbing", "Steepest Descent", "Simulated Annealing", "Genetic Algorithm"]
    return algorithms[selectOption(algorithms)]

    
from src.solver import importSolver
if __name__ == "__main__":
    algorithm = selectAlgorithm()
    file = selectInputFile()

    solver = importSolver(path.join(FILE_PATH, file))

    if algorithm == "Hill Climbing":
        node = solver.hillClimbing()
    elif algorithm == "Steepest Descent":
        node = solver.steepestDescent()
    elif  "Simulated Annealing":
        node = solver.simulatedAnnealing()
    elif  "Genetic Algorithm":
        node = solver.geneticAlgorithm()

    print(solver)
    print("\n\nDo you want to preview the map?")
    if (getYorN()):
        print(node.__str__(True))
    
    print("\n\nDo you want to export to png?")
    if (getYorN()):
        print("Type the name of the exported image")
        image = input()
        # solver.toImage(image, 4, node)