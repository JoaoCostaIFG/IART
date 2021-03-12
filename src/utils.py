#!/usr/bin/env python3


def getAdjacentCoords(Coord, maxX=0, maxY=0):
    def checkBoundary(X, Y):
        return X >= 0 and X < maxX and Y >= 0 and Y < maxY

    X, Y = Coord
    res = set()

    offsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for offsetX, offsetY in offsets:
        currX = X + offsetX
        currY = Y + offsetY
        if checkBoundary(currX, currY):
            res.add((currX, currY))

    return res


def getCoordsBetween(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    dx = x2 - x1
    signalx = 1 if dx >= 0 else -1
    dy = y2 - y1
    signaly = 1 if dy >= 0 else -1
    if abs(dx) > abs(dy):
        inc_row = False
        maxd = abs(dx)
        mind = abs(dy)
    else:
        inc_row = True
        maxd = abs(dy)
        mind = abs(dx)

    res = []
    # Main Diagonal
    for i in range(1, mind):
        res.append((x1 + i * signalx, y1 + i * signaly))
    if inc_row:  # Row Major
        for i in range(mind, maxd):
            res.append((x1 + mind * signalx, y1 + i * signaly))
    else:  # Column major
        for i in range(mind, maxd):
            res.append((x1 + i * signalx, y1 + mind * signaly))

    return res
