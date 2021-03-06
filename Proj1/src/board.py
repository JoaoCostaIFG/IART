#!/usr/bin/env python3

from random import choice, shuffle


class Board:
    EmptySquare = "."
    VoidSquare = "-"
    WallSquare = "#"

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
        self.covered_mem = {}

    def setBackbone(self, br, bc):
        self.backbone = (br, bc)

    # save the board information in more convenient structures
    # only set as available positions the squares that can be (theoretically)
    # reached by routers
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
                if self.board[row][col] == Board.WallSquare:
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
            if self.board[row][col] == Board.EmptySquare
        ]

    # returns a random available position from the board
    def getRandomPosOnce(self):
        shuffle(self.available_pos)
        return choice(self.available_pos)
    
    # returns a random generator for al lthe available positions on the board
    def getRandomPos(self):
        shuffle(self.available_pos)
        for pos in self.available_pos:
            yield pos

    # checks if the given cell is inside the board
    def isCellInsideBoard(self, cell):
        return cell[0] > 0 and cell[0] < self.h and cell[1] > 0 and cell[1] < self.w

    # gets the cell symbol at the position
    def getCell(self, cell):
        return self[cell[0]][cell[1]]

    # chekcs if the cell is empty (available)
    def isEmptyCell(self, cell):
        return self.getCell(cell) == Board.EmptySquare

    def __getitem__(self, key):
        return self.board[key]

    # calculates and saves the cells covered by the given router
    def getRouterCovered(self, router):
        if router in self.covered_mem:
            return self.covered_mem[router]

        covered = set()

        rowi = max(0, router[0] - self.r)
        coli = max(0, router[1] - self.r)
        rowf = min(self.h, router[0] + self.r + 1)
        colf = min(self.w, router[1] + self.r + 1)
        for row in range(rowi, rowf):
            for col in range(coli, colf):
                if self[row][col] != Board.EmptySquare:  # check if is available pos
                    continue

                # checks for walls on the square formed by the router anc the cell
                has_wall = False
                top = min(row, router[0])
                bot = max(row, router[0])
                left = min(col, router[1])
                right = max(col, router[1])
                for crow in range(top, bot + 1):
                    for ccol in range(left, right + 1):
                        if (crow, ccol) in self.walls:
                            has_wall = True
                            break
                if not has_wall:
                    covered.add((row, col))

        self.covered_mem[router] = covered
        return covered

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
                elif self.board[r][c] == Board.EmptySquare:
                    next_pixel = (0x14, 0x69, 0xC7)
                elif self.board[r][c] == Board.WallSquare:
                    next_pixel = (0xFF, 0xE1, 0x00)
                else:
                    next_pixel = (0x17, 0x17, 0x17)
                row += next_pixel * scale
            for s in range(scale):
                img.append(row)
        return img
