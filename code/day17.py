import utils
import re

example = False

inputfile = utils.INPUT_DIR / "day17.txt"
if example:
    inputfile = utils.INPUT_DIR / "day17_example.txt"

pattern_A = r'Register A: (\d+)'
pattern_B = r'Register B: (\d+)'
pattern_C = r'Register C: (\d+)'
pattern_program = r'Program: (\d+)'

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

register_A = 0
register_B = 0
register_C = 0

program = None

for line in lines:
     matches = re.search(pattern_A, line)
     if matches:
         register_A = int(matches.group(1))
     matches = re.search(pattern_B, line)
     if matches:
         register_B = int(matches.group(1))
     matches = re.search(pattern_C, line)
     if matches:
         register_C = int(matches.group(1))
     matches = re.search(pattern_program, line)
     if "Program" in line:
         program = list(map(int, line.strip().split()[1].split(",")))
         
# print(register_A)
# print(register_B)
# print(register_C)
# print(program)

# Opcodes:




def run_program(A, B, C, program, part2 = False):
    pointer = 0
    out_values = []
    register_A = A
    register_B = B
    register_C = C
    
    def get_combo_value(operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return register_A
        elif operand == 5:
            return register_B
        elif operand == 6:
            return register_C
        elif operand == 7:
            print("RESERVED")
            return None
        else:
            print("Should not happen.")
            return None

    while True:
        if pointer >= len(program):
            #print("===== HALT =====")
            break
        
        opcode = program[pointer]
        if pointer < len(program) - 1:
            operand = program[pointer + 1]
        
        if opcode == 0:
            # Operation 'adv' (division)
            numerator = register_A
            denominator = 2 ** get_combo_value(operand)
            register_A = int(numerator / denominator)
        
        elif opcode == 1:
            # Operation 'bxl' (bitwise XOR, literal operand)
            register_B = register_B ^ operand
        
        elif opcode == 2:
            # Operation 'bst': B modulo 8 (keep lowest 3 bits)
            register_B = get_combo_value(operand) % 8
            
        elif opcode == 3:
            # Operation 'jnz': nothing if A == 0, otherwise
            # jump to instruction 'literal'
            if register_A != 0:
                # substract 2 so that it compensates the +2 at the end of the iteration
                pointer = operand - 2
        
        elif opcode == 4:
            # Operation 'bxc' bitwise B XOR C
            register_B = register_B ^ register_C
        
        elif opcode == 5:
            # Operation 'out'
            out_values.append(get_combo_value(operand) % 8)
            if part2:
                last_out = len(out_values) - 1
                
                if part2 and out_values[last_out] != program[last_out]:
                    # print("*****", out_values[last_out], program[last_out])
                    return None
        
        elif opcode == 6:
            # Operation 'bdv'
            numerator = register_A
            denominator = 2 ** get_combo_value(operand)
            register_B = int(numerator / denominator)
            
        elif opcode == 7:
            numerator = register_A
            denominator = 2 ** get_combo_value(operand)
            register_C = int(numerator / denominator)
            
        pointer += 2

    return out_values

# Part 1
out_values = run_program(register_A, register_B, register_C, program)
print("Part 1 - Final output:", ','.join(list(map(str, out_values))))


# print("PART2")
# print(run_program(117440, 0, 0, program, part2=True))

# exit()

# Part 2
program_str = ','.join(list(map(str, out_values)))
A_iter = 0
while True:
    out_values = run_program(A_iter, register_B, register_C, program, part2=True)
    if out_values is None or len(out_values) < len(program):
        A_iter += 1
        continue
    else: 
        print("i=", A_iter, out_values)
        break
    
    # elif ','.join(list(map(str, out_values))) == program_str:
    #     print(register_A, register_B, register_C, out_values)
    #     print("Part 2 - Register A:", i)