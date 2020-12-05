#!/usr/bin/env python3

def parse_line(line):
    dash_split = line.split("-")
    num1 = int(dash_split[0])
    num2 = int(dash_split[1].split(" ")[0])
    c = dash_split[1].split(" ")[1].split(":")[0]
    s = line.split(" ")[-1]

    return num1, num2, c, s

def is_valid(line, policy="1"):
    """
    "<num1>-<num2> <char>: <string>"
    """
    num1, num2, c, s = parse_line(line)

    count = s.count(c)

    if policy == "1":
        return count >= num1 and count <= num2
    return (s[num1 - 1] == c or s[num2 - 1] == c) and s[num1 - 1] != s[num2 - 1]

def main():
    content = None
    with open("input", "r") as fcontent:
        content = fcontent.read()

    p1_valid = 0
    p2_valid = 0

    for l in content.split('\n'):
        if not l:
            continue
        p1_valid += 1 if is_valid(l, policy="1") else 0
        p2_valid += 1 if is_valid(l, policy="2") else 0

    print(f"p1: {p1_valid}")
    print(f"p2: {p2_valid}")

if __name__ == "__main__":
    main()
