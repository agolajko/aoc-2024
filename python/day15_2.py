def read_file(robot_pos: tuple, wall_pos: dict, box_pos: dict, instructions: list):
    with open('../data/day15_mid.txt') as f:
        lines = f.readlines()

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            wide_col = col * 2
            if char == '#':
                wall_pos[(row, wide_col)] = 1
                wall_pos[(row, wide_col+1)] = 1
            elif char == '@':
                robot_pos = (row, wide_col)
            elif char == 'O':
                box_pos[(row, wide_col)] = 1
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
                print('[', end='')
            elif (row, col) == robot_pos:
                print('@', end='')
            elif (row, col-1) in box_pos:  # Right side of a box
                print(']', end='')
            elif (row, col-1) == robot_pos:  # Right side of robot
                print('.', end='')
            else:
                print('.', end='')
        print()


def convert_directions(instructions: list) -> list:
    direction_map = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }
    return [direction_map[i] for i in instructions]


def is_valid_box_position(pos: tuple, wall_pos: dict, box_pos: dict, direction: tuple) -> bool:
    # For horizontal movement, check both spaces the box would occupy
    if direction[1] != 0:
        return (pos not in wall_pos and
                (pos[0], pos[1] + 1) not in wall_pos and
                pos not in box_pos)
    # For vertical movement, just check the single space
    return pos not in wall_pos and pos not in box_pos


def find_boxes_to_push(pos: tuple, direction: tuple, wall_pos: dict, box_pos: dict, pushed_boxes: set) -> bool:
    """
    Recursively find all boxes that need to be pushed when moving a box to pos.
    Returns True if the push is possible, False if not.
    Adds all boxes that need to be moved to pushed_boxes set.
    """
    # Check if this position hits a wall
    if pos in wall_pos or (pos[0], pos[1] + 1) in wall_pos:
        return False

    # Check if we can move to this position (no box or box will be moved)
    if pos not in box_pos and (pos[0], pos[1] - 1) not in box_pos:
        return True

    # Find any boxes at this position that we haven't processed yet
    new_boxes = set()
    # Check direct hit
    if pos in box_pos and pos not in pushed_boxes:
        new_boxes.add(pos)
    # Check right edge hit (box starts one to the left)
    if (pos[0], pos[1] - 1) in box_pos and (pos[0], pos[1] - 1) not in pushed_boxes:
        new_boxes.add((pos[0], pos[1] - 1))
    # Check left edge hit (box starts one to the right)
    if (pos[0], pos[1] + 1) in box_pos and (pos[0], pos[1] + 1) not in pushed_boxes:
        new_boxes.add((pos[0], pos[1] + 1))

    # If we've found new boxes, check if they can be pushed
    if new_boxes:
        pushed_boxes.update(new_boxes)
        # For each new box, check if its next position is clear
        for box_pos_found in new_boxes:
            next_pos = (box_pos_found[0] + direction[0], box_pos_found[1])
            if not find_boxes_to_push(next_pos, direction, wall_pos, box_pos, pushed_boxes):
                return False
        return True
    return True


def check_horizontal_collision(pos: tuple, box_pos: dict) -> bool:
    """Check if either edge of box at pos would collide with another box"""
    # Our box edges
    left_edge = pos
    right_edge = (pos[0], pos[1] + 1)

    # Check if either edge overlaps with any existing box
    for box in box_pos:
        box_left = box
        box_right = (box[0], box[1] + 1)

        # Check for any overlap between boxes
        if (pos[1] <= box[1] + 1 and pos[1] + 1 >= box[1]):
            return True
    return False


def move_robot(robot_pos: tuple, directions: list, wall_pos: dict, box_pos: dict, map_dim: tuple, instructions: list, print_lim: int) -> tuple:
    for idx, direction in enumerate(directions):
        new_pos = (robot_pos[0] + direction[0], robot_pos[1] + direction[1])

        # Check if robot can move to new position
        if new_pos in wall_pos:
            continue

        # Check for box collision - boxes are two spaces wide, check both spaces
        box_collision = new_pos in box_pos or (
            new_pos[0], new_pos[1] - 1) in box_pos

        if box_collision:
            # If we hit right side of a box, adjust to left edge
            if new_pos not in box_pos:
                old_box_pos = (new_pos[0], new_pos[1] - 1)
            else:
                old_box_pos = new_pos

            if idx < print_lim:
                print('Box collision')
                print(f'Old box pos: {old_box_pos}')

            # For vertical movement, use recursive check
            if direction[1] == 0:  # Vertical movement
                pushed_boxes = {old_box_pos}
                next_pos = (old_box_pos[0] + direction[0], old_box_pos[1])
                if find_boxes_to_push(next_pos, direction, wall_pos, box_pos, pushed_boxes):
                    # Move all boxes that need to be pushed
                    for box in sorted(pushed_boxes, key=lambda x: x[0], reverse=(direction[0] > 0)):
                        new_pos_box = (box[0] + direction[0], box[1])
                        box_pos[new_pos_box] = 1
                        del box_pos[box]
                else:
                    continue
            else:  # Horizontal movement
                new_box_pos = (old_box_pos[0], old_box_pos[1] + direction[1])
                if idx < print_lim:
                    print(f'New box pos: {new_box_pos}')

                # Check for box-box collisions including full width
                if check_horizontal_collision(new_box_pos, box_pos):
                    continue

                # Check for wall collisions
                if new_box_pos in wall_pos or (new_box_pos[0], new_box_pos[1] + 1) in wall_pos:
                    continue

                # Move is valid - move the box
                box_pos[new_box_pos] = 1
                del box_pos[old_box_pos]

        # Move robot
        robot_pos = new_pos

        if idx < print_lim:
            print(f'Move {idx}: {direction} {instructions[idx]}')
            print_map(wall_pos, box_pos, robot_pos, map_dim)
            print()

    return robot_pos, box_pos


def final_coordinate_sum(box_pos: dict) -> int:
    return sum([100 * box[0] + box[1] for box in box_pos.keys()])


def main():
    robot_pos, wall_pos, box_pos, instructions = (0, 0), {}, {}, []

    # Read and setup
    robot_pos, wall_pos, box_pos, instructions = read_file(
        robot_pos, wall_pos, box_pos, instructions)
    directions = convert_directions(instructions)
    map_dim = get_map_dimensions(wall_pos)

    # Initial state
    print("Initial state:")
    print_map(wall_pos, box_pos, robot_pos, map_dim)
    print()

    print_lim = 100

    # Process moves
    robot_pos, box_pos = move_robot(
        robot_pos, directions, wall_pos, box_pos, map_dim, instructions, print_lim)

    # Final state
    print("\nFinal state:")
    print_map(wall_pos, box_pos, robot_pos, map_dim)
    print(f'\nFinal sum: {final_coordinate_sum(box_pos)}')


if __name__ == "__main__":
    main()
