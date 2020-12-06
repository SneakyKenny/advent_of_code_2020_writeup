#!/usr/bin/env python3

def parse_person(line):
    person = set()

    for c in line:
        person.add(c)

    return person

def parse_groups(lines):
    groups = []

    group = []
    for line in lines:
        if not line:
            groups.append(group)
            group = []
        else:
            person = parse_person(line)
            group.append(person)

    return groups

def reduce_group_answers_any(group):
    answers = set()

    for person in group:
        for answer in person:
            answers.add(answer)

    return answers

def reduce_group_answers_all(group):
    answers = dict()

    for person in group:
        for answer in person:
            if answer in answers:
                answers[answer] += 1
            else:
                answers[answer] = 1

    filtered_answers = []
    for answer, number in answers.items():
        if number == len(group):
            filtered_answers.append(answer)

    return filtered_answers

def main():
    lines = None
    with open("input", "r") as fcontent:
        lines = fcontent.read().split("\n")

    groups = parse_groups(lines)

    count_p1 = 0
    count_p2 = 0

    for group in groups:
        count_p1 += len(reduce_group_answers_any(group))
        count_p2 += len(reduce_group_answers_all(group))

    print(f"p1: {count_p1}")
    print(f"p2: {count_p2}")

if __name__ == "__main__":
    main()
