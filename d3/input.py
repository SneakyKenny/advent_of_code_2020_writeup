#!/usr/bin/env python3

def make_matrix(s):
    m = []

    for l in s.split("\n"):
        if not l:
            continue
        m.append([c for c in l])

    return m

def get(x, y, m):
    return m[y][x % len(m[y])]

def main():
    matrix = None
    with open("input", "r") as fcontent:
        s = fcontent.read()
        # print(s)
        matrix = make_matrix(s)

    # print(f"{len(matrix)} x {len(matrix[0])}")

    num_match = 0

    x = 0
    for i in range(len(matrix)):
        num_match += 1 if get(x, i, matrix) == "#" else 0
        x += 3

    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]

    matches = []
    for (dy, dx) in slopes:
        x, y = 0, 0
        num_match = 0
        while y < len(matrix):
            num_match += 1 if get(x, y, matrix) == "#" else 0
            x += dx
            y += dy
        matches.append(num_match)

    p = 1
    for m in matches:
        p *= m

    print(f"p1: {num_match}")
    print(f"p2: {p}")

if __name__ == "__main__":
    main()
