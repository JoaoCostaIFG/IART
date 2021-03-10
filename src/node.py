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
            possibleCoords.update(
                getAdjacentCoords(backbone, self.board.h, self.board.w)
            )

        # notAWall = lambda coord: self.board[coord[0]][coord[1]] != "#"
        # notARouter = lambda coord: coord not in self.routers
        return (
            coord for coord in possibleCoords if notAWall(coord) and notARouter(coord)
        )

    def getPossibleBackbones(self, h, w):
        possibleCoords = set()
        for backbone in self.backbones:
            possibleCoords.update(getAdjacentCoords(backbone, h, w))

        return (coord for coord in possibleCoords)

    def genNeighbours(self, board):
        print("Nada")

    def getValue(self):
        board = self.board.board
        r = self.board.r
        self.covered = set()
        val = 0

        for row in range(0, self.board.h):
            for col in range(0, self.board.w):
                if board[row][col] != ".":
                    continue
                for router in self.routers:
                    has_wall = False
                    if abs(router[0] - row) > r or abs(router[1] - col) > r:
                        continue  # go check next router
                    for wall in self.board.walls:
                        if (
                            min(row, router[0]) <= wall[0]
                            and wall[0] <= max(row, router[0])
                            and min(col, router[1]) <= wall[1]
                            and wall[1] <= max(col, router[1])
                        ):
                            has_wall = True
                            break
                    if not has_wall:
                        val += 1
                        self.covered.add((row, col))

        print("covered:", self.covered)
        return len(self.covered)

    def __str__(self):
        res = ""

        for x in range(self.board.h):  # For each row
            for y in range(self.board.w):  # For each cell
                if (x, y) in self.routers:
                    res += "R"
                elif (x, y) in self.covered:
                    res += "C"
                elif (x, y) in self.backbones:
                    res += "b"
                else:
                    res += self.board.board[x][y]
            res += "\n"

        return res
