import heapq
from typing import Dict, Set, Tuple, Optional


def read_file(start_pos: tuple, end_pos: tuple, wall_pos: dict, viable_pos: set):
    with open('../data/day16.txt') as f:
        lines = f.readlines()

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                wall_pos[(row, col)] = 1
            elif char == 'S':
                start_pos = (row, col)
                viable_pos.add((row, col))

            elif char == 'E':
                end_pos = (row, col)
                viable_pos.add((row, col))

            elif char == '.':
                viable_pos.add((row, col))

    return start_pos, end_pos, wall_pos, viable_pos, (row, col)


def create_graph(start_pos: tuple, wall_pos: dict, viable_pos: dict) -> dict:
    graph = {}
    for pos in viable_pos:
        for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (pos[0] + dir[0], pos[1] + dir[1]) in viable_pos:
                if (pos, dir) not in graph:
                    graph[(pos, dir)] = {}
                for dir_next in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    # print(f'Pos {pos}, dir {dir}')
                    if dir_next == dir:
                        graph[(pos, dir)][(
                            (pos[0] + dir[0], pos[1] + dir[1]), dir_next)] = 1
                    else:
                        graph[(pos, dir)][(
                            (pos[0] + dir[0], pos[1] + dir[1]), dir_next)] = 1001

    return graph


def display_graph(graph: dict, dims: tuple) -> None:
    for row in range(dims[0]):
        for col in range(dims[1]):
            for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

                if ((row, col), dir) in graph:
                    print(
                        f'Key: {((row, col), dir) }, Value: {graph[((row, col), dir) ]}')
                    print()


def draw_map(wall_pos: dict, viable_pos: set, dims: tuple, traveled: list) -> None:
    traveled_pos = set([pos for pos, _ in traveled])
    for row in range(dims[0]):
        for col in range(dims[1]):
            if (row, col) in wall_pos:
                print('#', end='')
            elif (row, col) in viable_pos:
                if (row, col) in traveled_pos:
                    print('X', end='')
                else:
                    print('.', end='')
            else:
                print(' ', end='')
        print()


def dijkstra(
    graph: Dict[Tuple, Dict],
    start_pos: Tuple[int, int],
    end_pos: Tuple[int, int]
) -> Tuple[Optional[int], list]:
    # Initialize with all possible starting directions
    start_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # E, W, S, N
    heap = []
    distances = {}
    prev = {}

    for direction in start_directions:
        start_state = (start_pos, direction)
        # Cost to turn from initial east-facing
        initial_cost = 0 if direction == (0, 1) else 1000
        if start_state in graph:  # Only add if it's a valid move
            distances[start_state] = initial_cost
            prev[start_state] = None
            heapq.heappush(heap, (initial_cost, start_state))

    while heap:
        current_cost, current_state = heapq.heappop(heap)

        # If this path to this state is longer than one we've already found, skip it
        if current_cost > distances[current_state]:
            continue

        if current_state[0] == end_pos:
            path = []
            while current_state:
                path.append(current_state)
                current_state = prev[current_state]
            return current_cost, path[::-1]

        # Skip if state isn't in graph (wall or invalid position)
        if current_state not in graph:
            continue

        for neighbor, edge_cost in graph[current_state].items():
            new_cost = current_cost + edge_cost

            # Only update if we found a shorter path
            if new_cost < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_cost
                prev[neighbor] = current_state
                heapq.heappush(heap, (new_cost, neighbor))

    return None, []  # No path found


s_pos, e_pos, wall_pos, viable_pos = (0, 0), (0, 0), {}, set()

s_pos, e_pos, wall_pos, viable_pos, dims = read_file(
    s_pos, e_pos, wall_pos, viable_pos)


# print(s_pos, e_pos, wall_pos, viable_pos)

graph = create_graph(s_pos, wall_pos, viable_pos)


# display_graph(graph, dims)


# print(dims)


# Example usage:
cost, path = dijkstra(graph, s_pos, e_pos)  # From S to E

if cost is not None:
    print(f"Minimum cost: {cost}")
    # for state in path:
    #     print(f"Position: {state[0]}, Direction: {state[1]}")


# draw_map(wall_pos, viable_pos, dims, path)
