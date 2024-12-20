import utils
import re

example = False

inputfile = utils.INPUT_DIR / "day10.txt"
if example:
    inputfile = utils.INPUT_DIR / "day10_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

map = []
start_positions = []

for i in range(len(lines)):
    newlist = []
    for j in range(len(lines[0][:-1])):
        x = lines[i][j]
        newlist.append(int(x))
        if int(x) == 0:
            start_positions.append((i,j))
    map.append(newlist)

N_lines = len(map)
N_col = len(map[0])

# Dict memorizing the 
ends_reachable = {}


def get_reachable_top(map, i, j):
    """This function returns a SET containing all the reachable positions
    that have a height of 9 from the provided starting poing.
    Recursive."""
    if (i,j) in ends_reachable:
        return ends_reachable[(i,j)]

    current_level = map[i][j]
    if current_level == 9:
        # print("Reaching the top at", i,j)
        reachable = set()
        reachable.add((i,j))
        return reachable
    
    reachable_pos = set()

    # Top, only processing if exactly one level above
    if i > 0 and map[i-1][j] == map[i][j] + 1:
        # print("  Top")
        reachable_neighbor = get_reachable_top(map, i-1, j)
        reachable_pos = reachable_pos.union(get_reachable_top(map, i-1, j))
    # Right
    if j < N_col-1 and map[i][j+1] == map[i][j] + 1:
        # print("  Right")
        reachable_pos = reachable_pos.union(get_reachable_top(map, i, j+1))
    # Bottom
    if i < N_lines-1 and map[i+1][j] == map[i][j] + 1:
        # print("  Bottom")
        reachable_pos = reachable_pos.union(get_reachable_top(map, i+1, j))
    # Left
    if j > 0 and map[i][j-1] == map[i][j] + 1:
        # print("  Left")
        reachable_neighbor = get_reachable_top(map, i, j-1)
        reachable_pos = reachable_pos.union(get_reachable_top(map, i, j-1))

    ends_reachable[(i,j)] = reachable_pos
    return reachable_pos

print(N_lines)
print(N_col)

print("===")
print(map)
print("===")

print(sum([len(get_reachable_top(map,a,b)) for a,b in start_positions]))
