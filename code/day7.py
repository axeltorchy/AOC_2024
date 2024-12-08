import utils
import re

example = True

inputfile = utils.INPUT_DIR / "day7.txt"
if example:
    inputfile = utils.INPUT_DIR / "day7_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

pattern = r'(\d+):'
pattern2 = r'\s\d+'

results = []
operands = []

for line in lines:
    results.append(int(re.findall(pattern, line)[0]))
    operands.append(list(map(int, re.findall(pattern2, line))))

N_equations = len(results)

# Part 1
sum_possible = 0

def is_computable(left, remaining_list, expected_result):
    if len(remaining_list) == 1:
        return left + remaining_list[0] == expected_result or left * remaining_list[0] == expected_result
    
    return is_computable(left + remaining_list[0], remaining_list[1:], expected_result) \
        or is_computable(left * remaining_list[0], remaining_list[1:], expected_result)



for i in range(N_equations):
    N_operators = len(operands[i]) - 1
    if is_computable(operands[i][0], operands[i][1:], results[i]):
        sum_possible += results[i]

print("Part 1:", sum_possible)


# Part 2
sum_possible = 0

def is_computable_2(left, remaining_list, expected_result):
    if len(remaining_list) == 1:
        return left + remaining_list[0] == expected_result \
            or left * remaining_list[0] == expected_result \
            or int(f"{left}{remaining_list[0]}") == expected_result
    
    return is_computable_2(left + remaining_list[0], remaining_list[1:], expected_result) \
        or is_computable_2(left * remaining_list[0], remaining_list[1:], expected_result) \
        or is_computable_2(int(f"{left}{remaining_list[0]}"), remaining_list[1:], expected_result)



for i in range(N_equations):
    N_operators = len(operands[i]) - 1
    if is_computable_2(operands[i][0], operands[i][1:], results[i]):
        sum_possible += results[i]

print("Part 2:", sum_possible)
