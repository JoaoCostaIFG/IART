#!/usr/bin/env python3

from MinimumSpanningTree import Graph
from utils import getAdjacentCoords
from random import choices


class Node:
    def __init__(self, board, routers=[], backbones=[]):
        self.board = board
        self.routers = routers
        self.backbones = backbones

        self.val = 0
        self.need_calc = True
        self.covered = set()

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

    # TODO remove not in routers by removing router from possible coords on selection
    def genNeighbours(self, random=False):
        # Get random router to add to son
        selected_pos = self.board.available_pos
        if (random):
            selected_pos = choices(list(self.board.available_pos), k=len(self.board.available_pos))

        for pos in selected_pos:
            if pos not in self.routers:
                routers = self.routers.copy()
                routers.append(pos)
                son = Node(self.board, routers, self.backbones)
                # self.board.available_pos.remove(router)
                yield son

    def getCost(self, pr, pb):
        graph = Graph(self.board.backbone, self.routers)
        return graph.getBackboneLen() * pb + len(self.routers) * pr

    # TODO vaue will need to use set union
    def getValue(self, pr=0, pb=0, b=0):
        if not self.need_calc:
            return self.val

        board = self.board.board
        r = self.board.r
        self.covered = set()

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
                        self.covered.add((row, col))

        self.need_calc = False
        cost = self.getCost(pr, pb)
        if cost > b:
            self.val = 0
        else:
            # score = 1000 * target + (B - (backbones * pb + routers * pr))
            self.val = len(self.covered) * 1000 + (b - cost)

        return self.val

    def __str__(self):
        res = "Value is {}\n".format(self.val)

        for x in range(self.board.h):  # For each row
            for y in range(self.board.w):  # For each cell
                if (x, y) == self.board.backbone:
                    res += "B"
                elif (x, y) in self.routers:
                    res += "R"
                elif (x, y) in self.covered:
                    res += ":"
                elif (x, y) in self.backbones:
                    res += "b"
                else:
                    res += self.board.board[x][y]
            res += "\n"

        return res
