#!/usr/bin/env python3

start_state = [0, 0]
end_state = [2, 0]


# OPERATORS
def empty_left(b):
    return [0, b[1]]


def empty_right(b):
    return [b[0], 0]


def fill_left(b):
    return [4, b[1]]


def fill_right(b):
    return [b[0], 3]


def pass_to_right(b):
    left_to_full = 3 - b[1]
    if left_to_full > b[0]:
        amount = b[0]
    else:
        amount = left_to_full
    return [b[0] - amount, b[1] + amount]


def pass_to_left(b):
    left_to_full = 4 - b[0]
    if left_to_full > b[1]:
        amount = b[1]
    else:
        amount = left_to_full
    return [b[0] + amount, b[1] - amount]


# DFS
def dfs(b, visited):
    if b[0] == 2:  # end state
        return True
    if b in visited:  # already visited this node
        return False

    visited.append(b)
    # empty
    if b[0] > 0:
        if dfs(empty_left(b), visited):
            return True
    if b[1] > 0:
        if dfs(empty_right(b), visited):
            return True
    # fill
    if b[0] < 4:
        if dfs(fill_left(b), visited):
            return True
    if b[1] < 3:
        if dfs(fill_right(b), visited):
            return True
    # pass
    if b[0] > 0 and b[1] < 3:
        if dfs(pass_to_right(b), visited):
            return True
    if b[0] < 4 and b[1] > 0:
        if dfs(pass_to_left(b), visited):
            return True

    return False


visited = []
dfs(start_state.copy(), visited)
print(visited)
