import utils
import re

example = False

inputfile = utils.INPUT_DIR / "day6.txt"
if example:
    inputfile = utils.INPUT_DIR / "day6_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

blocked_positions = set()
guard_position = None
guard_direction = None

for i in range(len(lines)):
    for j in range(len(lines[i].strip())):
        if lines[i][j] == "#":
            blocked_positions.add((i, j))
        elif lines[i][j] in ["^", "<", ">", "v"]:
            initial_guard_position = [i, j]
            initial_guard_direction = lines[i][j]

N_lines = len(lines)
N_col = len(lines[0].strip())

next_moves = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1)
    }

rotations = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^"
}

guard_position = initial_guard_position.copy()
guard_direction = initial_guard_direction

guard_inside = True
visited_positions = set([(guard_position[0], guard_position[1])])
visited_positions_with_dir = set([(guard_position[0], guard_position[1], guard_direction)])

part_2 = set()

steps = 0
N_rotations = 0

while guard_inside:
    steps += 1
    
    #print("Current position:", guard_position)
    next_move = next_moves[guard_direction]
    next_position = (guard_position[0] + next_move[0], guard_position[1] + next_move[1])
    
    if next_position in blocked_positions:
        # Then rotate
        guard_direction = rotations[guard_direction]
        N_rotations += 1
        #print("  Rotating! Next direction:", guard_direction)
        continue
    else:
        # Part 2: check if the position has already been visited
        next_position2 = (guard_position[0] + next_move[0], guard_position[1] + next_move[1], guard_direction)
        if next_position2 in visited_positions_with_dir:
            print("Stuck in a loop!", next_position2)
            guard_inside = False

        # Then move forward if possible, or get out
        if next_position[0] < 0 or next_position[0] > N_lines - 1 \
            or next_position[1] < 0 or next_position[1] > N_col - 1:
            # Getting out
            guard_inside = False
        
        else:
            # Moving forward
            #print("Moving to", next_position)
            visited_positions.add(next_position)
            visited_positions_with_dir.add((next_position[0], next_position[1], guard_direction))
            guard_position = [next_position[0], next_position[1]]

print("Part 1, number of visited positions:", len(visited_positions))


# Re-run simulation by adding block on each visited position, and check whether we get into a loop
N_loops = 0

for x in visited_positions:
    blocked_positions.add(x)

    guard_position = initial_guard_position.copy()
    guard_direction = initial_guard_direction

    guard_inside = True
    visited_positions_with_dir_2 = set([(guard_position[0], guard_position[1], guard_direction)])

    part_2 = set()

    steps = 0
    N_rotations = 0

    while guard_inside:
        steps += 1
        
        #print("Current position:", guard_position)
        next_move = next_moves[guard_direction]
        next_position = (guard_position[0] + next_move[0], guard_position[1] + next_move[1])
        
        if next_position in blocked_positions:
            # Then rotate
            guard_direction = rotations[guard_direction]
            N_rotations += 1
            #print("  Rotating! Next direction:", guard_direction)
            continue
        else:
            # Part 2: check if the position has already been visited
            next_position2 = (guard_position[0] + next_move[0], guard_position[1] + next_move[1], guard_direction)
            if next_position2 in visited_positions_with_dir_2:
                print("Stuck in a loop! By adding block on:", x)
                N_loops += 1
                guard_inside = False

            # Then move forward if possible, or get out
            if next_position[0] < 0 or next_position[0] > N_lines - 1 \
                or next_position[1] < 0 or next_position[1] > N_col - 1:
                # Getting out
                guard_inside = False
            
            else:
                # Moving forward
                visited_positions_with_dir_2.add((next_position[0], next_position[1], guard_direction))
                guard_position = [next_position[0], next_position[1]]


    blocked_positions.remove(x)


print("Part 2, number of possibe positions to create loop:", N_loops)