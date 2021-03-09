#!/usr/bin/env python3

import png


class Solver:
    def __init__(self, h, w, r):
        self.h = h
        self.w = w
        self.r = r

        self.board = []
        #  self.board = [None] * (h * w)

        self.pb = self.pr = self.b = 0
        self.backbone = [0, 0]

    def setPrices(self, pb, pr, b):
        self.pb = pb
        self.pr = pr
        self.b = b

    def setBackbone(self, br, bc):
        self.backbone = [br, bc]

    def apppendRow(self, row):
        self.board.extend(row.split())

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
        img = []
        for r in range(self.h):
            row = ()
            for c in range(self.w):
                if self.board[r][c] == ".":
                    row += (0x14, 0x69, 0xC7) * scale
                elif self.board[r][c] == "#":
                    row += (0xFF, 0xE1, 0x00) * scale
                elif self.board[r][c] == "-":
                    row += (0x17, 0x17, 0x17) * scale
            for s in range(scale):
                img.append(row)

        # TODO
        #  img = [[ord(c) for c in row] for row in self.board]
        with open(filename, "wb+") as f:
            w = png.Writer(self.w * scale, self.h * scale, greyscale=False)
            w.write(f, img)


with open("input/simple.in", "r") as f:
    # read H, W and R (board size and router range)
    solver = Solver(*map(int, f.readline().split()))
    # read Pb, Pr and B (prices and budget)
    solver.setPrices(*map(int, f.readline().split()))
    # read br and bc (intial backbone coordinates)
    solver.setBackbone(*map(int, f.readline().split()))
    # read board
    for i in range(solver.h):
        solver.apppendRow(f.readline())


solver.dump()
solver.toImage("out.png", 100)
