

def read_file(robot_pos: tuple, wall_pos: dict, box_pos: dict, instructions: list):
    with open('../data/day15.txt') as f:
        lines = f.readlines()

    for row, line in enumerate(lines):

        for col, char in enumerate(line):
            if char == '#':
                wall_pos[(row, col)] = 1
            elif char == '@':
                robot_pos = (row, col)
            elif char == 'O':
                box_pos[(row, col)] = 1
            elif char in ['^', 'v', '<', '>']:
                instructions.append(char)

    return robot_pos, wall_pos, box_pos, instructions


def get_map_dimensions(wall_pos: dict) -> tuple:
    max_row = max([row for row, _ in wall_pos.keys()])
    max_col = max([col for _, col in wall_pos.keys()])

    return max_row+1, max_col+1


def print_map(wall_pos: dict, box_pos: dict, robot_pos: tuple, map_dim: tuple) -> None:
    for row in range(map_dim[0]):
        for col in range(map_dim[1]):
            if (row, col) in wall_pos:
                print('#', end='')
            elif (row, col) in box_pos:
                print('O', end='')
            elif (row, col) == robot_pos:
                print('@', end='')
            else:
                print('.', end='')
        print()


def convert_directions(instructions: list) -> list:
    directions = []
    for instruction in instructions:
        if instruction == '^':
            directions.append((-1, 0))
        elif instruction == 'v':
            directions.append((1, 0))
        elif instruction == '<':
            directions.append((0, -1))
        elif instruction == '>':
            directions.append((0, 1))

    return directions


def move_robot(robot_pos: tuple, directions: list, wall_pos: dict, box_pos: dict, map_dim: tuple) -> tuple:
    for idx, direction in enumerate(directions):

        # print(f'At index: {idx}/{len(directions)}')

        new_pos = (robot_pos[0] + direction[0], robot_pos[1] + direction[1])
        if new_pos in wall_pos:
            continue
        if new_pos in box_pos:
            new_box_pos = (new_pos[0] + direction[0],
                           new_pos[1] + direction[1])
            if new_box_pos in wall_pos:
                continue
            elif new_box_pos in box_pos:
                # check if there are any open spaces btw the box and the wall
                # print(f'Clashing boxes')

                # get the nearest wall in that direction
                num_boxes_in_dir = 1
                num_empty_space_in_dir = 0
                for i in range(1, 40):
                    if (new_box_pos[0] + direction[0] * i, new_box_pos[1] + direction[1] * i) in box_pos:
                        num_boxes_in_dir += 1

                    elif (new_box_pos[0] + direction[0] * i, new_box_pos[1] + direction[1] * i) in wall_pos:
                        closest_wall = (
                            new_box_pos[0] + direction[0] * i, new_box_pos[1] + direction[1] * i)
                        closest_empty_first = 0
                        break

                    else:
                        num_empty_space_in_dir + 1
                        closest_empty_first = 1

                        break

                # check if there are any open spaces btw the robot and the box
                if closest_empty_first:
                    # spawn new box

                    # print(
                    #     f'Spawn new box {num_boxes_in_dir} number of pos in that dir')

                    new_box_pos = (new_box_pos[0] + direction[0] * num_boxes_in_dir,
                                   new_box_pos[1] + direction[1] * num_boxes_in_dir)
                    # box_pos[new_box_pos] = 1
                    # del box_pos[new_pos]
                else:
                    continue

            box_pos[new_box_pos] = 1
            del box_pos[new_pos]
        robot_pos = new_pos
        # print(f'Robot pos after move: {robot_pos}')
        # print_map(wall_pos, box_pos, robot_pos, map_dim)

    return robot_pos, box_pos


def final_coordinate_sum(box_pos: dict) -> int:

    return sum([100*box[0] + box[1] for box in box_pos.keys()])


robot_pos, wall_pos, box_pos, instructions = (0, 0), {}, {}, []

robot_pos, wall_pos, box_pos, instructions = read_file(
    robot_pos, wall_pos, box_pos, instructions)
directions = convert_directions(instructions)

# print(f'Robot pos before: {robot_pos}')
# print(f'Box pos before: {box_pos}')

map_dim = get_map_dimensions(wall_pos)
# print(f'Map dimensions: {map_dim}')

# print_map(wall_pos, box_pos, robot_pos, map_dim)


robot_pos, box_pos = move_robot(
    robot_pos, directions, wall_pos, box_pos, map_dim)


# print(f'Directions: {directions}')
# print(f'Robot pos: {robot_pos}')
# print(f'Wall pos: {wall_pos}')
# print(f'Box pos: {box_pos}')

# print_map(wall_pos, box_pos, robot_pos, map_dim)

print(f'Final sum: {final_coordinate_sum(box_pos)}')
