import re
import sys

def mul(a,b):
    return a*b

def mull_it_over(mem):
    result = eval('+'.join(re.findall('mul\([0-9]+\,[0-9]+\)', mem)))
    print(f'Part 1: mull={result}')
    result, fac = 0, 1
    for el in re.findall("mul\([0-9]+\,[0-9]+\)|do\(\)|don't\(\)", mem):
        if el == 'do()':
            fac = 1
        elif el == "don't()":
            fac = 0
        else:
            result += fac * eval(el)
    print(f'Part 2: mull={result}')


if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else 'input.txt') as f:
        mull_it_over(f.read())
