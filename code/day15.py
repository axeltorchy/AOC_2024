import utils
import re

example = False

inputfile = utils.INPUT_DIR / "day15.txt"
if example:
    inputfile = utils.INPUT_DIR / "day15_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()


parse_moves = False
blocked_positions = set()
robot_position = None
box_positions = set()
list_moves = []
# Positions stored using complex numbers
for i in range(len(lines)):
    line = lines[i].strip()
    if len(line) < 2:
        parse_moves = True
        continue

    if not parse_moves:
        for j in range(len(line)):
            if line[j] == '#':
                blocked_positions.add(i + 1j*j)
            elif line[j] == 'O':
                box_positions.add(i + 1j*j)
            elif line[j] == '@':
                robot_position = i + 1j*j
    
    else:
        for j in range(len(line)):
            list_moves.append(line[j])

initial_position = robot_position

# print(blocked_positions)
# print(box_positions)
# print(robot_position)

# print(list_moves)
# print(len(list_moves))


moves = {
    "^": -1 + 0j,
    ">": 0 + 1j,
    "v": 1 + 0j,
    "<": 0 - 1j
    }


boxes = box_positions.copy()


def move(position, boxes, direction):
    next_position = position + moves[direction]
    # Case 1: next position is empty
    if next_position not in blocked_positions and next_position not in boxes:
        return next_position
    
    # Case 2: next position is blocked
    elif next_position in blocked_positions:
        return position

    # Case 3: next position is occupied by a box
    else:
        # Find how many boxes are in the way
        n = 1
        while True:
            isbox_pos = next_position + n * moves[direction]
            if isbox_pos in boxes:
                n += 1
                continue
            elif isbox_pos in blocked_positions:
                # Then there is no room this way since we haven't stopped before
                next_position = position
                break
            else:
                # Then there is a free space: move all boxes by one
                boxes.remove(next_position)
                boxes.add(isbox_pos)
                break
        return next_position


# Part 1
print("## Part 1 ##")
print("Initial robot position:", initial_position)
for x in list_moves:
    robot_position = move(robot_position, boxes, x)

# print(list_moves)
# print(boxes)
print("Final Robot position:", robot_position)

sum_gps = 0
for box in boxes:
    sum_gps += 100 * box.real + box.imag

print("Sum GPS:", sum_gps)


# Part 2 - scaled up version
blocked_part2 = set()
boxes_part2 = set()
robot_position = initial_position + 1j * initial_position.imag

for x in blocked_positions:
    blocked_part2.add(x + 1j * x.imag)
    blocked_part2.add(x + 1j * (x.imag + 1))


boxes = set()

for x in box_positions:
    # Only store the position of the left part of the box
    boxes_part2.add(x + 1j * x.imag)
    #boxes_part2.add(x + 1j * (x.imag + 1))

def move_top_bottom(direction, box_pos):
    print("   - Moving", direction, box_pos)
    # Returns an empty set if the box cannot be moved
    # Returns the set of boxes to be moves upwards if can be moved.
    tomove = set()

    if box_pos + moves[direction] in blocked_part2 or box_pos + moves[direction] + 1j in blocked_part2:
        # There is at least a blocked tile blocking the move
        return set()
    elif box_pos + moves[direction] in boxes_part2:
        # One box directly above.
        next_box_pos = box_pos + moves[direction]
        tomove = move_top_bottom(direction, next_box_pos)
        # If the box above can't be moved: then this box can't be moved either
        if len(tomove) == 0:
            return set()
        
    elif box_pos + moves[direction] - 1j in boxes_part2 or box_pos + moves[direction] + 1j in boxes_part2:
        # at least one box to try to move
        # try to move left box if exists
        if box_pos + moves[direction] - 1j in boxes_part2:
            move_top_left = move_top_bottom(direction, box_pos + moves[direction] - 1j)
            if len(move_top_left) == 0:
                return set()
            else:
                tomove = tomove.union(move_top_left)
        
        # try to move right box if exists
        if box_pos + moves[direction] + 1j in boxes_part2:
            move_top_right = move_top_bottom(direction, box_pos + moves[direction] + 1j)
            if len(move_top_right) == 0:
                return set()
            else:
                tomove = tomove.union(move_top_right)

    tomove.add(box_pos)
    return tomove

