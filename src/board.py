#!/usr/bin/env python3

class Board:
    def __init__(self, board=[], routers=[], backbones=[]):
        self.board = board
        self.routers = routers
        self.backbones = backbones

    def apppendRow(self, row):
        self.board.append(list(row[:-1]))

    def addRouter(self, router):
        self.routers.append(router)

    def addBackBone(self, backbone):
        self.backbones.append(backbone)

    def getPossibleRouters(self, h, w):
        from utils import getAdjacentCoords
        possibleCoords = set()
        for backbone in self.backbones:
            possibleCoords.update(getAdjacentCoords(backbone, h, w))

        notAWall = lambda coord: self.board[coord[0]][coord[1]] != "#"
        notARouter = lambda coord: coord not in self.routers
        return (coord for coord in possibleCoords if notAWall(coord) and notARouter(coord))
    
    def __str__(self):
        res = ""
        for x in range(len(self.board)): # For each row
            for y in range(len(self.board[x])): # For each cell
                if ((x, y) in self.routers):
                    res += "r"
                elif ((x, y) in self.backbones):
                    res += "b"
                else:
                    res += self.board[x][y]
            res += "\n"

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
