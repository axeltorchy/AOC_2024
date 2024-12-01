import utils
import re

example = False

inputfile = utils.INPUT_DIR / "day1.txt"
if example:
    inputfile = utils.INPUT_DIR / "day1_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

left_list = []
right_list = []

for line in lines:
    a, b = line.split()
    left_list.append(int(a))
    right_list.append(int(b))

N = len(left_list)

sorted_left_list = left_list.copy()
sorted_left_list.sort()
sorted_right_list = right_list.copy()
sorted_right_list.sort()


sum_diffs_sorted = 0
for i in range(N):
    sum_diffs_sorted += abs(sorted_left_list[i]-sorted_right_list[i])


print("Part 1:")
print(sum_diffs_sorted)


###
### Part 2
###

# Creating dict with number of occurrences in the right list
occurrences_right = {}
for x in right_list:
    if x in occurrences_right:
        occurrences_right[x] += 1
    else:
        occurrences_right[x] = 1


similarity_score = 0

for x in left_list:
    if x in occurrences_right:
        similarity_score += x * occurrences_right[x]


print("Part 2 - similarity score:", similarity_score)