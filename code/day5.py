import utils
import re
from functools import cmp_to_key

example = False

inputfile = utils.INPUT_DIR / "day5.txt"
if example:
    inputfile = utils.INPUT_DIR / "day5_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

dependencies = {}
dependencies2 = {}
dependencies3 = set()

updates = []

incorrect_updates_idx = []

# Parsing input
for line in lines:
    matches = re.findall(r'\d+\|\d+', line)
    if matches:
        a, b = map(int, re.findall(r'\d+', line))
        if a not in dependencies:
            dependencies[a] = [b]
        else:
            dependencies[a].append(b)
        
        if b not in dependencies2:
            dependencies2[b] = [a]
        else:
            dependencies2[b].append(a)

        dependencies3.add((a, b))

    else:
        matches = re.findall(r'\d+', line)
        if matches:
            updates.append(list(map(int, matches)))

print(updates)
print(dependencies)
print(dependencies2)
print(dependencies3)

print("========")

sum_middle_pages = 0
i_update = 0

for update in updates:
    # print("=====")
    # print("Update:", update)
    broken = False
    for i in range(len(update)):
        for j in range(i+1, len(update)):

            if (update[j], update[i]) in dependencies3:
                # print("Breaking rule!", (update[j], update[i]))
                broken = True
                break
        if broken:
            break
    
    if not broken:
        sum_middle_pages += update[len(update)//2]
    else:
        incorrect_updates_idx.append(i_update)
    
    i_update += 1


print("Part 1:", sum_middle_pages)



def compare(left, right):
    if (left, right) in dependencies3:
        return -1
    return 1

sum_incorrect_middle_pages = 0

for i in incorrect_updates_idx:
    sum_incorrect_middle_pages += sorted(updates[i], key=cmp_to_key(compare))[len(updates[i]) // 2]



print("Part 1:", sum_incorrect_middle_pages)
