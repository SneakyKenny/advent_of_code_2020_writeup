#!/usr/bin/env python3

def parse_lines(lines):
    obj = {
        "rules": {},
        "ticket": [],
        "nearby": []
    }

    line_index = 0

    for line in lines:
        if not line:
            break
        split = line.split(": ")
        rule_name = split[0]
        rule_ranges_str = split[1].split(" or ")
        rule_ranges = []
        for r in rule_ranges_str:
            s, e = r.split("-")
            rule_ranges.append((int(s), int(e)))

        obj["rules"][rule_name] = rule_ranges
        line_index += 1

    line_index += 2

    obj["ticket"] = [int(num) for num in lines[line_index].split(",")]

    line_index += 3

    for i in range(line_index, len(lines)):
        if not lines[i]:
            continue
        obj["nearby"].append([int(num) for num in lines[i].split(",")])

    return obj

def is_num_in_rules(obj, num):
    for rule in obj["rules"].values():
        for rrange in rule:
            if num >= rrange[0] and num <= rrange[1]:
                return True

    return False

def solve_part_one(obj):
    invalid = []

    for index, ticket in enumerate(obj["nearby"]):
        for num in ticket:
            if not is_num_in_rules(obj, num):
                invalid.append((num, index))

    s = 0

    for num, _ in invalid:
        s += num

    return s, invalid

def discard_invalid(obj):
    _, invalid = solve_part_one(obj)

    for num, _ in invalid:
        for index, ticket in enumerate(obj["nearby"]):
            if num in ticket:
                obj["nearby"].pop(index)

def is_number_in_range(obj, rule, num):
    obj_rule = obj["rules"][rule]
    for rrange in obj_rule:
        if num >= rrange[0] and num <= rrange[1]:
            return True

    return False

def get_possibilities(obj):
    possibilities = []
    for _ in range(len(obj["rules"].keys())):
        possibilities.append([[k, True] for k in obj["rules"].keys()])

    for ticket in obj["nearby"]:
        for index, num in enumerate(ticket):
            if not possibilities[index][1]:
                continue

            for i, p in enumerate(possibilities[index]):
                if not is_number_in_range(obj, p[0], num):
                    possibilities[index][i][1] = False

    return possibilities

def result_filled(result):
    for r in result:
        if r is None:
            return False

    return True

def all_zeroes(sums):
    for s in sums:
        if s:
            return False

    return True

def get_possibilities_count(possibilities):
    sums = [0 for _ in range(len(possibilities))]

    for i in range(len(possibilities)):
        for j in range(len(possibilities[i])):
            if possibilities[i][j][1]:
                sums[j] += 1

    return sums

def solve_part_two(obj):
    discard_invalid(obj)

    possibilities = get_possibilities(obj)

    """
    print('\n')
    for p in possibilities:
        print(p)
    print('\n')
    """

    result = [None for _ in range(len(possibilities))]

    sums = get_possibilities_count(possibilities)
    # TODO: Refactor that piece of sh*t
    while not all_zeroes(sums):
        found = False
        for i in range(len(sums)):
            if found:
                break
            if sums[i] == 1:
                # print(f"found sum == 1 at i = {i}")
                for j in range(len(possibilities)):
                    if possibilities[j][i][1]:
                        # print(f"found associated possibility: {possibilities[j][i][0]} at index {j}")
                        result[j] = possibilities[j][i][0]
                        for k in range(len(possibilities[j])):
                            possibilities[j][k][1] = False

                        sums = get_possibilities_count(possibilities)

                        found = True
                        break
                    if found:
                        break
                if found:
                    break
            if found:
                break

    p = 1

    for i in range(len(result)):
        if result[i].startswith("departure"):
            p *= obj["ticket"][i]

    return p

def main():
    obj = None
    with open("input", "r") as fcontent:
        lines = [line for line in fcontent.read().split("\n")]
        obj = parse_lines(lines)

    # print(obj)

    print(f"p1: {solve_part_one(obj)[0]}")
    print(f"p2: {solve_part_two(obj)}")

if __name__ == "__main__":
    main()
