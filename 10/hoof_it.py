import sys

VALID_HEADINGS=((-1,0), (0,1), (1,0), (0,-1))

class HoofIt:
    
    def __init__(self, topomap):
        self.topomap = topomap
        self.maxy = len(topomap)-1
        self.maxx = len(topomap[0])-1

    def within(self, pos):
        return (pos[0] >= 0 and pos[1] >= 0 and
                pos[0] <= self.maxy and pos[1] <= self.maxx)
    
    def getval(self, pos):
        return self.topomap[pos[0]][pos[1]]

    def _starting_positions(self):
        for y in range(self.maxy+1):
            for x in range(self.maxx+1):
                if self.topomap[y][x] == 0:
                    yield (y, x)
         
    def _climb_up(self, pos, start_pos):
        val = self.getval(pos)
        if val == 9:
            yield (start_pos, pos)
            return
        for heading in VALID_HEADINGS:
            next_pos = (pos[0] + heading[0], pos[1] + heading[1])
            if self.within(next_pos) and self.getval(next_pos) == val + 1:
                    yield from self._climb_up(next_pos, start_pos)
        
    def count_trails(self, distinct_trails = True):  
        all_trails = [start_end_pair 
                      for startpos in self._starting_positions()
                      for start_end_pair in self._climb_up(startpos, startpos)]
        if distinct_trails:
            return len(set(all_trails))
        else:
            return len(all_trails)


if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else 'example_input.txt') as f:
        topomap = [list(map(lambda el: int(el), list(line[:-1]))) for line in f.readlines()]
    hoofit = HoofIt(topomap)
    print(f'Part 1: number of trail-detstination pairs {hoofit.count_trails()}')
    print(f'Part 2: number of all trails {hoofit.count_trails(False)}')    