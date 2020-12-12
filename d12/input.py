#!/usr/bin/env python3

from enum import Enum

class MovementType(Enum):
    N = 1
    S = 2
    E = 3
    W = 4
    L = 5
    R = 6
    F = 7

class Movement:
    def __init__(self, m_type, m_value):
        self.m_type = m_type
        self.m_value = m_value

    def from_string(s):
        m_type = MovementType[s[0]]
        m_value = int(s[1:])
        return Movement(m_type, m_value)

    def __str__(self):
        return f"{self.m_type.name} - {self.m_value}"

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, o):
        self.x += o.x
        self.y += o.y
        return self

class Game:
    def __init__(self, moves):
        self.moves = moves
        self.current_move = 0
        self.position = Position(0, 0)
        self.direction = MovementType.E

    def __str__(self):
        return f"pos: {self.position}, dir: {self.direction}, move: {self.current_move}"

    def move_N(self, val):
        self.position.y += val

    def move_S(self, val):
        self.position.y -= val

    def move_E(self, val):
        self.position.x += val

    def move_W(self, val):
        self.position.x -= val

    def rotate_L(self, val):
        rotation_map = {
            MovementType.E: MovementType.N,
            MovementType.N: MovementType.W,
            MovementType.W: MovementType.S,
            MovementType.S: MovementType.E,
        }

        self.direction = rotation_map[self.direction]

    def rotate_R(self, val):
        rotation_map = {
            MovementType.E: MovementType.S,
            MovementType.S: MovementType.W,
            MovementType.W: MovementType.N,
            MovementType.N: MovementType.E,
        }

        self.direction = rotation_map[self.direction]

    def move_F(self, val):
        move_map = {
            MovementType.N: self.move_N,
            MovementType.S: self.move_S,
            MovementType.E: self.move_E,
            MovementType.W: self.move_W,
        }

        move_map[self.direction](val)

    def play_move(self):
        move = self.moves[self.current_move]

        move_map = {
            MovementType.N: self.move_N,
            MovementType.S: self.move_S,
            MovementType.E: self.move_E,
            MovementType.W: self.move_W,
            MovementType.L: self.rotate_L,
            MovementType.R: self.rotate_R,
            MovementType.F: self.move_F,
        }

        if move.m_type in [MovementType.L, MovementType.R]:
            for _ in range(move.m_value // 90):
                move_map[move.m_type](move.m_value)
        else:
            move_map[move.m_type](move.m_value)

        self.current_move += 1

    def play(self):
        self.current_move = 0
        self.position = Position(0, 0)
        self.direction = MovementType.E

        while self.current_move < len(self.moves):
            self.play_move()

        return abs(self.position.x) + abs(self.position.y)

class NewGame:
    def __init__(self, moves):
        self.moves = moves
        self.current_move = 0
        self.position = Position(0, 0)
        self.direction = MovementType.E
        self.waypoint = Position(10, 1)

    def __str__(self):
        return f"pos: {self.position}, waypoint: {self.waypoint}, dir: {self.direction}, move: {self.current_move}"

    def move_N(self, val):
        self.waypoint.y += val

    def move_S(self, val):
        self.waypoint.y -= val

    def move_E(self, val):
        self.waypoint.x += val

    def move_W(self, val):
        self.waypoint.x -= val

    def rotate_L(self, val):
        self.waypoint = Position(-self.waypoint.y, self.waypoint.x)

    def rotate_R(self, val):
        self.waypoint = Position(self.waypoint.y, -self.waypoint.x)

    def move_F(self, val):
        for _ in range(val):
            self.position = self.position + self.waypoint

    def play_move(self):
        move = self.moves[self.current_move]

        move_map = {
            MovementType.N: self.move_N,
            MovementType.S: self.move_S,
            MovementType.E: self.move_E,
            MovementType.W: self.move_W,
            MovementType.L: self.rotate_L,
            MovementType.R: self.rotate_R,
            MovementType.F: self.move_F,
        }

        if move.m_type in [MovementType.L, MovementType.R]:
            for _ in range(move.m_value // 90):
                move_map[move.m_type](move.m_value)
        else:
            move_map[move.m_type](move.m_value)

        self.current_move += 1

    def play(self):
        self.current_move = 0
        self.position = Position(0, 0)
        self.direction = MovementType.E
        self.waypoint = Position(10, 1)

        while self.current_move < len(self.moves):
            self.play_move()

        return abs(self.position.x) + abs(self.position.y)


def main():
    lines = None
    with open("input", "r") as fcontent:
        lines = [line for line in fcontent.read().split("\n") if line]

    # print(lines)
    moves = [Movement.from_string(s) for s in lines]

    game = Game(moves)
    print(f"p1: {game.play()}")

    new_game = NewGame(moves)
    print(f"p2: {new_game.play()}")

if __name__ == "__main__":
    main()
