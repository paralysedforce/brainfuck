from __future__ import print_function
import sys

cmd = """
++++++++++ 10
[>
++++++++++ 10  >  h
++++++++++ 10  >  e
++++++++++ 10  >  l 
++++++++++ 10  >  l 
+++++++++++ 11 >  o
+++ >3 Space
+++++++++++ 11 >  w
+++++++++++ 11 >  o
+++++++++++ 11 >  r
++++++++++ 10  >  l 
++++++++++ 10  >  d 
<<<<< < <<<<< <-]

> ++++. 104=h
> +. 101=e
> ++++++++. 108=l
> ++++++++. 108=l
> +. 111=o
> ++.  32=Space
> +++++++++. 119=w
> +. 111=o
> ++++. 114=r
> ++++++++. 108=l
> . 100=d
"""

def brainfuck(cmd):
    tape = [0]
    pntr = 0
    pc = 0
#    pdb.set_trace()
    while pc < len(cmd):
        char = cmd[pc]
        if char == '+':
            tape[pntr] += 1
            pc += 1
            continue
        if char == '-':
            tape[pntr] -= 1
            pc += 1
            continue
        if char == '>':
            if pntr == len(tape) - 1:
                tape.append(0)
            pntr += 1
            pc += 1
            continue
        if char == '<':
            if pntr == 0:
                tape = [0] + tape
            else:
                pntr -= 1
            pc += 1
            continue
        if char == '.':
            print(chr(tape[pntr]), end = '')
            pc += 1
            continue
        if char == ',':
            tape[pntr] = ord(input()[0])
            pc += 1
            continue
        if char == '[':
            if tape[pntr] == 0:
                count = 0
                pc += 1
                while cmd[pc] != ']' or count != 0:
                    if cmd[pc] == '[': count += 1
                    if cmd[pc] == ']': count -= 1
                    pc += 1
            pc += 1
            continue
        if char == ']':
            #pdb.set_trace()
            if tape[pntr] != 0:
                count = 0
                pc -= 1
                while cmd[pc] != '[' or count != 0:
                    if cmd[pc] == ']': count += 1
                    if cmd[pc] == '[': count -= 1
                    pc -= 1
            pc += 1
            continue
        pc +=1
    return tape

def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            doc = f.read()
        print(brainfuck(doc))
    else:
        print(brainfuck(cmd))

if __name__ == '__main__':
    main()
