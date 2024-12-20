#!/bin/python3
import utils
import re

example = False

inputfile = utils.INPUT_DIR / "day11.txt"
if example:
    inputfile = utils.INPUT_DIR / "day11_example.txt"


with open(inputfile, "r") as fh:
    lines = fh.read().splitlines()


stones = [int(x) for x in lines[0].strip().split()]

print("Before blinking:")
print(stones)

def blink(stone_list):
    new_list = []
    for i in range(len(stone_list)):
        x = stone_list[i]
        #print("==", x)
        # Rule 1: if 0, then become 1
        if x == 0:
            new_list.append(1)
            continue
        # Rule 2: if even number of digits
        length = len(str(x))
        if length % 2 == 0:
            new_list.append(int(str(x)[:length//2]))
            new_list.append(int(str(x)[length//2:]))
            continue
        
        # If no rule applies, then replace by new stone
        new_list.append(x * 2024)
    return new_list

stone_list = stones

N = 25

for i in range(N):
    # print(f"Blinking for the {i+1}-th time")
    stone_list = blink(stone_list)

print(f"Part 1: after blinking {N} times, {len(stone_list)} stones")




## Part 2: since each stone is treated independently,
# no need to store them all
# We only need one entry (count) per stone "type" (number)
stones_count = {}

for x in stones:
    stones_count[x] = stones_count.get(x, 0) + 1

def blink2(stones_count):
    stone_numbers = list(stones_count.keys())
    
    new_stone_count = {}
    
    for x in stones_count.keys():
        # For each type of stone
        number_x = stones_count[x]
        
        # Rule 1: if 0, then become 1
        if x == 0:
            new_stone_count[1] = new_stone_count.get(1, 0) + number_x
            continue
        # Rule 2: if even number of digits
        length = len(str(x))
        if length % 2 == 0:
            number1 = int(str(x)[:length//2])
            number2 = int(str(x)[length//2:])
            new_stone_count[number1] = new_stone_count.get(number1, 0) + number_x
            new_stone_count[number2] = new_stone_count.get(number2, 0) + number_x
            continue
        
        # If no rule applies, then replace by new stone
        new_stone_count[x * 2024] = new_stone_count.get(x * 2024, 0) + number_x
        
    return new_stone_count

N = 75

for i in range(N):
    # print(f"Blinking for the {i+1}-th time")
    stones_count = blink2(stones_count)

print(f"Part 2: after blinking {N} times, {sum(stones_count.values())} stones")