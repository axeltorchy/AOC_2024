import utils
import re
from itertools import combinations

example = False

inputfile = utils.INPUT_DIR / "day8.txt"
if example:
    inputfile = utils.INPUT_DIR / "day8_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

antennae = {}
unique_positions_with_antinode = set()

for i in range(len(lines)):
    lines[i] = lines[i].strip()
    for j in range(len(lines[i])):
        if lines[i][j] != ".":
            if lines[i][j] in antennae:
                antennae[lines[i][j]].append(i + j * 1j)
            else:
                antennae[lines[i][j]] = [i + j * 1j]

N_lines = len(lines)
N_col = len(lines[0])
# print(antennae)


for x in antennae:
    possible_pairs = combinations(antennae[x], 2)
    for a, b in possible_pairs:
        delta = b - a
        antinode1 = a - delta
        antinode2 = b + delta

        if antinode1.real < 0 or antinode1.real > N_lines - 1 \
            or antinode1.imag < 0 or antinode1.imag > N_col - 1:
            # off bounds
            pass
        else:
            unique_positions_with_antinode.add(antinode1)
        
        if antinode2.real < 0 or antinode2.real > N_lines - 1 \
            or antinode2.imag < 0 or antinode2.imag > N_col - 1:
            # off bounds
            pass
        else:
            unique_positions_with_antinode.add(antinode2)
        
print("Part 1:", len(unique_positions_with_antinode))


# Part 2

antinodes_part_2 = set()

for x in antennae:
    possible_pairs = combinations(antennae[x], 2)

    for a, b in possible_pairs:
        delta = b - a

        i = 0
        while True:
            antinode = a + i * delta

            if antinode.real < 0 or antinode.real > N_lines - 1 \
                or antinode.imag < 0 or antinode.imag > N_col - 1:
                # off bounds
                break
            antinodes_part_2.add(antinode)
            i += 1

        i = 0
        while True:
            antinode = a - i * delta

            if antinode.real < 0 or antinode.real > N_lines - 1 \
                or antinode.imag < 0 or antinode.imag > N_col - 1:
                # off bounds
                break
            antinodes_part_2.add(antinode)
            i += 1

print("Part 2:", len(antinodes_part_2))
