#!/usr/bin/env python3

def get_seat_id(row, col):
    return 8 * row + col

def get_coord(s, a, b, c1, c2):
    # print(f"range: {a}, {b}")
    for i in range(len(s)):
        # print(f"char: {s[i]}")
        if s[i] == c1:
            a = (a + b) // 2 + 1
            # print(f"new (a) range: {a}, {b}")
        elif s[i] == c2:
            b = (a + b) // 2
            # b = b // 2
            # print(f"new (b) range: {a}, {b}")
        else:
            print(f"invalid char: {s[i]}")
    return a

def main():
    lines = None

    with open("input", "r") as fcontent:
        lines = [line for line in fcontent.read().split("\n") if line]

    max_id = 0
    occupied = {}

    for s in lines:
        row = get_coord(s[:7], 0, 127, "B", "F")
        col = get_coord(s[7:], 0, 7, "R", "L")
        seat_id = get_seat_id(row, col)
        # print(f"{s}: row {row}, col {col}, id {seat_id}")
        max_id = max(max_id, seat_id)
        occupied[seat_id] = True

    # print(f"max id: {max_id}")

    """
    for i in range(max_id):
        p = (i - 1) in occupied
        c = i in occupied
        n = (i + 1) in occupied
        print(f"{i} - {p} - {c} - {n}") # ```grep "True - False - True"```
    """

    my_seat_id = -1
    for i in range(max_id):
        if not (i in occupied):
            if ((i - 1 in occupied)) and ((i + 1) in occupied):
                # print(f"{i} has no surroundings")
                my_seat_id = i

    print(f"p1: {max_id}")
    print(f"p2: {my_seat_id}")

if __name__ == "__main__":
    main()
