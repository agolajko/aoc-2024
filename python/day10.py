results = []
input_map = []

num_str = ''

with open("../data/day10.txt", newline='\n') as f:
    for line in f:
        line = line.strip()
        input_map.append([int(i) for i in list(line)])


def create_neighbours_dict(input_map):
    neighbours = {}
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(len(input_map)):
        for j in range(len(input_map[i])):
            neighbours[(i, j)] = []

            # print(f"Neighbours of {input_map[i][j]} input_map i: {i}, j: {j}")

            for y, x in directions:
                # print(f"y: {y}, x: {x}")
                if i+y >= 0 and i+y < len(input_map) and j+x >= 0 and j+x < len(input_map[i]):
                    if input_map[i+y][j+x] - input_map[i][j] == 1:
                        neighbours[(i, j)].append((i+y, j+x))

    return neighbours


def dfs(curent_pos: tuple, visited_paths: dict):
    # print(f"Current pos: {curent_pos}")
    # print(f"Visited paths: {visited_paths}")

    if input_map[curent_pos[0]][curent_pos[1]] == 9:
        # print(f"9 found at {curent_pos} via path: {visited_paths}")
        return 1

    nines_found = 0

    for neighbour in neighbours_dict[curent_pos]:

        # next_val = input_map[neighbour[0]][neighbour[1]]
        # print(f"Next val: {next_val}")

        if neighbour not in visited_paths:
            visited_paths.add(neighbour)
            # print(f"Adding path {neighbour} to {visited_paths}")
            nines_found += dfs(neighbour, visited_paths)
            visited_paths.remove(neighbour)
            # print(f"Now have {nines_found} nines found")
            # print(f"Not Clearing path {neighbour} from {visited_paths}")

    return nines_found


# print(input_map)
neighbours_dict = create_neighbours_dict(input_map)

paths_sum = 0

for key in neighbours_dict:
    if input_map[key[0]][key[1]] == 0:
        # print(f"Key: {key} Neighbours: {neighbours_dict[key]}")
        # print(f'Starting from 0 at {key}')
        paths_sum += dfs(key, {key})

print(f"Paths sum: {paths_sum}")
