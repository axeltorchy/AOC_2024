import utils
import re
import matplotlib.pyplot as plt

example = False

inputfile = utils.INPUT_DIR / "day14.txt"
if example:
    inputfile = utils.INPUT_DIR / "day14_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

positions = []
velocities = []

positions_cpx = []
velocities_cpx = []

# Grid dimensions
N_lines = 103
N_col = 101

if example:
    N_lines = 7
    N_col = 11

# Complex numbers:
# - real part is the distance from the left side
# - imaginary part is the distance from the top

for line in lines:
    p,v = line.split(" ")
    pos = list(map(int, p[2:].split(",")))
    vel = list(map(int, v[2:].split(",")))
    positions.append(pos)
    velocities.append(vel)
    positions_cpx.append(pos[0] + 1j*pos[1])
    velocities_cpx.append(vel[0] + 1j*vel[1])

# print(positions)
# print(velocities)

# print(positions_cpx)
# print(velocities_cpx)

# # Example
# positions_cpx = [2 + 4j]
# velocities_cpx = [2 - 3j]


# Part 1
positions_after_100s = []
for i in range(len(positions_cpx)):
    new_pos = positions_cpx[i] + 100 * velocities_cpx[i]
    new_pos = (new_pos.real % N_col) + 1j * (new_pos.imag % N_lines)
    positions_after_100s.append(new_pos)

count_robots_quadrants = {
    (False, False): 0, # Right, bottom
    (False, True): 0, # Right, top
    (True, False): 0, # Left, bottom
    (True, True): 0 # Left, top
    }

for pos in positions_after_100s:
    if pos.real == N_col // 2 or pos.imag == N_lines // 2:
        # Exactly in the middle, ignore
        continue
    count_robots_quadrants[(pos.real < N_col // 2, pos.imag < N_lines // 2)] += 1

safety_factor = 1
for x in count_robots_quadrants.values():
    safety_factor *= x

print("Part 1, safety factor:", safety_factor)


# Part 2 - starting at 8000

epoch = 0

minimum_value = 9999999999999999999999
minimum_index = 0
while True:
    epoch += 1
    for i in range(len(positions_cpx)):
        positions_cpx[i] = positions_cpx[i] + velocities_cpx[i]
        positions_cpx[i] = (positions_cpx[i].real % N_col) + 1j * (positions_cpx[i].imag % N_lines)
    
    # plt.scatter([x.real for x in positions_cpx], [x.imag for x in positions_cpx])
    # plt.xlabel('Real Part')
    # plt.ylabel('Imaginary Part')
    # plt.savefig("/tmp/figures/" + str(epoch) + ".png")
    # plt.clf()

    count_robots_quadrants = {
        (False, False): 0, # Right, bottom
        (False, True): 0, # Right, top
        (True, False): 0, # Left, bottom
        (True, True): 0 # Left, top
        }

    for pos in positions_cpx:
        if pos.real == N_col // 2 or pos.imag == N_lines // 2:
            # Exactly in the middle, ignore
            continue
        count_robots_quadrants[(pos.real < N_col // 2, pos.imag < N_lines // 2)] += 1

    if count_robots_quadrants[(False, True)] == count_robots_quadrants[(True, True)] and \
        count_robots_quadrants[(True, False)] == count_robots_quadrants[(False, False)]:
        print("OK MAYBE! After", epoch, "times.")

    safety_factor = 1
    for x in count_robots_quadrants.values():
        safety_factor *= x

    if safety_factor < minimum_value:
        minimum_value = safety_factor
        minimum_index = epoch
    #print("Epoch", epoch, "--", safety_factor)

    if epoch % 20 == 0:
        print("#", epoch)
    if epoch == 15000:
        break


# 6752 too low
# 6146 too low
# 5712 too low
# 9308 no
# 9732 ?

print("Epoch minimizing the safety factor:", minimum_index, minimum_value)
# Answer: 18264