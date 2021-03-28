from os import pardir, path
import matplotlib.pyplot as plt
import numpy as np

def stocasticHillclimbingParse(line):
    contents = line.split(" ")
    step = int(contents[1])
    cost = int(contents[4].split("/")[0])
    score = int(contents[-1].replace("\n", ""))
    return (step, cost, score)

def annealingParse(line):
    contents = line.split(" ")
    temperature = float(contents[1])
    step = int(contents[4])
    cost = int(contents[7].split("/")[0])
    score = int(contents[-1].replace("\n", ""))
    return (step, temperature, cost, score)

def geneticParse(line):
    contents = line.split(" ")
    print(contents)
    temperature = float(contents[1])
    step = int(contents[4])
    cost = int(contents[7].split("/")[0])
    score = int(contents[-1].replace("\n", ""))
    return (step, temperature, cost, score)


def parse(FIELDS, parseFunc, file):
    filename = path.join("results", file)
    res = {}
    for field in FIELDS:
        res[field] = []
    with open(filename, "r") as f:
        for line in f:
            if "Step: " in line:
                data = parseFunc(line)
                print(data)
                for i in range(len(FIELDS)):
                    res[FIELDS[i]].append(data[i])
    return res

# https://stackoverflow.com/questions/50685409/select-n-evenly-spaced-out-elements-in-array-including-first-and-last
def GetSpacedElements(array, numElems = 4):
    out = array[np.round(np.linspace(0, len(array)-1, numElems)).astype(int)]
    return out

def plot(data, colors):
    if (len(data) == 0):
        return
    figure, subplots = plt.subplots(len(data[0]) - 1, 1)
    i = 0
    for field in data[0]:
        if (field != "steps"):
            for solI in range(len(data)):
                print(i)
                subplots[i].plot(data[solI][field], color=colors[field][solI])
                subplots[i].set_xlabel("steps")
                subplots[i].set_ylabel(field)
            i += 1
    #plt.xticks(np.arange(min(x), max(x), max(x)/10))
    #plt.yticks(np.arange(min(z), max(z), max(z)/80))
    plt.show()

# HillClimbing
res1 = parse(["steps", "cost", "score"], stocasticHillclimbingParse, "sh.txt")
res2 = parse(["steps", "cost", "score"], stocasticHillclimbingParse, "sh2.txt")
res3 = parse(["steps", "cost", "score"], stocasticHillclimbingParse, "sh3.txt")

# Genetic
# res1 = parse(["steps", "cost", "score"], stocasticHillclimbingParse, "gn.txt")
# res2 = parse(["steps", "cost", "score"], stocasticHillclimbingParse, "gn2.txt")
# res3 = parse(["steps", "cost", "score"], stocasticHillclimbingParse, "gn3.txt")

# Annealing
# res1 = parse(["steps", "temperature", "cost", "score"], annealingParse, "an.txt")
# res2 = parse(["steps", "temperature", "cost", "score"], annealingParse, "an2.txt")
# res3 = parse(["steps", "temperature", "cost", "score"], annealingParse, "an3.txt")

colors = {"cost" : ["orange", "blue", "green"], "score" : ["orange", "blue", "green"], "temperature" : ["orange", "blue", "green"]}
plot((res1, res2, res3), colors)