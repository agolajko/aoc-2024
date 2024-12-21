
import re


def read_file() -> list:
    with open('../data/day17_small.txt', 'r') as file:
        file_content = file.read()

        in_map = []
        lines = file_content.strip().split('\n')

        # Process three lines at a time
        for i in range(0, len(lines)):

            # Extract numbers using regex
            reg_a = re.findall(
                r'Register A: (\d+)', lines[i])

            reg_b = re.findall(
                r'Register B: (\d+)', lines[i])

            reg_c = re.findall(
                r'Register C: (\d+)', lines[i])

            prog = re.findall(
                # r'Program: ', lines[i])
                r'Program: (\d+(,\d+)*)', lines[i])

            if len(reg_a):
                in_map.append(int(reg_a[0]))
            elif len(reg_b):
                in_map.append(int(reg_b[0]))
            elif len(reg_c):
                in_map.append(int(reg_c[0]))
            elif len(prog):
                in_map.append([int(i) for i in list(prog[0][0])[::2]])

    return in_map


def find_combo(reg_a, reg_b, reg_c, operand: int):

    if operand in [0, 1, 2, 3]:
        return operand
    elif operand == 4:
        return reg_a
    elif operand == 5:
        return reg_b
    elif operand == 6:
        return reg_c
    elif operand == 7:
        print(f'Error! Operand 7')
        return 'Error'

    return


def op0(reg_a, reg_b, reg_c, operand: int):

    numerator = reg_a
    to_power = find_combo(reg_a, reg_b, reg_c, operand)
    denom = 2**to_power

    res1 = int(numerator/denom)

    reg_a = res1

    return reg_a


def op1(reg_a, reg_b, reg_c, operand: int):

    biwise_xor = reg_b ^ operand

    return biwise_xor


def op2(reg_a, reg_b, reg_c, operand: int):

    mod8_combo = find_combo(reg_a, reg_b, reg_c, operand) % 8

    return mod8_combo


def op3(reg_a, reg_b, reg_c, operand: int):

    if reg_a == 0:
        jump = False
        return jump, 0
    else:
        jump = True
        return jump, operand


def op4(reg_a, reg_b, reg_c, operand: int):

    bitwise_xor = reg_b ^ reg_c

    return bitwise_xor


def op5(reg_a, reg_b, reg_c, operand: int):

    mod8_combo = find_combo(reg_a, reg_b, reg_c, operand) % 8

    return mod8_combo


def op6(reg_a, reg_b, reg_c, operand: int):

    numerator = reg_a
    to_power = find_combo(reg_a, reg_b, reg_c, operand)
    denom = 2**to_power

    res1 = int(numerator/denom)

    return res1


def op7(reg_a, reg_b, reg_c, operand: int):

    numerator = reg_a
    to_power = find_combo(reg_a, reg_b, reg_c, operand)
    denom = 2**to_power

    res1 = int(numerator/denom)

    return res1


def next_instruction():

    return 2


def run_process(reg_a, reg_b, reg_c, prog):
    output = []

    instruction_pointer = 0

    while instruction_pointer < len(prog):

        opcode = prog[instruction_pointer]
        next_operand = prog[instruction_pointer+1]

        if opcode == 0:
            reg_a = op0(reg_a, reg_b, reg_c, next_operand)
            # print(f'opcode: {opcode}')
            # print(f'New reg_a {reg_a}')
            instruction_pointer += next_instruction()

        elif opcode == 1:
            reg_b = op1(reg_a, reg_b, reg_c, next_operand)
            instruction_pointer += next_instruction()

        elif opcode == 2:
            reg_b = op2(reg_a, reg_b, reg_c, next_operand)
            # output.append([out2])
            instruction_pointer += next_instruction()

        elif opcode == 3:
            # print(f'Opcode {opcode} and operand {next_operand} ')
            jump, res3 = op3(reg_a, reg_b, reg_c, next_operand)
            if jump:
                instruction_pointer = res3
            else:
                instruction_pointer += next_instruction()

        elif opcode == 4:
            reg_b = op4(reg_a, reg_b, reg_c, next_operand)
            instruction_pointer += next_instruction()

        elif opcode == 5:
            # print(f'Opcode {opcode} and operand {next_operand} ')
            mod8_combo = op5(reg_a, reg_b, reg_c, next_operand)
            output.append([int(i) for i in list(str(mod8_combo))])

            instruction_pointer += next_instruction()

        elif opcode == 6:
            reg_b = op6(reg_a, reg_b, reg_c, next_operand)
            instruction_pointer += next_instruction

        elif opcode == 7:
            reg_c = op7(reg_a, reg_b, reg_c, next_operand)
            instruction_pointer += next_instruction()

    output = [item for sublist in output for item in sublist]
    output = ','.join([str(i) for i in output])

    print(f' Reg A: {reg_a}, Reg B: {reg_b}, Reg C: {reg_c}')
    return output


reg_a, reg_b, reg_c, prog = read_file()


out = run_process(reg_a, reg_b, reg_c, prog)
print(out)
