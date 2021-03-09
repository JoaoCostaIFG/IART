#!/usr/bin/env python3

# import png
from board import Board
from node import Node


class Solver:
    def __init__(self, h, w, r):
        self.h = h
        self.w = w
        self.r = r

        self.board = Board()
        #  self.board = [None] * (h * w)

        self.pb = self.pr = self.b = 0
        self.backbone = [0, 0]

    def setPrices(self, pb, pr, b):
        self.pb = pb
        self.pr = pr
        self.b = b

    def setBackbone(self, br, bc):
        self.backbone = [br, bc]

    def dump(self):
        print(
            "Board {}x{}. Router range is {}. Backbone at {}".format(
                self.h, self.w, self.r, self.backbone
            )
        )
        print(
            "Router price is {}. Backbone price is {}. Max budget is {}".format(
                self.pr, self.pb, self.b
            )
        )

    def toImage(self, filename, scale=1):
        img = self.board.toImage(scale)

        # TODO
        #  img = [[ord(c) for c in row] for row in self.board]
        with open(filename, "wb+") as f:
            w = png.Writer(self.w * scale, self.h * scale, greyscale=False)
            w.write(f, img)


def importSolver(filename):
    with open(filename, "r") as f:
        # read H, W and R (board size and router range)
        solver = Solver(*map(int, f.readline().split()))
        # read Pb, Pr and B (prices and budget)
        solver.setPrices(*map(int, f.readline().split()))
        # read br and bc (intial backbone coordinates)
        solver.setBackbone(*map(int, f.readline().split()))
        # read board
        for i in range(solver.h):
            solver.board.apppendRow(f.readline())
    return solver


solver = importSolver("input/simple.in")
solver.dump()
board = Board(solver.board.board, [], [(1, 2), (5, 5)])
print(list(board.getPossibleRouters(solver.h, solver.w)))
print(board)
print(board.board)
# solver.toImage("out.png", 100)
# node.genNeighbours("asd")