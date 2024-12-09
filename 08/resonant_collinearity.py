import sys

class Cartesian:
    
    @staticmethod
    def create(leny, lenx, fill_value='.'):
        vals = []
        for i in range(leny):
            vals.append([fill_value]*lenx)
        return Cartesian(vals)

    def __init__(self, values):
        """values: 2D matrix in a list of lists form
        coordinates: y=0 at the top, x=0 at the most left
        """
        self.values = values
        self.maxy = len(values)-1
        self.maxx = 0 if len(values) == 0 else len(values[0])-1

    def setval(self, y, x, value):
        self.values[y][x] = value
        
    def getval(self, y, x):
        return self.values[y][x]
    
    def iterate(self):
        for y in range(self.maxy+1):
            for x in range(self.maxx+1):
                yield (y,x,self.values[y][x])
    
    def within(self, coords):
        return (coords[0] >= 0 and coords[0] <= self.maxy
                and coords[1] >= 0 and coords[1] <= self.maxx)

    def __repr__(self):
        return '\n'.join(''.join(row) for row in self.values)    
      

class ResonantCollinearity:

    def __init__(self, city):
        self.city = Cartesian(city)
        self.antennas = self.locate_antennas()

    def locate_antennas(self):
        result = {}
        for y,x,val in self.city.iterate():
            if val.isalnum():
                if val in result:
                    result[val].append((y,x))
                else:
                    result[val]=[(y,x)]
        return result

    @property
    def antenna_pairs(self):
        for atype, locations in self.antennas.items():
            for i in range(len(locations)):
                for j in range(i+1, len(locations)):
                    yield atype, locations[i], locations[j]

    @property  
    def antinodes(self):
        for atype, a1, a2 in self.antenna_pairs:
            disty = a1[0] - a2[0]
            distx = a1[1] - a2[1]
            node = (a1[0] + disty, a1[1] + distx)
            if self.city.within(node) and self.city.getval(node[0],node[1]) != atype:
                yield node[0], node[1]
            node = (a1[0] -2 * disty, a1[1] -2 * distx)
            if self.city.within(node) and self.city.getval(node[0],node[1]) != atype:
                yield node[0], node[1]

    @property  
    def antinodes2(self):
        # antinodes are all equidistant points on the line through the antena pair
        for atype, a1, a2 in self.antenna_pairs:
            disty = a1[0] - a2[0]
            distx = a1[1] - a2[1]
            slope = 1 if (disty >= 0 and distx >= 0) or (disty < 0 and distx < 0) else -1
            # a bit of of overhead for testing if calculated point is inside city boundary
            test = max(self.city.maxx, self.city.maxy)
            for i in range(-1*test, test):
                node = (a1[0] + slope * i * abs(disty), a1[1] + i * abs(distx))
                if self.city.within(node):
                    yield node[0], node[1]

    def __repr__(self):
        return str(self.city) + '\n' \
            + str(self.antennas)


def print_anode_map(size_y, size_x, anodes, fill_value='#'):
    anode_map = Cartesian.create(size_y, size_x, '.')
    for loc in anode_locs:
        anode_map.setval(loc[0], loc[1], fill_value)
    print(anode_map)


if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else 'input.txt') as f:
        city = [list(line[:-1]) for line in f.readlines()]        
    resonance = ResonantCollinearity(city)
    anode_locs = set((a[0], a[1]) for a in resonance.antinodes)
    print(f'Part 1: unique antinode locations: {len(anode_locs)}')
    #print_anode_map(resonance.city.maxy+1, resonance.city.maxx+1, anode_locs)
    anode_locs = set((a[0], a[1]) for a in resonance.antinodes2)
    print(f'Part 2: antinode locations for any grid position: {len(anode_locs)}')
    #print_anode_map(resonance.city.maxy+1, resonance.city.maxx+1, anode_locs)