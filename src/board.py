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

    # save the board information in more convenient structures
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

    # filter from the available positions set the positions that
    # aren't reachable with our current budget
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
        res = "Board {}x{}\nRouter range is {}\nBackbone at {}".format(
            self.h, self.w, self.r, self.backbone
        )

        return res

    # scale is how many pixels the side of one 1 board cell takes in the output image
    # returns a RGB pixel grid
    def toImage(self, scale=1):
        img = []
        for r in range(self.h):
            row = ()
            for c in range(self.w):
                if (r, c) == self.backbone:
                    next_pixel = (0x30, 0x0, 0x17)
                elif self.board[r][c] == ".":
                    next_pixel = (0x14, 0x69, 0xC7)
                elif self.board[r][c] == "#":
                    next_pixel = (0xFF, 0xE1, 0x00)
                else:
                    next_pixel = (0x17, 0x17, 0x17)
                row += next_pixel * scale
            for s in range(scale):
                img.append(row)
        return img
