import re
import heapq
from typing import Dict, Set, Tuple, Optional


def read_file(lines_to_read: int) -> list:
    with open('../data/day18_small.txt', 'r') as file:
        file_content = file.read()

        in_map = []
        lines = file_content.strip().split('\n')

        # Process three lines at a time
        for i in range(0, lines_to_read):

            coords = re.findall(
                r'(\d+),(\d+)', lines[i])

            # print(coords)
            in_map.append((int(coords[0][1]), int(coords[0][0])))

    return in_map


def create_map(in_map: list, map_dim: tuple) -> dict:
    viable_pos = set()
    for row in range(map_dim[0]):
        for col in range(map_dim[1]):
            if (row, col) not in in_map:
                viable_pos.add((row, col))

    return viable_pos


def create_graph(viable_pos: dict) -> dict:
    graph = {}
    for pos in viable_pos:
        for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (pos[0] + dir[0], pos[1] + dir[1]) in viable_pos:
                if (pos, dir) not in graph:
                    graph[(pos, dir)] = {}
                for dir_next in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    # print(f'Pos {pos}, dir {dir}')
                    graph[(pos, dir)][(
                        (pos[0] + dir[0], pos[1] + dir[1]), dir_next)] = 1

    return graph


def draw_map(viable_pos: set, dims: tuple, traveled: list) -> None:
    traveled_pos = set([pos for pos, _ in traveled])
    for row in range(dims[0]):
        for col in range(dims[1]):
            if (row, col) in viable_pos:
                if (row, col) in traveled_pos:
                    print('O', end='')
                else:
                    print('.', end='')
            else:
                print('#', end='')
        print()


# def display_graph(graph: dict, dims: tuple) -> None:
#     for row in range(dims[0]):
#         for col in range(dims[1]):
#             for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

#                 if ((row, col), dir) in graph:
#                     print(
#                         f'Key: {((row, col), dir) }, Value: {graph[((row, col), dir) ]}')
#                     print()


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
        initial_cost = 0
        if start_state in graph:  # Only add if it's a valid move
            distances[start_state] = initial_cost
            prev[start_state] = None
            heapq.heappush(heap, (initial_cost, start_state))

    while heap:
        current_cost, current_state = heapq.heappop(heap)
        # print(f"Current cost and state: {current_cost}, {current_state} ")

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


def path_exists(graph: Dict[Tuple, Dict], start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
    # Initialize with all possible starting directions
    start_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited = set()
    stack = []

    # Add all valid starting states to the stack
    for direction in start_directions:
        start_state = (start_pos, direction)
        if start_state in graph:
            stack.append(start_state)
            visited.add(start_state)

    # Iterative DFS
    while stack:
        current_state = stack.pop()
        current_pos = current_state[0]

        if current_pos == end_pos:
            return True

        if current_state in graph:
            for next_state in graph[current_state]:
                if next_state not in visited:
                    visited.add(next_state)
                    stack.append(next_state)

    return False


def shortest_path(graph: Dict[Tuple, Dict], start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
    # Initialize with all possible starting directions
    start_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited = set()
    stack = []
    paths_found = []

    # Add all valid starting states to the stack
    for direction in start_directions:
        start_state = (start_pos, direction)
        if start_state in graph:
            stack.append(start_state)
            visited.add(start_state)

    # Iterative DFS
    while stack:
        current_state = stack.pop()
        current_pos = current_state[0]

        if current_pos == end_pos:
            paths_found.append([stack])
            print(f"Current pos {current_pos}")
            print(f"Current stack {stack}")
            print(f"Stack len {len(stack)}")

            # return True

        if current_state in graph:
            for next_state in graph[current_state]:
                if next_state not in visited:
                    visited.add(next_state)
                    stack.append(next_state)

    print(f"Paths_found in fun {paths_found}")
    return paths_found


map_dim = (7, 7)

in_map = read_file(12)

viable_pos = create_map(in_map, map_dim)
graph = create_graph(viable_pos)

cost, path = dijkstra(
    graph, (0, 0), (map_dim[0]-1, map_dim[1]-1))  # From S to E

print(f"Minimum cost: {cost} and path {path}")

draw_map(viable_pos, map_dim, [])

does_exist = path_exists(graph, (0, 0), (map_dim[0]-1, map_dim[1]-1))
path_list = shortest_path(graph, (0, 0), (map_dim[0]-1, map_dim[1]-1))
print(f"Path list {path_list}")
print(does_exist)
# print(in_map)

min_path = 30
for idx, path1 in enumerate(path_list):
    print(f"Idx {idx} and path {path1}")
    print()
    if len(path1) < min_path:
        min_path = len(path1)

print(f"Min path {min_path}")
print(f"Len path1 {len(path1)}")
