#!/usr/bin/env python3

class Game:
    def __init__(self, starting_numbers):
        self.turn = 1
        self.starting_numbers = starting_numbers
        self.spoken_map = {}
        self.numbers_spoken = []

    def reset(self):
        self.turn = 1
        self.spoken_map = {}
        self.numbers_spoken = []

    def speak(self):
        if (self.turn - 1) < len(self.starting_numbers):
            num = self.starting_numbers[self.turn - 1]
            self.spoken_map[num] = [self.turn]

            # print(f"speaking {num}")
            self.numbers_spoken.append(num)
        else:
            last_spoken = self.numbers_spoken[-1]
            # print(f"last spoken: {last_spoken}")

            # if self.turn % 50000 == 0:
            #    print(f"{self.turn}")

            if len(self.spoken_map[last_spoken]) == 1:
                if 0 in self.spoken_map:
                    self.spoken_map[0].append(self.turn)
                else:
                    self.spoken_map[0] = [self.turn]
                self.spoken_map[0]

                # print(f"{self.turn}\tspeaking new:\t{0}")
                self.numbers_spoken.append(0)
            else:
                diff = self.spoken_map[last_spoken][-1] - self.spoken_map[last_spoken][-2]

                if diff in self.spoken_map:
                    self.spoken_map[diff].append(self.turn)
                else:
                    self.spoken_map[diff] = [self.turn]

                # print(f"{self.turn}\tspeaking diff:\t{diff}")
                self.numbers_spoken.append(diff)

    def play(self, part="p1"):
        self.reset()

        limit = 2020 if part == "p1" else 30000000
        while len(self.numbers_spoken) < limit:
            self.speak()
            self.turn += 1

        return self.numbers_spoken[-1]

def main():
    starting_numbers = None

    with open("input", "r") as fcontent:
        starting_numbers = [int(n) for n in fcontent.read().split("\n")[0].split(",") if n]

    game = Game(starting_numbers)
    print(f"p1: {game.play()}")
    print(f"p2: {game.play('p2')}")

if __name__ == "__main__":
    main()
