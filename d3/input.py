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
        matrix = make_matrix(fcontent.read())

    # slopes = [(1, 3)]
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]

    p1 = 0
    matches = []

    for (dy, dx) in slopes:
        x, y = 0, 0
        num_match = 0
        while y < len(matrix):
            num_match += 1 if get(x, y, matrix) == "#" else 0
            x += dx
            y += dy

        if dy == 1 and dx == 3:
            p1 = num_match

        matches.append(num_match)

    product = 1
    for m in matches:
        product *= m

    print(f"p1: {p1}")
    print(f"p2: {product}")

if __name__ == "__main__":
    main()