def move(position, boxes_part2, direction):
    next_position = position + moves[direction]
    # Case 1: next position is blocked
    if next_position in blocked_part2:
        return position
    
    # Case 2: next position is empty
    elif next_position - 1j not in boxes_part2 and next_position not in boxes_part2:
        return next_position
    

    # Case 3: next position is occupied by a box
    else:
        # Two cases: horizontal move (easier) and vertical move (harder)
        # Horizontal move
        boxes_to_move = set()
        if direction == '<':
            isbox_pos = position - 2j
            while True:
                # If there is a box and there is an empty space next to it:
                if isbox_pos in boxes_part2 and isbox_pos - 1j not in blocked_part2:
                    # Then if there is not another box, the space is empty.
                    boxes_to_move.add(isbox_pos)
                    if isbox_pos - 2j not in boxes_part2:
                        break
                    # Otherwise, there is another box, let's continue
                    isbox_pos -= 2j
                # Otherwise, it must be blocked
                elif isbox_pos in boxes_part2 and isbox_pos - 1j in blocked_part2:
                    next_position = position
                    boxes_to_move = set()
                    break
                else:
                    print("SHOULD NOT HAPPEN")
                    exit()

            # If the space was empty, there must be boxes to move left
            print(f"  {len(boxes_to_move)} boxes to move.")
            if len(boxes_to_move) == 0:
                return position
            for x in boxes_to_move:
                boxes_part2.remove(x)
                boxes_part2.add(x - 1j)

        elif direction == '>':
            isbox_pos = position + 1j
            while True:
                # If there is a box and there is an empty space next to it:
                if isbox_pos in boxes_part2 and isbox_pos + 2j not in blocked_part2:
                    # Then if there is not another box, the space is empty.
                    boxes_to_move.add(isbox_pos)
                    if isbox_pos + 2j not in boxes_part2:
                        break
                    # Otherwise, there is another box, let's continue
                    isbox_pos += 2j
                # Otherwise, it must be blocked
                elif isbox_pos in boxes_part2 and isbox_pos + 2j in blocked_part2: 
                    next_position = position
                    boxes_to_move = set()
                    break
                else:
                    print("SHOULD NOT HAPPEN")
                    exit()
        
            print(f"  {len(boxes_to_move)} boxes to move.")
            if len(boxes_to_move) == 0:
                return position
            for x in boxes_to_move:
                boxes_part2.remove(x)
                boxes_part2.add(x + 1j)

        elif direction in {'^','v'}:
            # Determine if box is directly above/below or on the left side:
            if next_position - 1j in boxes_part2:
                tomove = move_top_bottom(direction, next_position - 1j)
            else:
                tomove = move_top_bottom(direction, next_position)
            
            #print("    TOMOVE:", tomove)
            if len(tomove) == 0:
                # Impossible to move upwards/downwards
                return position
            else:
                # Otherwise, move all boxes in the corresponding direction
                for x in tomove:
                    boxes_part2.remove(x)
                for x in tomove:
                    boxes_part2.add(x + moves[direction])

        return next_position

print("Initial robot position:", robot_position)
print("Initial boxes positions:", boxes_part2)

# Part 2
print("## Part 2 ##")
for x in list_moves:
    print("Moving", x)
    robot_position = move(robot_position, boxes_part2, x)
    print("  New robot position:", robot_position)
    print("  New boxes positions:", boxes_part2)



sum_gps = 0
for box in boxes_part2:
    sum_gps += 100 * box.real + box.imag

print("Sum GPS:", sum_gps)