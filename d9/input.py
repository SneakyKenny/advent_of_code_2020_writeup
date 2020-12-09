#!/usr/bin/env python3

def number_is_sum(num, r1, r2, numbers):
    for i in range(r1, r2):
        for j in range(i, r2):
            if num == (numbers[i] + numbers[j]):
                return True
    return False

def find_first_invalid(numbers):
    # print(numbers)
    delta = 25
    r1 = 0
    r2 = r1 + delta

    for i in range(r2, len(numbers) - delta):
        if number_is_sum(numbers[i], r1, r2, numbers):
            r1 += 1
            r2 += 1
        else:
            return numbers[i], r1, r2

    # no match
    return -1, -1, -1

def find_weakness(numbers):
    first_invalid, r1, r2 = find_first_invalid(numbers)

    set_size = 2

    while True:
        # maybe break at some point...

        for i in range(r2):
            s = 0
            for j in range(set_size):
                s += numbers[i + j]
            if s == first_invalid:
                return numbers[i : i + set_size]

        set_size += 1


def main():
    number_list = None
    with open("input", "r") as fcontent:
        number_list = [int(line) for line in fcontent.read().split("\n") if line]

    # print(f"first invalid: {find_first_invalid(number_list)}")
    first_invalid, _, _ = find_first_invalid(number_list)
    print(f"p1: {first_invalid}")

    s = find_weakness(number_list)
    print(f"p2: {min(s) + max(s)}")

if __name__ == "__main__":
    main()
