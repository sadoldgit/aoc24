import sys

def op_permutations(n, basis=2, padlen=0):
    if n == 0:
        return '+' * padlen
    nums = []
    while n:
        n, r = divmod(n, basis)
        if r == 0:
            nums.append('+')
        elif r == 1:
            nums.append('*')
        else:
            nums.append('|')
    return ('+' * padlen + ''.join(reversed(nums)))[-padlen:]

class Calibration:

    def __init__(self, line):
        result, values = line.split(':')
        self.result = int(result)
        self.values = [int(value) for value in values.split()]
        
    def __repr__(self):
        return f'{self.result}: {self.values}'

    def valid_eq(self, allow_concatenations=False):
        """returns valid equation or None if calibration result can't be 
        calculated by any operator permutation"""

        opperm = []
        nr_ops = len(self.values)-1
        basis  = 3 if allow_concatenations else 2
        for i in range(basis**nr_ops):
            opperm.append(op_permutations(i, basis, nr_ops))

        for perm in opperm:
            result   = self.values[0]
            equation = str(result)
            for i in range(1,len(self.values)):
                if perm[i-1] == '+':
                    result += self.values[i]
                elif perm[i-1] == '*':
                    result *= self.values[i]
                else:
                    result = int(str(result)+str(self.values[i]))
                if result > self.result:
                    break
                equation += f' {perm[i-1]} {self.values[i]}'  
            if result == self.result:
                return f'{self.result}: {equation}'
        return None
        

def bridge_repair(lines):
    equations = [Calibration(line) for line in lines]
    result = sum([cal.result if cal.valid_eq(False) is not None
                  else 0 for cal in equations])
    print(f'Part 1: calibration result: {result}')
    result = sum([cal.result if cal.valid_eq(True) is not None
                  else 0 for cal in equations])
    print(f'Part 2: calibration with concatenations: {result}')
    return equations


if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else 'input.txt') as f:
        eq = bridge_repair(f.readlines())
