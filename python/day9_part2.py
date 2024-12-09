import copy

results = []
inputs = []

num_str = ''

with open("../data/day9.txt", newline='\n') as f:
    for line in f:
        line = line.strip()
        num_str += line


def parse_input(num_str: str):
    free_space = []
    for i in range(len(num_str)):
        if i % 2 == 0:
            free_space.append([i//2] * int(num_str[i]))
        elif i % 2 != 0:
            if int(num_str[i]) != 0:
                free_space.append([None] * int(num_str[i]))
    return free_space


def fill_in_nones(free_space: list, compacted_space: list, i: int):
    for x in range(len(compacted_space)):

        if len(compacted_space[x]) >= len(free_space[i]) and x <= i:
            nones_index = []
            for is_none_index in range(len(compacted_space[x])):
                if compacted_space[x][is_none_index] is None:
                    nones_index.append(is_none_index)

            if len(nones_index) >= len(free_space[i]):

                for ind1, ind2 in zip(nones_index, range(len(free_space[i]))):
                    compacted_space[x][ind1] = free_space[i][ind2]
                    compacted_space[i][ind2] = None

                return compacted_space

    return compacted_space


def fill_free_space(free_space: list):
    print(f"Length of free_space: {len(free_space)}")

    compacted_space = copy.deepcopy(free_space)
    for i in range(len(free_space)-1, -1, -1):
        if i % 400 == 0:

            print(f"At {i} of {len(compacted_space)}")

        if free_space[i][0] is not None:

            compacted_space = fill_in_nones(
                free_space, compacted_space, i)

    return compacted_space


def flatten_sum(compacted_space: list):
    sum = 0
    counter = 0
    for i in range(len(compacted_space)):
        if len(compacted_space[i]) != 0:
            for j in range(len(compacted_space[i])):
                if compacted_space[i][j] is not None:
                    sum += compacted_space[i][j] * counter
                    counter += 1
                elif compacted_space[i][j] is None:
                    counter += 1

    return sum


mapped_str = parse_input(num_str)

filled_list = fill_free_space(mapped_str)

print(flatten_sum(filled_list))
