import sys

class GardenPlot:

    def __init__(self, plant, *parts):
        self.plant = plant
        self.parts = set(parts)

    def add_parts(self, *parts):
        for part in parts:
            self.parts.add(part)

    def merge(self, other):
        self.add_parts(*other.parts)

    @property
    def area(self):
        return len(self.parts)

    def __repr__(self):
        # miny = min(part[0] for part in self.parts)
        maxy = max(part[0] for part in self.parts)
        # minx = min(part[1] for part in self.parts)
        maxx = max(part[1] for part in self.parts)        
        rows = []
        for y in range(maxy+1):
            row = []
            for x in range(maxx+1):
                if (y, x) in self.parts:
                   row.append(self.plant)
                else:
                   row.append('.')
            rows.append(row)
        return '\n'.join(''.join(row) for row in rows)


class Garden:

    def __init__(self, garden):
        self.garden = garden
        self.maxx = len(garden[0]) - 1
        self.maxy = len(garden) - 1
        self.plots = []
        self._extract_plots()

    def _within(self, part):
        return (part[0] >= 0 and part[0] <= self.maxy
                and part[1] >= 0 and part[1] <= self.maxx)

    def _find_plot(self, plant, part):
        if not self._within(part):
            return None
        for plot in self.plots:
            if plot.plant != plant:
                continue
            if part in plot.parts:
                return plot
        return None

    def _extract_plots(self):
        # scan rows from up to down
        for y in range(len(self.garden)):
            plot = None
            x = 0
            while x <= self.maxx:
                plant = self.garden[y][x]
                upper_plots = set()
                plant_row = []
                # collect until new plant or end of row
                while x <= self.maxx and self.garden[y][x] == plant:
                    plant_row.append((y, x))
                    # possibly join with the same plant, already in some upper plot
                    upper_plots.add(self._find_plot(plant, (y-1, x)))
                    x += 1
                if None in upper_plots:
                    upper_plots.remove(None)
                # all upper plots joined with this row can be merged
                if len(upper_plots) > 0:
                    it_plots = iter(upper_plots)
                    to_plot = next(it_plots)
                    from_plot = next(it_plots, None)
                    while from_plot is not None:
                        to_plot.merge(from_plot)
                        self.plots.remove(from_plot)
                        from_plot = next(it_plots, None)
                    to_plot.add_parts(*plant_row)
                else:
                    plot = GardenPlot(plant, *plant_row)
                    self.plots.append(plot)

    NEIGHBORS = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    def _is_boundary(self, plot, part, calc_nbr):
        nbr = (part[0] + calc_nbr[0], part[1] + calc_nbr[1])
        if not self._within(nbr) or self.garden[nbr[0]][nbr[1]] != plot.plant:
            return True
        return False
    
    def perimeter(self, plot: GardenPlot):
        perimeter = 0
        for part in plot.parts:
            for calc_nbr in Garden.NEIGHBORS:
                if self._is_boundary(plot, part, calc_nbr):
                    perimeter += 1
        return perimeter
    
    def _inline_parts(self, plot, part, calc_nbr):
        # yield all plot parts that are inline with the given part
        # according to the neighbor calculation
        if calc_nbr[0] < 0 or calc_nbr[0] > 0:
            inc = ((0, -1), (0, 1))
        else:
            inc = ((-1, 0), (1, 0))
        side_1 = (part[0] + inc[0][0], part[1] + inc[0][1])
        side_2 = (part[0] + inc[1][0], part[1] + inc[1][1])
        stop_1, stop_2 = False, False
        while not (stop_1 and stop_2):
            if (not stop_1 and self._within(side_1)
                and self.garden[side_1[0]][side_1[1]] == plot.plant
                and self._is_boundary(plot, side_1, calc_nbr)):
                    yield side_1
                    side_1 = (side_1[0] + inc[0][0], side_1[1] + inc[0][1])
            else:
                stop_1 = True
            if (self._within(side_2)
                and self.garden[side_2[0]][side_2[1]] == plot.plant
                and self._is_boundary(plot, side_2, calc_nbr)):
                    yield side_2
                    side_2 = (side_2[0] + inc[1][0], side_2[1] + inc[1][1])
            else:
                stop_2 = True

    def perimeter2(self, plot: GardenPlot):
        perimeter = 0
        exclude_parts = set()
        used_parts = set()
        for part in plot.parts:
            for calc_nbr in Garden.NEIGHBORS:
                if (part, calc_nbr) in exclude_parts:
                    continue
                if self._is_boundary(plot, part, calc_nbr):
                    used_parts.add((part, calc_nbr))
                    perimeter += 1
                    # try lef-right or up-down if this is the same line
                    for exclude_part in self._inline_parts(plot, part, calc_nbr):
                        exclude_parts.add((exclude_part, calc_nbr))
        return perimeter


if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else 'input.txt') as f:
        garden = Garden([list(line[:-1]) for line in f.readlines()])
    price = sum([plot.area * garden.perimeter(plot) for plot in garden.plots])
    print(f'Part 1: total fencing price: {price}')

    price = sum([plot.area * garden.perimeter2(plot) for plot in garden.plots])
    print(f'Part 2: total discount fencing price: {price}')