#!/usr/bin/env python3

def p1(t, b_ids):
    i = t
    while True:
        for b_id in b_ids:
            if i % b_id == 0:
                return i, b_id
        i += 1

def sp2(b_ids, index):
    offset = -1
    to_match = {}
    for b_id in b_ids:
        offset += 1

        if b_id == "x":
            continue

        to_match[offset] = b_id

    print(f"to_match: {to_match}")

    i = 0
    while True:
        ok = True
        for k, v in to_match.items():
            if (i + k) % v != 0:
                ok = False
                break
        if ok:
            return i

        i += 1

    return None

def p2(b_ids):
    # see solution in (rust)[https://github.com/ropewalker/advent_of_code_2020/blob/master/src/day13.rs]
    # see solution in (js)[https://johnbeech.github.io/advent-of-code-2020/solutions/day13/viewer.html]
    return None

def main():
    lines = None

    with open("input", "r") as fcontent:
        lines = [line for line in fcontent.read().split("\n") if line]

    # p1
    my_time = int(lines[0])
    bus_ids = [int(n) for n in lines[1].split(",") if n != "x"]

    t, bus_id = p1(my_time, bus_ids)
    print(f"p1: {(t - my_time) * bus_id}")

    # p2
    bus_ids = [int(n) if n != "x" else "x" for n in lines[1].split(",")]
    print(bus_ids)
    t = p2(bus_ids)
    print(f"p2: {t}")


if __name__ == "__main__":
    main()
