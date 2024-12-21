import heapq

from collections import defaultdict
from typing import Dict, Set, Tuple, List, Optional


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


def dijkstra_all_paths(
    graph: Dict[Tuple, Dict],
    start_pos: Tuple[int, int],
    end_pos: Tuple[int, int]
) -> Tuple[Optional[int], List[list]]:
    start_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    heap = []
    distances = {}
    prev = defaultdict(set)  # Store set of predecessors for each state

    for direction in start_directions:
        start_state = (start_pos, direction)
        initial_cost = 0  # No turn cost at start
        if start_state in graph:
            distances[start_state] = initial_cost
            # Add None as predecessor for start states
            prev[start_state].add(None)
            heapq.heappush(heap, (initial_cost, start_state))

    while heap:
        current_cost, current_state = heapq.heappop(heap)

        if current_cost > distances[current_state]:
            continue

        if current_state[0] == end_pos:
            min_cost = current_cost
            break

        if current_state not in graph:
            continue

        for neighbor, edge_cost in graph[current_state].items():
            new_cost = current_cost + edge_cost

            # If we found an equal-cost path, add it as another valid predecessor
            if new_cost == distances.get(neighbor, float('inf')):
                prev[neighbor].add(current_state)

            # If we found a better path, clear previous predecessors and start new set
            elif new_cost < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_cost
                # Start new set with this predecessor
                prev[neighbor] = {current_state}
                heapq.heappush(heap, (new_cost, neighbor))

    # Recursive function to build all paths
    def build_paths(state):
        if state is None:
            return [[]]

        paths = []
        for predecessor in prev[state]:
            for path in build_paths(predecessor):
                paths.append(path + [state])
        return paths

    # Find all paths that end at the goal
    all_paths = []
    for end_state in [s for s in prev if s[0] == end_pos]:
        if distances[end_state] == min_cost:  # Only include paths with minimum cost
            paths = build_paths(end_state)
            all_paths.extend(paths)

    return min_cost, all_paths if all_paths else []


s_pos, e_pos, wall_pos, viable_pos = (0, 0), (0, 0), {}, set()

s_pos, e_pos, wall_pos, viable_pos, dims = read_file(
    s_pos, e_pos, wall_pos, viable_pos)


# print(s_pos, e_pos, wall_pos, viable_pos)

graph = create_graph(s_pos, wall_pos, viable_pos)


# display_graph(graph, dims)


# print(dims)


# Example usage:
cost, path = dijkstra_all_paths(graph, s_pos, e_pos)  # From S to E

if cost is not None:
    print(f"Minimum cost: {cost}")
    # for state in path:
    #     print(f"Position: {state[0]}, Direction: {state[1]}")

print(f"Number of paths: {len(path)}")
# print(f"Path: {path[0][0][0]}")
count_unique = set()
for p in path:
    for i in p:
        count_unique.add(i[0])


print(f"Number of unique paths: {len(count_unique)}")
# draw_map(wall_pos, viable_pos, dims, path)
