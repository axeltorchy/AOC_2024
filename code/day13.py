import utils
import re
import numpy as np

example = False

inputfile = utils.INPUT_DIR / "day13.txt"
if example:
    inputfile = utils.INPUT_DIR / "day13_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

pattern_A = r'Button A: X\+(\d+), Y\+(\d+)'
pattern_B = r'Button B: X\+(\d+), Y\+(\d+)'
pattern_prize = r'Prize: X=(\d+), Y=(\d+)'

systems = []
results = []

# Parse input
system = [[], []]

for line in lines:
    matches = re.search(pattern_A, line)
    if matches:
        xa, ya = list(map(int, matches.groups()))
    
    matches = re.search(pattern_B, line)
    if matches:
        xb, yb = list(map(int, matches.groups()))
        systems.append([[xa, xb], [ya, yb]])

    matches = re.search(pattern_prize, line)
    if matches:
        results.append(list(map(int, matches.groups())))


sum_tokens = 0
sum_tokens_part2 = 0

for i in range(len(systems)):
    a = np.array(systems[i]).astype(int)
    b = np.array(results[i]).astype(int)
    x = np.linalg.solve(a, b)
    
    # Make sure only to keep the integer solutions, otherwise consider not possible
    if abs(x[0] - round(x[0])) < 0.01 and abs(x[1] - round(x[1])) < 0.01:
        sum_tokens += x[0] * 3 + x[1]

    # Part 2
    b = b + 10000000000000*np.ones(2).astype(int)
    x = np.linalg.solve(a, b)
    if abs(x[0] - round(x[0])) < 0.01 and abs(x[1] - round(x[1])) < 0.01:
        sum_tokens_part2 += x[0] * 3 + x[1]

print("Sum tokens (part 1):", sum_tokens)
print("Sum tokens (part 2):", sum_tokens_part2)