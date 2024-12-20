import utils
import re
from itertools import combinations

example = False

inputfile = utils.INPUT_DIR / "day9.txt"
if example:
    inputfile = utils.INPUT_DIR / "day9_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

blocks = []
empty_blocks_id = []

file_lengths = {}
file_starting_id = {}

empty_blocks_lengths = []
empty_blocks_starting_id = []

current_id = 0
is_fileblock_id = True
for x in lines[0].strip():
    digit = int(x)
    if is_fileblock_id:
        # For part 2
        file_lengths[current_id] = digit
        file_starting_id[current_id] = len(blocks)

        blocks.extend([current_id] * digit)
        current_id += 1
        is_fileblock_id = False

    else:
        # For part 2
        if digit != 0:
            empty_blocks_lengths.append(digit)
            empty_blocks_starting_id.append(len(blocks))

        empty_blocks_id.extend([i for i in range(len(blocks), len(blocks)+digit)])
        blocks.extend([None] * digit)
        is_fileblock_id = True


print("Total file blocks:", len(blocks))

# Part 1
# Moving blocks
blocks_moved = blocks.copy()

current_filled_id = 0
max_block_id = 0
for i in range(len(blocks)-1,-1,-1):
    if i <= empty_blocks_id[current_filled_id]:
        # Re-ordering is finished
        max_block_id = i
        break

    if blocks[i] is None:
        continue

    #print(f"Moving block {i} ({blocks[i]}) to position {empty_blocks_id[current_filled_id]}")
    blocks_moved[i] = None
    blocks_moved[empty_blocks_id[current_filled_id]] = blocks[i]
    current_filled_id += 1


# Compute checksum

def compute_checksum(blocks_list):
    checksum = 0
    for i in range(len(blocks_list)):
        if blocks_list[i] is None:
            continue
        checksum += i * blocks_list[i]
    return checksum

print("Part 1, checksum;", compute_checksum(blocks_moved))



# Part 2 - naive
blocks_part2 = blocks.copy()

max_file_id = max(file_lengths.keys())

for i in range(max_file_id,0,-1):
    # For each file, find the leftmost empty space with sufficient size
    file_size = file_lengths[i]

    for j in range(len(empty_blocks_lengths)):
        if empty_blocks_starting_id[j] >= file_starting_id[i]:
            # Only move the file if the empty space is left to that file 
            break

        if empty_blocks_lengths[j] >= file_size:
            # print(f"Moving file {i} to block starting position {empty_blocks_starting_id[j]}")
            start_id = empty_blocks_starting_id[j]
            for k in range(file_size):
                blocks_part2[start_id+k] = i
                blocks_part2[file_starting_id[i]+k] = None
            
            if empty_blocks_lengths[j] == file_size:
                empty_blocks_lengths.pop(j)
                empty_blocks_starting_id.pop(j)
            else:
                empty_blocks_lengths[j] -= file_size
                empty_blocks_starting_id[j] += file_size
            break

print("Part 2, checksum;", compute_checksum(blocks_part2))