import sys

# directions
NORTH = 0
EAST  = 1
SOUTH = 2
WEST  = 3
# y,x
MOVE={NORTH:(-1,0), EAST:(0,1), SOUTH:(1,0), WEST:(0,-1)}

class DicOList(dict):
    "dictionary of lists with unique elements"
    
    def try_add(self, k, v):
        if not k in self:
            self[k] = [v]
            added = True
        else:
            if v in self[k]:
                added = False
            else:
                self[k].append(v)
                added = True
        return added

class GuardGallivant:

    def __init__(self, guard_map):
        self.guard_map = guard_map
        self.maxy = len(guard_map)-1
        self.maxx = len(guard_map[0])-1

    def _locate_guard(self):
        for y in range(self.maxy+1):
            for x in range(self.maxx+1):
                if self.guard_map[y][x] == '^':
                    return [y, x]
        
    def map_coverage(self):
        position = self._locate_guard()
        heading  = NORTH
        path     = DicOList()
        stepcnt  = 0
        while True:
            path.try_add((position[0], position[1]), (heading, stepcnt))
            new_y = position[0] + MOVE[heading][0]
            new_x = position[1] + MOVE[heading][1]
            if new_x < 0 or new_y < 0 or new_x > self.maxx or new_y > self.maxy:
                break
            if self.guard_map[new_y][new_x] == '#':
                # turn clockwise
                heading = (heading + 1) % 4
            position[0] = position[0] + MOVE[heading][0]
            position[1] = position[1] + MOVE[heading][1]
            stepcnt += 1
        return path
    
    def obstruction_positions(self, path):
        # interesting places on the path are the ones which would return
        # the guard on the already throden path -> crossroads
        crossroads = [k for k, v in guard_path.items() if len(v) > 1]
        for croad in crossroads:
            for heading, stepcnt in path[croad]:
                wouldturn = (heading + 1) % 4
                if any(filter(lambda other: other[0] == wouldturn
                       and other[1] < stepcnt, path[croad])):
                    new_y = croad[0] + MOVE[heading][0]
                    new_x = croad[1] + MOVE[heading][1]
                    yield (new_y, new_x)


if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else 'input.txt') as f:
        guard_map = [list(line[:-1]) for line in f.readlines()]
    gg = GuardGallivant(guard_map)
    guard_path = gg.map_coverage()
    print(f'Part 1: covered positions {len(guard_path.keys())}')
    obstructions = set(gg.obstruction_positions(guard_path))
    print(f'Part 2: number of obstruction positions {len(obstructions)}')