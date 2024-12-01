import utils
import re

example = False

inputfile = utils.INPUT_DIR / "day1.txt"
if example:
    inputfile = utils.INPUT_DIR / "day1_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

list1 = []
list2 = []

for line in lines:
    a, b = line.split()
    list1.append(int(a))
    list2.append(int(b))

N = len(list1)

sorted_list1 = list1.copy()
sorted_list1.sort()
sorted_list2 = list2.copy()
sorted_list2.sort()


sum_diffs_sorted = 0
for i in range(N):
    sum_diffs_sorted += abs(sorted_list1[i]-sorted_list2[i])

print(sum_diffs_sorted)
