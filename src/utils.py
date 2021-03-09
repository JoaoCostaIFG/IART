def getAdjacentCoords(Coord, maxX=0, maxY=0):
    X, Y = Coord
    checkBoundary = lambda X, Y: (X >= 0 and X < maxX and Y >= 0 and Y< maxY)
    res = []

    offsets = ((-1, -1), (-1, 0), (-1, 1),
               (0, -1),           (0, 1),
               (1, -1),  (1, 0),  (1, 1))
    for offsetX, offsetY in offsets:
        currX = X + offsetX
        currY = Y + offsetY
        if (checkBoundary(currX, currY)):
            res.append([currX, currY])
    
    return res