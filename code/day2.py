import utils
import re

example = True

inputfile = utils.INPUT_DIR / "day2.txt"
if example:
    inputfile = utils.INPUT_DIR / "day2_example2.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

reports = []

for line in lines:
    reports.append([int(x) for x in line.split()])

N = len(reports)


def is_report_safe(report, part2=False):
    steps = set()
    for i in range(len(report)-1):
        step = report[i+1] - report[i]
        steps.add(step)

    # Part 1
    # A report is safe only if it has only steps of size 1, 2 and 3 (or a subset),
    # either all positive or all negative.
    # i.e. if one of the two conditions (mutually exclusive) is verified:
    # - there are only steps in {1, 2, 3}
    # - there are only steps in {-1, -2, -3}
    safe = steps.issubset({1,2,3}) or steps.issubset({-1,-2,-3})

    # Part 2
    if part2 and not safe:
        # Check if it could be safe by removing one of the numbers in the list
        # Brute force, check for any removal in every unsafe report
        for i in range(len(report)):
            if is_report_safe(report[:i]+report[i+1:]):
                return True

    return safe


def get_N_safe_reports(reports, part2=False):
    return sum([is_report_safe(report, part2) for report in reports])

print("Part 1, number of safe reports:", get_N_safe_reports(reports))
print("Part 2, number of safe reports:", get_N_safe_reports(reports, part2=True))

