#!/usr/bin/env python3

from random import shuffle


class Board:
    pb = 0
    pr = 0
    b = 0

    def __init__(self, h, w, r):
        self.h = h
        self.w = w
        self.r = r

        self.board = []
        self.backbone = (0, 0)
        self.walls = set()
        self.available_pos = []

    def setBackbone(self, br, bc):
        self.backbone = (br, bc)

    def setBoardInfo(self, info, cable_range):
        self.board = info

        # the range to check for walls is bigger walls is bigger
        wall_range = round(cable_range + self.r / 2)  # TODO use circle
        # maximum range from initial backbone
        rowi = max(0, self.backbone[0] - wall_range)
        coli = max(0, self.backbone[1] - wall_range)
        # +1 because python range's interval is open on the right hand side
        rowf = min(self.h, self.backbone[0] + wall_range + 1)
        colf = min(self.w, self.backbone[1] + wall_range + 1)
        for row in range(rowi, rowf):
            for col in range(coli, colf):
                if self.board[row][col] == "#":
                    self.walls.add((row, col))

        cable_range = round(cable_range)
        # maximum range from initial backbone
        rowi = max(0, self.backbone[0] - cable_range)
        coli = max(0, self.backbone[1] - cable_range)
        # +1 because python range's interval is open on the right hand side
        rowf = min(self.h, self.backbone[0] + cable_range + 1)
        colf = min(self.w, self.backbone[1] + cable_range + 1)
        self.available_pos = [
            (row, col)
            for row in range(rowi, rowf)
            for col in range(coli, colf)
            if self.board[row][col] == "."
        ]
        # shuffle available positions
        shuffle(self.available_pos)

    def updateAvailablePos(self, routers, maxdist):
        new_available_pos = set()
        for pos in self.available_pos:
            dist = (
                max(abs(pos[0] - self.backbone[0]), abs(pos[1] - self.backbone[1])) - 1
            )
            if dist <= maxdist:
                new_available_pos.add(pos)
                continue
            for router in routers:
                dist = max(abs(pos[0] - router[0]), abs(pos[1] - router[1])) - 1
                if dist <= maxdist:
                    new_available_pos.add(pos)
                    break

        self.available_pos = new_available_pos
        return len(self.available_pos) - len(new_available_pos)

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
                if (r, c) == self.backbone:
                    row += (0x30, 0x0, 0x17) * scale
                elif self.board[r][c] == ".":
                    row += (0x14, 0x69, 0xC7) * scale
                elif self.board[r][c] == "#":
                    row += (0xFF, 0xE1, 0x00) * scale
                elif self.board[r][c] == "-":
                    row += (0x17, 0x17, 0x17) * scale
            for s in range(scale):
                img.append(row)
        return img
