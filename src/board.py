#!/usr/bin/env python3


class Board:
    def __init__(self, h, w, r):
        self.h = h
        self.w = w
        self.r = r

        self.board = []
        self.backbone = [0, 0]
        self.walls = set()

    def setBoard(self, board):
        self.board = board

        for row in range(self.h):
            for col in range(self.w):
                if self.board[row][col] == "#":
                    self.walls.add((row, col))

    def setBackbone(self, br, bc):
        self.backbone = [br, bc]

    def __str__(self):
        res = "Board {}x{}. Router range is {}. Backbone at {}".format(
            self.h, self.w, self.r, self.backbone
        )

        return res

    def toImage(self, scale=1):
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
        return img
