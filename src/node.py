#!/usr/bin/env python3

from utils import getAdjacentCoords


class Node:
    def __init__(self, board, routers=[], backbones=[]):
        self.board = board
        self.routers = routers
        self.backbones = backbones

    def addRouter(self, router):
        self.routers.append(router)

    def addBackBone(self, backbone):
        self.backbones.append(backbone)

    def getPossibleRouters(self):
        def notAWall(coord):
            return self.board.board[coord[0]][coord[1]] != "#"

        def notARouter(coord):
            return coord not in self.routers

        possibleCoords = set()
        for backbone in self.backbones:
            possibleCoords.update(getAdjacentCoords(backbone, self.board.h, self.board.w))

        # notAWall = lambda coord: self.board[coord[0]][coord[1]] != "#"
        # notARouter = lambda coord: coord not in self.routers
        return (
            coord for coord in possibleCoords if notAWall(coord) and notARouter(coord)
        )

    def genNeighbours(self, board):
        print("Nada")

    def getValue(self):
        val = 0

        for router in self.routers:
            rowi = max(0, router[0] - self.board.r)
            coli = max(0, router[1] - self.board.r)
            rowf = min(self.board.h, router[0] + self.board.r + 1)
            colf = min(self.board.w, router[1] + self.board.r + 1)
            for row in range(rowi, rowf):
                for col in range(coli, colf):
                    if self.board.board[row][col] == ".":
                        val += 1

        return val

    def __str__(self):
        res = ""

        for x in range(self.board.h):  # For each row
            for y in range(self.board.w):  # For each cell
                if (x, y) in self.routers:
                    res += "R"
                elif (x, y) in self.backbones:
                    res += "b"
                else:
                    res += self.board.board[x][y]
            res += "\n"

        return res
