#!/usr/bin/env python3

class Board:
    def __init__(self, board=[], routers=[], backbones=[]):
        self.board = board
        self.routers = routers
        self.backbones = backbones

    def apppendRow(self, row):
        self.board.extend(row.split())

    def addRouter(self, router):
        self.routers.append(router)

    def addBackBone(self, backbone):
        self.backbones.append(backbone)

    def getPossibleRouters(self):
        from utils import getAdjacentCoords
        for backbone in self.backbones:
            print(getAdjacentCoords(backbone))


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

    def __str__(self):
        return  "\n".join(self.board)
