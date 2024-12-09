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


def fill_in_nones(free_space: list, compacted_space: list, i: int, j: int):
    for x in range(len(compacted_space)):
        for y in range(len(compacted_space[x])):

            if compacted_space[x][y] is None and x <= i:
                compacted_space[x][y] = free_space[i][j]
                if len(compacted_space[i]) != 0:
                    del compacted_space[i][-1]
                else:
                    del compacted_space[i]
                return free_space, compacted_space

    return free_space, compacted_space


def fill_free_space(free_space: list):
    print(f"Length of free_space: {len(free_space)}")

    compacted_space = copy.deepcopy(free_space)
    for i in range(len(free_space)-1, -1, -1):
        if i % 400 == 0:

            print(f"At {i} of {len(compacted_space)}")

        for j in range(len(free_space[i])):

            if free_space[i][j] is not None:

                free_space, compacted_space = fill_in_nones(
                    free_space, compacted_space, i, j)

    return compacted_space


def flatten_sum(compacted_space: list):
    sum = 0
    counter = 0
    print(f"Length of compacted_space: {len(compacted_space)}")
    for i in range(len(compacted_space)):
        if len(compacted_space[i]) != 0:
            for j in range(len(compacted_space[i])):
                if compacted_space[i][j] is not None:

                    sum += compacted_space[i][j] * counter
                    counter += 1

    return sum


mapped_str = parse_input(num_str)

print(flatten_sum(fill_free_space(mapped_str)))
