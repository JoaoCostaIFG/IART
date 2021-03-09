#!/usr/bin/env python3


class Node:
    def __init__(self, board):
        self.board = board

    def genNeighbours(self, board):
        print("Nada")

    def getValue(self, r, w, h):
        val = 0

        for router in self.board.routers:
            rowi = max(0, router[0] - r)
            coli = max(0, router[1] - r)
            rowf = min(h, router[0] + r + 1)
            colf = min(w, router[1] + r + 1)
            for row in range(rowi, rowf):
                for col in range(coli, colf):
                    if self.board.board[row][col] == ".":
                        val += 1

        return val
