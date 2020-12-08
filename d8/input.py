#!/usr/bin/env python3

from enum import Enum

class InstructionType(Enum):
    ACC = 1
    JMP = 2
    NOP = 3

class ProgramInstruction:
    def __init__(self, s):
        self.instruction_type = InstructionType[s[:3].upper()]
        self.initial_type = self.instruction_type
        self.argument = int(s[4:])

    def switch(self):
        m = {
            InstructionType.ACC: InstructionType.ACC,
            InstructionType.JMP: InstructionType.NOP,
            InstructionType.NOP: InstructionType.JMP,
        }

        self.instruction_type = m[self.instruction_type]

    def restore(self):
        self.instruction_type = self.initial_type

class Program:
    pc: int = 0
    accumulator: int = 0
    instructions_run: list = []

    def __init__(self, instruction_list):
        self.instruction_list = instruction_list
        self.reset()

    def reset(self):
        self.pc = 0
        self.accumulator = 0
        self.instructions_run = [False for _ in range(len(self.instruction_list))]

    def __str__(self):
        s = f"pc: {self.pc} - acc: {self.accumulator}\n"
        for instruction in self.instruction_list:
            s += f"{instruction.instruction_type.name}\t{instruction.argument}"
            s += "\n" if instruction != self.instruction_list[-1] else ""
        return s

    def run_acc(self, arg, pc, acc):
        # print(f"running acc: pc is {pc}, acc is {acc}, arg is {arg}")
        acc += arg
        pc += 1

        return pc, acc

    def run_jmp(self, arg, pc, acc):
        # print(f"running jmp: pc is {pc}, acc is {acc}, arg is {arg}")
        pc += arg

        return pc, acc

    def run_nop(self, arg, pc, acc):
        # print(f"running nop: pc is {pc}, acc is {acc}, arg is {arg}")
        pc += 1
        return pc, acc

    def run_one_instruction(self):
        if self.pc >= len(self.instruction_list):
            # End of program
            return True

        instruction = self.instruction_list[self.pc]

        instruction_type = instruction.instruction_type
        argument = instruction.argument

        if self.instructions_run[self.pc] == True:
            return False

        self.instructions_run[self.pc] = True

        fn = {
            InstructionType.ACC: self.run_acc,
            InstructionType.JMP: self.run_jmp,
            InstructionType.NOP: self.run_nop,
        }

        self.pc, self.accumulator = fn[instruction_type](arg = argument,
                                                         pc = self.pc,
                                                         acc = self.accumulator)

        return True

    def run(self):
        self.reset()

        while False in self.instructions_run:
            res = self.run_one_instruction()

            if self.pc >= len(self.instruction_list):
                # End of program
                return True

            if not res:
                return False

        return True

    def fix(self):
        for i in range(len(self.instruction_list)):
            continue_if = [InstructionType.JMP, InstructionType.NOP]
            if not (self.instruction_list[i].instruction_type in continue_if):
                continue

            self.instruction_list[i].switch()

            if self.run() == True:
                # print(f"Successfully fixed the program: changed instruction #{i}")
                self.instruction_list[i].restore()
                return True

            self.instruction_list[i].restore()

        return False

def main():
    program = None

    with open("input", "r") as fcontent:
        lines = [line for line in fcontent.read().split("\n") if line]
        instruction_list = [ProgramInstruction(line) for line in lines]
        program = Program(instruction_list)

    # print(program)
    program.run()
    print(f"p1: {program.accumulator}")
    program.fix()
    print(f"p2: {program.accumulator}")

if __name__ == "__main__":
    main()
