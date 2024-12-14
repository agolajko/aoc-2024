import re


def read_file() -> list:
    with open('../data/day14.txt', 'r') as file:
        file_content = file.read()

        in_map = []
        lines = file_content.strip().split('\n')

        # Process three lines at a time
        for i in range(0, len(lines)):

            # Extract numbers using regex
            line_items = re.findall(
                r'p\=(\d+),(\d+) v\=(-?\d+),(-?\d+)', lines[i])

            start = {

                'position': {
                    'x': int(line_items[0][0]),
                    'y': int(line_items[0][1])
                },
                'velocity': {
                    'x': int(line_items[0][2]),
                    'y': int(line_items[0][3])
                }
            }

            in_map.append(start)
            # print(line_items)

        return in_map


def run_steps(in_pos: dict, steps: int, map_size: tuple, ret_dict: dict) -> dict:

    in_x = in_pos['position']['x']
    in_y = in_pos['position']['y']

    speed_x = in_pos['velocity']['x']
    speed_y = in_pos['velocity']['y']

    new_x = (in_x + (speed_x * steps)) % map_size[0]
    new_y = (in_y + (speed_y * steps)) % map_size[1]

    # print(f'New pos: {new_x}, {new_y}')

    if (new_x, new_y) not in ret_dict:
        ret_dict[(new_x, new_y)] = 1
    else:
        ret_dict[(new_x, new_y)] += 1

    return ret_dict


def print_map(ret_dict: dict, map_size: tuple) -> None:

    for y in range(map_size[1]):
        for x in range(map_size[0]):
            if (x, y) in ret_dict:
                print(ret_dict[(x, y)], end='')
            else:
                print('.', end='')
        print('')


def count_quadrants(out_map: dict, map_size: tuple) -> int:

    quad_1 = 0
    quad_2 = 0
    quad_3 = 0
    quad_4 = 0

    mid_x = map_size[0] // 2
    mid_y = map_size[1] // 2

    for y in range(map_size[1]):
        for x in range(map_size[0]):
            if (x, y) in out_map:
                if x < mid_x and y < mid_y:
                    quad_1 += out_map[(x, y)]
                elif x > mid_x and y < mid_y:
                    quad_2 += out_map[(x, y)]
                elif x < mid_x and y > mid_y:
                    quad_3 += out_map[(x, y)]
                elif x > mid_x and y > mid_y:
                    quad_4 += out_map[(x, y)]

    return quad_1 * quad_2*quad_3 * quad_4


# print(read_file())
in_map1 = read_file()
map_dim = (101, 103)
out_map = {}
for in_line in in_map1:
    out_map = run_steps(in_line, 100, map_dim, out_map)
print(out_map)
print_map(out_map, map_dim)
print(count_quadrants(out_map, map_dim))


for i in range(10000):
    out_map = {}
    for in_line in in_map1:
        out_map = run_steps(in_line, i, map_dim, out_map)
    # print(out_map)

    # check if none share a space
    # that's perhaps when a tree will form
    all_ones = True
    for key in out_map:
        if out_map[key] > 1:
            all_ones = False
            break

    if all_ones:
        # print to check tree visually
        print_map(out_map, map_dim)
        print(f'Step: {i}')
        print('\n\n\n')
