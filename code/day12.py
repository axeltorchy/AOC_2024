#!/bin/python3
import utils
import re

example = False

inputfile = utils.INPUT_DIR / "day12.txt"
if example:
    inputfile = utils.INPUT_DIR / "day12_example5.txt"



with open(inputfile, "r") as fh:
    lines = fh.read().splitlines()

# List of sets, each set contains all the members of the region
regions = []

N_lines = len(lines)
N_col = len(lines[0])

visited_plots = set()


def explore_area(i,j):
    if (i, j) in visited_plots:
        return set()
    
    visited_plots.add((i, j))
    return_set = set()
    return_set.add((i, j))
    
    # print("==", lines[i][j], lines[i-1][j])
    
    if i > 0 and lines[i-1][j] == lines[i][j] and (i-1, j) not in visited_plots:
        #print("Top from", i, j)
        return_set = return_set.union(explore_area(i-1, j))
    
    if i < N_lines - 1 and lines[i+1][j] == lines[i][j] and (i+1, j) not in visited_plots:
        #print("Bottom from", i, j, newset)
        return_set = return_set.union(explore_area(i+1, j))
    
    if j > 0 and lines[i][j-1] == lines[i][j] and (i, j-1) not in visited_plots:
        #print("Left from", i, j)
        return_set = return_set.union(explore_area(i, j-1))
        
    if j < N_col - 1 and lines[i][j+1] == lines[i][j] and (i, j+1) not in visited_plots:
        #print("Right from", i, j, newset)
        return_set = return_set.union(explore_area(i, j+1))
    
    # print("AA", return_set)
    return return_set

N_region = 0
current_type = lines[0][0]

for i in range(N_lines):
    for j in range(N_col):
        if (i,j) in visited_plots:
            continue
        
        area_set = explore_area(i,j)
        print(f"{lines[i][j]}: region of {len(area_set)} plots.")
        print(f"   Set: {area_set}")
        regions.append(area_set)
        
regions_areas = [0] * len(regions)
regions_perimeters = [0] * len(regions)
regions_prices = [0] * len(regions)
regions_prices_part2 = [0] * len(regions)

for n in range(len(regions)):
    # For each region, find perimeter
    # Horizontal fences are located by the coordinates of the plot below
    # Vertical fences are located by the coordinates of the plot to the right
    horizontal_fences = {}
    vertical_fences = {}

    set_h_fences = set()
    set_v_fences = set()
       
    for i, j in regions[n]:
        horizontal_fences[(i,j)] = horizontal_fences.get((i,j), 0) + 1
        horizontal_fences[(i+1,j)] = horizontal_fences.get((i+1,j), 0) + 1
        
        vertical_fences[(i,j)] = vertical_fences.get((i,j), 0) + 1
        vertical_fences[(i,j+1)] = vertical_fences.get((i,j+1), 0) + 1
    
    perimeter = 0
    for x in horizontal_fences:
        if horizontal_fences[x] == 1:
            perimeter += 1
            set_h_fences.add(x)
    for x in vertical_fences:
        if vertical_fences[x] == 1:
            perimeter += 1
            set_v_fences.add(x)
    
    regions_areas[n] = len(regions[n])
    regions_perimeters[n] = perimeter
    regions_prices[n] = regions_areas[n] * perimeter
    
    print("Region", n, "Area:", regions_areas[n], "Perimeter:", regions_perimeters[n])

    # Part 2
    # Compute the number of sides
    visited_h_fences = set()
    visited_v_fences = set()

    print(" Set H fences", set_h_fences)
    print(" Set V fences", set_v_fences)

    N_sides = 0

    for x in set_h_fences:
        print("  - H fence:", x)
        i, j = x
        at_least_one = False
        while True:
            if (i, j) in set_h_fences and (i, j) not in visited_h_fences:
                visited_h_fences.add((i,j))
                print("     Visited", i, j)
                if (i,j) in regions[n] and (i,j+1) in regions[n] or (i-1,j) in regions[n] and (i-1, j+1) in regions[n]:
                    j += 1
                at_least_one = True
            else:
                break
        
        i, j = x
        if (i,j) in regions[n] and (i,j-1) in regions[n] or (i-1,j) in regions[n] and (i-1, j-1) in regions[n]:
            j -= 1
        while True:
            if (i, j) in set_h_fences and (i, j) not in visited_h_fences:
                visited_h_fences.add((i,j))
                print("     Visited", i, j)
                if (i,j) in regions[n] and (i,j-1) in regions[n] or (i-1,j) in regions[n] and (i-1, j-1) in regions[n]:
                    j -= 1
                at_least_one = True
            else:
                break
        
        if at_least_one:
            N_sides += 1


    for x in set_v_fences:
        i, j = x
        at_least_one = False
        while True:
            if (i, j) in set_v_fences and (i, j) not in visited_v_fences:
                visited_v_fences.add((i,j))
                if (i,j) in regions[n] and (i+1,j) in regions[n] or (i,j-1) in regions[n] and (i+1, j-1) in regions[n]:
                    i += 1
                at_least_one = True
            else:
                break
        
        i, j = x
        if (i,j) in regions[n] and (i-1,j) in regions[n] or (i,j-1) in regions[n] and (i-1, j-1) in regions[n]:
            i -= 1
        while True:
            if (i, j) in set_v_fences and (i, j) not in visited_v_fences:
                visited_v_fences.add((i,j))
                if (i,j) in regions[n] and (i-1,j) in regions[n] or (i,j-1) in regions[n] and (i-1, j-1) in regions[n]:
                    i -= 1
                at_least_one = True
            else:
                break
        
        if at_least_one:
            N_sides += 1
    
    print("  Number of sides", N_sides)

    regions_prices_part2[n] = regions_areas[n] * N_sides


print("Part 1, sum of region prices:", sum(regions_prices))

# Part 2
# 836294 is too low
print("Part 2, sum of region prices:", sum(regions_prices_part2))
