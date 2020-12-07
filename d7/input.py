#!/usr/bin/env python3

import re

def print_tree(t):
    for k, v in t.items():
        print(f"{k}:")
        if not len(v):
            print("\t- no other bags")
        for c, n in v.items():
            print(f"\t- {c} ({n})")

def parse_lines(lines):
    t = {}

    for line in lines:
        bb_color = line.split(" bags")[0]

        t[bb_color] = {}

        line = line.split("contain ")[1]
        line = line.replace("bags", "bag")
        line = line.replace(".", "")
        line = re.sub("$", ", ", line)

        # print(f"- {bb_color}")
        for sbags in line.split(" bag, "):
            if not sbags:
                continue

            split = sbags.split(" ")

            if split[0] == "no":
                # print(f"\tno other bags")
                break

            # print(f"\t - {sbags}")

            sb_color = " ".join(split[1:])
            sb_num = int(split[0])

            t[bb_color][sb_color] = sb_num

    return t

def find_all_that_contain(t, color):
    res = []

    for k, v in t.items():
        for c, _ in v.items():
            if c == color:
                res.append(k)

    return res

def rec(t, color, visited, matches):
    visited.add(color)
    matches.append(color)

    containers = find_all_that_contain(t, color)
    # print(f"{color} is in {containers}")
    for container in containers:
        if not (container in visited):
            rec(t, container, visited, matches)

def bfs(t):
    visited = set()
    matches = []

    sg_containers = find_all_that_contain(t, "shiny gold")

    for i in range(len(sg_containers)):
        # print(f"starting on `{sg_containers[i]}`")
        rec(t, sg_containers[i], visited, matches)

    return matches

def rec2(t, color):
    num_bags = 1

    # print(f"Starting for {color}")

    for c, n in t[color].items():
        # print(f"{color} in {c} ({n}x)")
        num_bags += n * rec2(t, c)

    # print(f"Ending for {color}: {num_bags}")

    return num_bags

def bfs2(t):
    total_bags = 0

    # print(f"`shiny gold` contains {t['shiny gold'].keys()}")
    for c, n in t["shiny gold"].items():
        total_bags += n * rec2(t, c)

    return total_bags

def main():
    lines = None
    with open("input", "r") as fcontent:
        lines = [line for line in fcontent.read().split("\n") if line]

    t = parse_lines(lines)
    # print_tree(t)

    print(f"p1: {len(bfs(t))}")
    print(f"p2: {bfs2(t)}")

if __name__ == "__main__":
    main()
