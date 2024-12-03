import utils
import re

example = False

inputfile = utils.INPUT_DIR / "day3.txt"
if example:
    inputfile = utils.INPUT_DIR / "day3_example_part2.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

pattern = r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)'

sum_part1 = 0
sum_part2 = 0
enabled = True

for line in lines:
    
    for x in re.findall(pattern, line):
        if x[0:3] == "mul":
            a, b = map(int, re.findall(r'\d+', x))
            sum_part1 += a * b
            if enabled:
                sum_part2 += a * b
        elif x == "do()":
            enabled = True
        elif x == "don't()":
            enabled = False
        else:
            print("SHOULD NOT HAPPEN")


print("Part 1, sum:", sum_part1)
print("Part 2, sum:", sum_part2)

