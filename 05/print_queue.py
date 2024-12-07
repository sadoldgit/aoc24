import sys
from functools import cmp_to_key

class PrintQueue:

    def __init__(self, rules, pages):
        self.rules = rules
        self.pages = pages
        # use available sorted algorithm but provide our sorting key
        # solution for sorted which does not accept function with 
        # two parameters, returning -1,0,1, therefore cmp_to_key
        self.sort_key_fn=cmp_to_key(self.page_ordering)
        
    def page_ordering(self, x, y):
        if [y,x] in self.rules:
            ret = 1
        elif [x,y] in self.rules:
            ret = -1
        else:
            ret = 0
        return ret
    
    def sum_pages(self, sum_correct=True):
        sum_middle = 0
        for page in self.pages:
            expected = sorted(page, key=self.sort_key_fn)
            if page == expected:
                if sum_correct:
                    sum_middle += page[len(page)//2]
            elif not sum_correct:
                sum_middle += expected[len(expected)//2]
        return sum_middle

if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else 'input.txt') as f:
        rules = []
        pages = []
        for line in f.readlines():
            if line.find('|') >= 0:
                rules.append(list(map(lambda rule: int(rule), line.rstrip().split('|'))))
            elif line.find(',') >=0:
                pages.append([int(page) for page in line.rstrip().split(',')])    
    queue = PrintQueue(rules, pages)
    print(f'Part 1: sum already correctly ordered: {queue.sum_pages()}')
    print(f'Part 2: sum incorrect correctly ordered: {queue.sum_pages(False)}')
    
