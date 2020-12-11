#!/usr/bin/env python3

from enum import Enum

from copy import deepcopy

class SeatStatus(Enum):
    FLOOR = 1
    EMPTY = 2
    OCCUPIED = 3
    INVALID = 4

def get_status(c):
    char_to_status = {
        ".": SeatStatus.FLOOR,
        "L": SeatStatus.EMPTY,
        "#": SeatStatus.OCCUPIED,
        "": SeatStatus.INVALID,
    }

    return char_to_status[c]

def get_char(s):
    status_to_char = {
        SeatStatus.FLOOR: ".",
        SeatStatus.EMPTY: "L",
        SeatStatus.OCCUPIED: "#",
        SeatStatus.INVALID: "Q",
    }

    return status_to_char[s]

def parse_matrix(lines):
    m = []

    for line in lines:
        row = []
        for c in line:
            row.append(get_status(c))
        m.append(row)

    return m

def check_diff(m1, m2):
    if m1 is None and m2 is not None or m2 is None and m1 is not None:
        return False

    if len(m1) != len(m2):
        return False

    for i in range(len(m1)):
        if len(m1[i]) != len(m2[i]):
            return False

        for j in range(len(m1[i])):
            if m1[i][j] != m2[i][j]:
                return False

    return True

def get(matrix, i, j):
    if i < 0 or i >= len(matrix):
        return SeatStatus.INVALID

    if j < 0 or j >= len(matrix[i]):
        return SeatStatus.INVALID

    return matrix[i][j]

def occupied_to_int(matrix, i, j):
    return 1 if get(matrix, i, j) == SeatStatus.OCCUPIED else 0

def count_adjacent(matrix, i, j):
    return sum([occupied_to_int(matrix, x, y)
        for y in range(j - 1, j + 2)
        for x in range(i - 1, i + 2)]) - occupied_to_int(matrix, i, j)

def next_iter(matrix):
    new = deepcopy(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            count = count_adjacent(matrix, i, j)
            if matrix[i][j] == SeatStatus.EMPTY and count == 0:
                new[i][j] = SeatStatus.OCCUPIED
            elif matrix[i][j] == SeatStatus.OCCUPIED and count >= 4:
                new[i][j] = SeatStatus.EMPTY
            else:
                new[i][j] = matrix[i][j]

    return new

def count_adjacent2(matrix, i, j):
    directions = [
        (-1, -1), ( 0, -1), ( 1, -1),
        (-1,  0), ( 0,  0), ( 1,  0),
        (-1,  1), ( 0,  1), ( 1,  1)
    ]

    s = 0

    for (dx, dy) in directions:
        if dx == 0 and dy == 0:
            continue

        x = j + dx
        y = i + dy

        found_seat = None

        dist = 0
        while True:
            got = get(matrix, y, x)
            if got != SeatStatus.FLOOR:
                found_seat = got
                break

            dist += 1

            y += dy
            x += dx

            if x < 0 or y < 0 or y >= len(matrix) or x >= len(matrix[y]):
                break

        if found_seat == SeatStatus.OCCUPIED:
            s += 1

    return s

def next_iter2(matrix):
    new = deepcopy(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if get(matrix, i, j) == SeatStatus.FLOOR:
                new[i][j] = SeatStatus.FLOOR
                continue
            count = count_adjacent2(matrix, i, j)
            if matrix[i][j] == SeatStatus.EMPTY and count == 0:
                new[i][j] = SeatStatus.OCCUPIED
            elif matrix[i][j] == SeatStatus.OCCUPIED and count >= 5:
                new[i][j] = SeatStatus.EMPTY
            else:
                new[i][j] = matrix[i][j]

    return new

def count_occupied(matrix):
    s = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            s += occupied_to_int(matrix, i, j)

    return s

def print_matrix(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(get_char(m[i][j]), end="")
        print("")
    print("")

def main():
    matrix = None

    with open("input", "r") as fcontent:
        lines = [line for line in fcontent.read().split("\n") if line]
        matrix = parse_matrix(lines)

    original_matrix = deepcopy(matrix)

    # print_matrix(matrix)
    new = None

    i = 0
    while True:
        new = next_iter(matrix)

        if check_diff(matrix, new):
            break

        matrix = new
        i += 1

    print(f"p1: {count_occupied(matrix)}")

    matrix = deepcopy(original_matrix)
    new = None

    i = 0
    while True:
        new = next_iter2(matrix)

        if check_diff(matrix, new):
            break

        matrix = new
        i += 1

    print(f"p2: {count_occupied(matrix)}")

if __name__ == "__main__":
    main()
