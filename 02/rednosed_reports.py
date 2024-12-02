import sys

def is_safe(report, tolerate_one=False):
    difs = [report[i+1] - report[i]
            for i in range(len(report)-1)]
    mindif = min(difs)
    maxdif = max(difs)
    safe = mindif * maxdif > 0
    if safe:
        if mindif < 0:
            safe = mindif >= -3 and maxdif <= -1
        else:
            safe = mindif >= 1 and maxdif <=3
    if not safe and tolerate_one:
        # try with single level removal
        for i in range(len(report)):
            safe = safe or is_safe(report[:i] + report[i+1:])
            if safe:
                break
    return safe

def rednosed_reports(reports):
    nr_safe = sum([1 if is_safe(report) else 0 for report in reports])
    print(f'Part 1: safe reports = {nr_safe}')
    nr_safe = sum([1 if is_safe(report, True) else 0 for report in reports])
    print(f'Part 2: safe reports with single bad allowed = {nr_safe}')

if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else 'input.txt') as f:
        rednosed_reports([[int(level) for level in line.split()]
                          for line in f.readlines()])
