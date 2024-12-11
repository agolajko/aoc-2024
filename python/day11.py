
input_stones = []


with open("../data/day11.txt", newline='\n') as f:
    for line in f:
        line = line.strip()
        line = line.split(' ')
        for i in line:
            input_stones.append(int(i))


def step_forward(input_stones):

    result = []

    for idx, stone in enumerate(input_stones):
        if stone == 0:
            result.append(1)
        elif len(str(stone)) % 2 == 0:
            first_half = str(stone)[:len(str(stone))//2]
            second_half = str(stone)[len(str(stone))//2:]

            result.extend([int(first_half), int(second_half)])

        else:
            result.append(stone * 2024)
    return result


one_step = step_forward(input_stones)

print(f'First step: {one_step}')

for i in range(74):
    print(f'Step {i+1}')
    one_step = step_forward(one_step)
    # print(one_step)

print(f'Final stone number: {len(one_step)}')
