import utils
import re
import numpy as np

example = False

inputfile = utils.INPUT_DIR / "day4.txt"
if example:
    inputfile = utils.INPUT_DIR / "day4_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    horizontal = fh.read().splitlines()

lines = []

for i in range(len(horizontal)):
    lines.append(list(horizontal[i]))

N_lines = len(lines)
N_col = len(lines[0])

lines_np = np.array(lines)

left_diags = [lines_np[::-1,:].diagonal(i) for i in range(-1 * N_lines + 1, N_col)]
right_diags = [lines_np.diagonal(i) for i in range(N_lines, -1 * N_col,-1)]


diags_l = ["".join(n.tolist()) for n in left_diags]
diags_r = ["".join(n.tolist()) for n in right_diags]
diags_r.remove("")
vertical = ["".join([lines[i][j] for i in range(N_col)]) for j in range(N_lines)]

N_xmas = 0

for x in horizontal:
    N_xmas += x.count("XMAS")
    N_xmas += x.count("SAMX")
for x in vertical:
    N_xmas += x.count("XMAS")
    N_xmas += x.count("SAMX")
for x in diags_l:
    N_xmas += x.count("XMAS")
    N_xmas += x.count("SAMX")
for x in diags_r:
    N_xmas += x.count("XMAS")
    N_xmas += x.count("SAMX")
        

print("Part 1:", N_xmas)


# Part 2
N_xmas_2 = 0

for i in range(len(diags_l)):
    x = diags_l[i]
    for m in re.finditer("SAM", x):
        i_start, i_end = m.start(), m.end()
        m = i_start + 1
        # A is the m'th element of the i_th left diagonal
        # Let us find A's coordinates

        line_A = min(i, N_lines-1) - m
        col_A = max(0, i-N_lines+1) + m

        # Check if the other diagonal is 
        i_diag_r = N_col - col_A + line_A - 1

        diag_r = diags_r[i_diag_r]

        pos_A = i_diag_r - (N_col - 1 - col_A)

        word = lines[line_A-1][col_A-1] + lines[line_A][col_A] + lines[line_A+1][col_A+1]
        # print(word)
        
        # print("1 -- ", m, line_A, col_A, i_diag_r, diags_r[i_diag_r], "==", word)

        if word == "MAS" or word == "SAM":
            N_xmas_2 += 1

    for m in re.finditer("MAS", x):
        i_start, i_end = m.start(), m.end()
        m = i_start + 1
        # A is the m'th element of the i_th left diagonal
        # Let us find A's coordinates

        line_A = min(i, N_lines-1) - m
        col_A = max(0, i-N_lines+1) + m

        # Check if the other diagonal is 
        i_diag_r = N_col - col_A + line_A - 1

        diag_r = diags_r[i_diag_r]

        pos_A = i_diag_r - (N_col - 1 - col_A)

        word = lines[line_A-1][col_A-1] + lines[line_A][col_A] + lines[line_A+1][col_A+1]
        # print(word)
        
        #print("2 -- ", m, line_A, col_A, i_diag_r, diags_r[i_diag_r], "==", word)

        if word == "MAS" or word == "SAM":
            N_xmas_2 += 1


print("Part 2:", N_xmas_2)