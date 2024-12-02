import sys
from itertools import groupby

def read_lists(fpath):
    ids = [int(locid) for locid in open(fpath).read().split()]
    list1 = sorted([ids[i*2]   for i in range(len(ids)//2)])
    list2 = sorted([ids[i*2+1] for i in range(len(ids)//2)])
    return list1, list2

def historian_hysteria(list1, list2):
    distance = sum([abs(list2[i] - list1[i]) for i in range(len(list1))])
    print(f'Part 1: distance = {distance}')
    list2_counts = {key: len(list(grp)) for key, grp in groupby(list2)}
    score = sum([idx * list2_counts.get(idx, 0) for idx in list1])
    print(f'Part 2: similarity score = {score}')

if __name__ == '__main__':
    historian_hysteria(*read_lists(sys.argv[1] if len(sys.argv) > 1 else 'input.txt'))