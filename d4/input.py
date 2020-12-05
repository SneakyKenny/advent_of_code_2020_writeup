#!/usr/bin/env python3

import re

def is_valid(pwd):
    req_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

    for field in pwd.split(" "):
        try:
            req_fields.pop(req_fields.index(field.split(":")[0]))
        except:
            pass

    return len(req_fields) == 0

def is_valid_byr(v):
    n = int(v)
    return n >= 1920 and n <= 2002

def is_valid_iyr(v):
    n = int(v)
    return n >= 2010 and n <= 2020

def is_valid_eyr(v):
    n = int(v)
    return n >= 2020 and n <= 2030

def is_valid_hgt_cm(v):
    n = int(v)
    return n >= 150 and n <= 193

def is_valid_hgt_in(v):
    n = int(v)
    return n >= 59 and n <= 76

def is_valid_hgt(v):
    if "cm" in v:
        return is_valid_hgt_cm(v.split("cm")[0])
    if "in" in v:
        return is_valid_hgt_in(v.split("in")[0])
    return False

def is_hexa(v):
    c = ord(v)
    return (c >= ord("0") and c <= ord("9")) or (c >= ord("a") and c <= ord("f"))

def is_hexa_str(v):
    for c in v:
        if not is_hexa(c):
            return False
    return True

def is_valid_hcl(v):
    return v[0] == "#" and is_hexa_str(v.split("#")[1]) and len(v.split("#")[1]) == 6

def is_valid_ecl(v):
    return v in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

def is_num(v):
    c = ord(v)
    return c >= ord("0") and c <= ord("9")

def is_num_str(v):
    for c in v:
        if not is_num(c):
            return False
    return True

def is_valid_pid(v):
    return is_num_str(v) and len(v) == 9

def is_valid_cid(v):
    return True

def is_valid_p2(pwd):
    if not is_valid(pwd):
        return False

    test_fn = {
        "byr": is_valid_byr,
        "iyr": is_valid_iyr,
        "eyr": is_valid_eyr,
        "hgt": is_valid_hgt,
        "hcl": is_valid_hcl,
        "ecl": is_valid_ecl,
        "pid": is_valid_pid,
        "cid": is_valid_cid,
    }

    for field in pwd.split(" "):
        k, v = field.split(":")
        if not test_fn[k](v):
            # print(f"invalid {k}: {v}")
            return False
    return True

def main():
    lines = []
    with open("input", "r") as fcontent:
        r = fcontent.read()

        curr_pass = []

        for line in r.split("\n"):
            if not line:
                lines.append(' '.join(curr_pass))
                curr_pass = []
                continue
            curr_pass.append(line)

    p1_valid = 0
    p2_valid = 0

    for pwd in lines:
        p1_valid += 1 if is_valid(pwd) else 0
        p2_valid += 1 if is_valid_p2(pwd) else 0

    print(f"p1: {p1_valid}")
    print(f"p2: {p2_valid}")

if __name__ == "__main__":
    main()
