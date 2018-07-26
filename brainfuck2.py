from collections import namedtuple
from abc import ABC, abstractmethod
import numpy as np
import time
import sys
import argparse

debug = False
MAXSIZE = 8192
ptr = MAXSIZE // 2
mem = np.zeros(MAXSIZE, dtype=int)
code = []
pc = 0

# Intermediate representation

# Base Classes 
class Token(ABC):
    @abstractmethod
    def run(self):
        pass

class ValToken(Token):
    def __init__(self, value):
        self.value = value

# Tokens
class AddToken(ValToken):
    def run(self):
        global mem, ptr
        mem[ptr] += self.value
    def __repr__(self):
        return "+ " + str(self.value)

class SubToken(ValToken):
    def run(self):
        mem[ptr] -= self.value
    def __repr__(self):
        return "- " + str(self.value)

class RightToken(ValToken):
    def run(self):
        global ptr
        ptr += self.value
    def __repr__(self):
        return "> " + str(self.value)

class LeftToken(ValToken):
    def run(self):
        global ptr
        ptr -= self.value
    def __repr__(self):
        return "< " + str(self.value)

class PrintToken(Token):
    def run(self):
        print(chr(mem[ptr]), end='')
    def __repr__(self):
        return "."

class InToken(ValToken):
    def run(self):
        mem[ptr] = ord(input()[:self.val])
    def __repr__(self):
        return "."


class OpenToken(Token):
    def __init__(self):
        self.match = None

    def find_match(self):
        layer = 0
        for i in range(code.index(self) + 1, len(code)):
            if isinstance(code[i], CloseToken):
                if layer == 0:
                    return i
                else:
                    layer -= 1
            elif isinstance(code[i], OpenToken):
                layer += 1

    def run(self):
        global pc
        if not mem[ptr]:
            if not self.match:
                self.match = self.find_match()
            pc = self.match

    def __repr__(self):
        return "["

class CloseToken(Token):
    def __init__(self):
        self.match = None

    def find_match(self):
        layer = 0
        for i in range(code.index(self) - 1, -1, -1):
            if isinstance(code[i], OpenToken):
                if layer == 0:
                    return i
                else:
                    layer -= 1
            elif isinstance(code[i], CloseToken):
                layer += 1 

    def run(self):
        global pc 
        if mem[ptr]:
            if not self.match:
                self.match = self.find_match()
            pc = self.match
            
    def __repr__(self):
        return "]"

class ClearToken(Token):
    def run(self):
        mem[ptr] = 0
    def __repr__(self):
        return "CLR"

class ScanToken(Token):
    def __init__(self, direction, value):
        self.direction = direction
        self.value = value

    def run(self):
        global mem, ptr

        if self.direction == 'L':
            while mem[ptr]:
                ptr -= self.value

        elif self.direction == 'R':
            while mem[ptr]:
                ptr += self.value

    def __repr__(self):
        return "SCN {0}: {1}".format(self.direction, self.value)

class CopyToken(Token):

# Converting into the intermdiate representation
def build_brainfuck(code_string):
    for char in code_string:
        if char == '+': code.append(AddToken(1))
        elif char == '-': code.append(SubToken(1))
        elif char == '<': code.append(LeftToken(1))
        elif char == '>': code.append(RightToken(1))
        elif char == '.': code.append(PrintToken())
        elif char == ',': code.append(InToken())
        elif char == '[': code.append(OpenToken())
        elif char == ']': code.append(CloseToken())

# Optimizations
def optimize_brainfuck():
    accumulate_optimization()
    loop_optimizations()

def accumulate_optimization():
    global code
    new_code = [code.pop(0)]

    while code:
        instruction = code.pop(0)
        last_instruction = new_code[-1]
        if (isinstance(last_instruction, AddToken) 
                and isinstance(instruction, AddToken)):
            new_code[-1] = AddToken(last_instruction.value + 1)

        elif (isinstance(last_instruction, SubToken) 
                and isinstance(instruction, SubToken)):
            new_code[-1] = SubToken(last_instruction.value + 1)

        elif (isinstance(last_instruction, RightToken) 
                and isinstance(instruction, RightToken)):
            new_code[-1] = RightToken(last_instruction.value + 1)

        elif (isinstance(last_instruction, LeftToken) 
                and isinstance(instruction, LeftToken)):
            new_code[-1] = LeftToken(last_instruction.value + 1)

        else:
            new_code.append(instruction)

    code = new_code

def loop_optimizations():
    global code

    i = 0
    while i < len(code) - 2:
        if (isinstance(code[i], OpenToken) and
            isinstance(code[i + 2], CloseToken)):

            found = False
            if isinstance(code[i + 1], SubToken):
                code[i] = ClearToken()
                found = True
            elif isinstance(code[i + 1], RightToken):
                code[i] = ScanToken('R', code[i + 1].value)
                print('fuck')
                found = True
            elif isinstance(code[i + 1], LeftToken):
                code[i] = ScanToken('L', code[i + 1].value)
                found = True
#
            if found:
                code.pop(i+2)
                code.pop(i+1)
        i += 1

def copy_optimization():
    global code

    while i < len(code):
        if (isintance(code[i], OpenToken)):
            movement = net_movement(i)
            if movement == 0 and \
                    (isinstance(code[i+1]
                
        i += 1

def net_movement(start_of_block):
    global code
    
    net_right = 0
    for i in range(start_of_block, code[start_of_block].find_match()):
        if isinstance(code[i], RightToken):
            net_right += code[i].value
        if isinstance(code[i], LeftToken):
            net_right -= code[i].value
    return net_right



def run_brainfuck():
    global pc
    try:
        print(code)
        while True:
            cur_instruction = code[pc]
    #        print(cur_instruction)
            cur_instruction.run()
            pc += 1
    except IndexError:
        print("\nDone")


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='location of a brainfuck source file')
    parser.add_argument('-d', '--debug', help='debug mode', action='store_true')
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    with open(args.filename) as f:
        cmd = f.read()

    build_brainfuck(cmd)
    optimize_brainfuck()
    if debug: print(code)
    a = time.time()
    run_brainfuck()
    print(time.time() - a)
    if debug: print(mem)

if __name__ == '__main__':
    main()
