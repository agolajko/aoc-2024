import copy

maze = []

"""
. - 0
visited - 1
# - 2

"""

with open("../data/day6.txt", newline='\n') as f:
    for line in f:
        line = line.strip()
        maze.append(list(line))

maze_empty = []


def create_start_maze(maze_arr: list, maze_num: list):
    for i in range(len(maze)):
        maze_num.append([])
        for j in range(len(maze[i])):
            if maze_arr[i][j] == ".":
                maze_num[i].append(0)
            elif maze_arr[i][j] == "#":
                maze_num[i].append(2)
            elif maze_arr[i][j] == "^":
                maze_num[i].append(3)
            elif maze_arr[i][j] == "v":
                maze_num[i].append(4)
            elif maze_arr[i][j] == "<":
                maze_num[i].append(5)
            elif maze_arr[i][j] == ">":
                maze_num[i].append(6)
    return maze_num


def find_path(grid):

    # Directions: up, right, down, left (clockwise order)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    current_dir = 0  # Start going up

    step_counter = 0

    # Find starting position
    start_pos = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 3:
                start_pos = (i, j)
                break
        if start_pos:
            break

    path = []
    current_pos = start_pos

    visited_pos = set()

    while True:
        path.append(current_pos)

        # print(f'Current pos {current_pos}')

        next_state = (current_pos, current_dir)

        if next_state in visited_pos:

            # check loop length
            prev_index = path.index(current_pos)
            path_length = len(path)
            loop_length = path_length - prev_index

            # print(f'Loop found! {loop_length} length')

            return loop_length, step_counter,  True

        else:
            visited_pos.add(next_state)

        # Try moving in current direction
        next_pos = (
            current_pos[0] + directions[current_dir][0],
            current_pos[1] + directions[current_dir][1]
        )

        # Check if we hit a wall or out of bounds
        if (next_pos[0] < 0 or next_pos[0] >= len(grid) or
                next_pos[1] < 0 or next_pos[1] >= len(grid[0])):
            break

        elif grid[next_pos[0]][next_pos[1]] == 2:
            # Turn right
            current_dir = (current_dir + 1) % 4

        elif grid[next_pos[0]][next_pos[1]] == 0 and next_pos not in path:
            step_counter += 1

            current_pos = next_pos

        else:
            current_pos = next_pos

    return path, step_counter, False


def find_loops(grid, path):

    loop_counter = 0
    progress_counter = 0

    for i, j in set(path):

        if progress_counter % 300 == 0:
            print(f'Progress: {progress_counter}/{len(set(path))}')
        progress_counter += 1

        # for i in range(len(grid)):
        #     for j in range(len(grid[i])):
        # for i in [7]:
        #     for j in [6, 7, 8, 9]:

        looping = False
        copy_grid = copy.deepcopy(grid)

        # print(f'Is looping? {looping}')
        if copy_grid[i][j] == 3:
            print(f'Cant place barrier in start pos {i,j}')
        else:
            copy_grid[i][j] = 2

            # print(f'Barrier placed at {i,j}')

            paths_none, no_steps_none, looping = find_path(copy_grid)

            if looping:
                # print(f'Loop found')
                # print(f'Pos {i,j}')
                loop_counter += 1

                if loop_counter % 10 == 0 and loop_counter > 0:
                    print(f'Loop counter value: {loop_counter}')

    return loop_counter


if __name__ == "__main__":
    maze_start = create_start_maze(maze, maze_empty)

    path1, no_steps, looping = find_path(maze_start)
    # # print(path1[0])
    # # print(path1)
    # # print(f'(9,7) in path {(9,7) in path1}')
    # print(f'No. steps: {no_steps+1}')
    # print(f'Looping? {looping}')

    loops_found = 0

    loops_found = find_loops(maze_start, path1)
    print(f'Found {loops_found} possible positions for loops')
