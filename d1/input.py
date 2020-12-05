#!/usr/bin/env python3

def find_pair(values, target):
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] + values[j] == target:
                return values[i], values[j]
    return None

def find_trio(values, target):
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            for k in range(len(values)):
                if values[i] + values[j] + values[k] == target:
                    return values[i], values[j], values[k]
    return None

def main():
    with open("input", "r") as fcontent:
        content = fcontent.read()
    values = [int(l) for l in content.split("\n") if l]

    n1, n2 = find_pair(values, 2020)
    print(f"p1: {n1 * n2}")
    n1, n2, n3 = find_trio(values, 2020)
    print(f"p2: {n1 * n2 * n3}")

if __name__ == "__main__":
    main()
