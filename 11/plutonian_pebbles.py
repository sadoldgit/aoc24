import datetime
import math
import sys

cache = {}

def blink(pebble, blink_count):
    if blink_count == 0:
        return 1
    elif pebble == 0:
        val = blink(1, blink_count-1)
        cache[(pebble, blink_count)] = val
        print(f'Cache hit on {blink_count}')
        return val
    # check if already calculated
    cached_val = cache.get((pebble, blink_count), None)
    if cached_val is not None:
        return cached_val
    # no luck, use next two rules and cache the result
    digits = math.trunc(math.log10(pebble)) + 1
    if digits % 2 == 0:
        split = math.trunc(math.pow(10, digits//2))      
        val = blink(pebble // split, blink_count - 1) + \
            blink(pebble % split, blink_count - 1)
        cache[(pebble, blink_count)] = val
        return val
    else:
        val = blink(pebble*2024, blink_count - 1)
        cache[(pebble, blink_count)] = val
        return val
               

if __name__ == '__main__':
    nr_blinks = 75
    with open(sys.argv[1] if len(sys.argv) > 1 else 'input.txt') as f:
        pebbles = [int(num) for num in f.read().split()]
    start = datetime.datetime.now()
    cnt = sum([blink(pebble, nr_blinks) for pebble in pebbles])
    end = datetime.datetime.now()
    print(f'Number of pebbles after {nr_blinks} blinks = {cnt}. Calc time: {str(end-start)}')
    print('Cache:', len(cache))
