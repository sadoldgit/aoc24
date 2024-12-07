import sys


class CeresSearch:

    search_paths=[]
    for y in range(-1,2):
        for x in range(-1,2):
            if x == y == 0:
                continue
            search_paths.append((y,x))

    def __init__(self, mem, word='XMAS'):
        self.mem = mem
        self.word = word
        self.maxx = len(mem[0]) - 1
        self.maxy = len(mem) - 1
        
    def xmas_count(self):
        cnt = 0
        for y in range(self.maxy + 1):
            for x in range(self.maxx + 1):
                if not self.mem[y][x] == self.word[0]:
                    continue
                for path in CeresSearch.search_paths:
                    cnt += self.search_word(self.word, y, x, path)
        return cnt

    def search_word(self, word, y, x, path):
        if not self.mem[y][x] == word[0]:
            return 0
        elif len(word) == 1:
            return 1
        new_y, new_x = y + path[0], x + path[1]
        if new_x < 0 or new_y < 0 or new_x > self.maxx or new_y > self.maxy:
            return 0
        return self.search_word(word[1:], new_y, new_x, path)

    
    def mas_count(self):
        cnt = 0
        for y in range(1, self.maxy):
            for x in range(1, self.maxx):
                if not self.mem[y][x] == 'A':
                    continue
                if not ((self.mem[y-1][x-1] == 'M' and self.mem[y+1][x+1] == 'S')
                    or (self.mem[y-1][x-1] == 'S' and self.mem[y+1][x+1] == 'M')):
                    continue
                if ((self.mem[y+1][x-1] == 'M' and self.mem[y-1][x+1] == 'S')
                    or((self.mem[y+1][x-1] == 'S' and self.mem[y-1][x+1] == 'M'))):
                    cnt += 1
        return cnt


if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else 'input.txt') as f:
        search = CeresSearch([list(line[:-1]) for line in f.readlines()])
    print(f'Part 1: XMAS count = {search.xmas_count()}')
    print(f'Part21: MAS count = {search.mas_count()}')
    
