
"""
1. find base cost of traversing the maze
2. find all possible cheats
    a. loop through all map positions and see if cheat exists
    b. add to dict of cheats
3. find the cheat cost for each cheat

"""


from typing import Dict, Set, Tuple, List, Optional
from collections import deque


def read_file(filepath: str) -> tuple:
    """
    Read maze file and create position mappings.

    Args:
        filepath: Path to the maze file

    Returns:
        tuple: (start_pos, end_pos, wall_pos, viable_pos, dimensions)
    """
    start_pos = None
    end_pos = None
    wall_pos = {}
    viable_pos = set()

    with open(filepath) as f:
        lines = [line.strip() for line in f.readlines()]

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            pos = (row, col)
            if char == '#':
                wall_pos[pos] = 1
            elif char == 'S':
                start_pos = pos
                viable_pos.add(pos)
            elif char == 'E':
                end_pos = pos
                viable_pos.add(pos)
            elif char == '.':
                viable_pos.add(pos)

    dimensions = (len(lines), len(lines[0]))
    return start_pos, end_pos, wall_pos, viable_pos, dimensions


def create_viable_map(wall_positions: dict, dimensions: tuple) -> set:
    """
    Create a set of all viable positions (non-wall positions) in the maze.

    Args:
        wall_positions: Dictionary of wall positions
        dimensions: (rows, cols) of the maze

    Returns:
        set: Set of all viable positions
    """
    rows, cols = dimensions
    all_positions = {(row, col)
                     for row in range(rows)
                     for col in range(cols)}
    return all_positions - set(wall_positions.keys())


def bidirectional_bfs(start: tuple, end: tuple, viable_pos: set, dimensions: tuple) -> int:
    """
    Perform bidirectional BFS to find shortest path length.

    Args:
        start: Starting position (row, col)
        end: Ending position (row, col)
        viable_pos: Set of viable positions
        dimensions: Maze dimensions (rows, cols)

    Returns:
        int: Length of shortest path or -1 if no path exists
    """
    if start not in viable_pos or end not in viable_pos:
        return -1

    # Initialize forward and backward searches
    forward_q = deque([(start, 0)])
    backward_q = deque([(end, 0)])
    forward_visited = {start: 0}
    backward_visited = {end: 0}

    rows, cols = dimensions
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while forward_q and backward_q:
        # Expand forward
        pos, dist = forward_q.popleft()
        if pos in backward_visited:
            return dist + backward_visited[pos]

        # Try all directions
        for dx, dy in directions:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if (new_pos in viable_pos and
                    new_pos not in forward_visited):
                forward_q.append((new_pos, dist + 1))
                forward_visited[new_pos] = dist + 1

        # Expand backward
        pos, dist = backward_q.popleft()
        if pos in forward_visited:
            return dist + forward_visited[pos]

        for dx, dy in directions:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if (new_pos in viable_pos and
                    new_pos not in backward_visited):
                backward_q.append((new_pos, dist + 1))
                backward_visited[new_pos] = dist + 1

    return -1


def find_shortcut_walls(wall_pos: dict, viable_pos: set, dimensions: tuple) -> List[tuple]:
    """
    Find all walls that could be potential shortcuts (have paths on both sides).

    Args:
        wall_pos: Dictionary of wall positions
        viable_pos: Set of viable positions
        dimensions: Maze dimensions (rows, cols)

    Returns:
        List of wall positions that could be shortcuts
    """
    shortcuts = []
    rows, cols = dimensions
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for wall in wall_pos:
        row, col = wall
        # Skip edge walls
        if row == 0 or row == rows-1 or col == 0 or col == cols-1:
            continue

        # Count viable neighbors
        viable_neighbors = sum(1 for dx, dy in directions
                               if (row + dx, col + dy) in viable_pos)

        # If wall has at least 2 viable neighbors, it's a potential shortcut
        if viable_neighbors >= 2:
            shortcuts.append(wall)

    return shortcuts


def calculate_shortcut_savings(start: tuple, end: tuple, wall_pos: dict,
                               viable_pos: set, dimensions: tuple) -> List[dict]:
    """
    Calculate path savings for each potential shortcut wall.

    Args:
        start: Starting position
        end: Ending position
        wall_pos: Dictionary of wall positions
        viable_pos: Set of viable positions
        dimensions: Maze dimensions

    Returns:
        List of dictionaries containing wall positions and their savings
    """
    # Get original path length
    original_length = bidirectional_bfs(start, end, viable_pos, dimensions)
    if original_length == -1:
        return []

    # Find all potential shortcuts
    shortcuts = find_shortcut_walls(wall_pos, viable_pos, dimensions)
    savings = []

    # Test each shortcut
    for idx, wall in enumerate(shortcuts):
        # Create new viable positions set with wall removed
        if idx % 1000 == 0:
            print(f'At {idx} of {len(shortcuts)}')
        new_viable = viable_pos | {wall}

        # Calculate new path length
        new_length = bidirectional_bfs(start, end, new_viable, dimensions)

        if new_length != -1 and new_length < original_length:
            savings.append({
                'position': wall,
                'original_length': original_length,
                'new_length': new_length,
                'saving': original_length - new_length
            })

    # Sort by savings (highest first)
    return sorted(savings, key=lambda x: x['saving'], reverse=True)

# Usage example:


def main():
    # Read the maze
    start, end, wall_pos, viable_pos, dimensions = read_file(
        '../data/day20.txt')

    # Calculate and display shortcuts
    savings = calculate_shortcut_savings(
        start, end, wall_pos, viable_pos, dimensions)

    print(
        f"Original path length: {savings[0]['original_length'] if savings else 'No path found'}")
    print("\nTop shortcuts by savings:")
    for s in savings[:5]:  # Show top 5 shortcuts
        print(f"Wall at {s['position']}: saves {s['saving']} steps "
              f"(new length: {s['new_length']})")

    print(f'Sum of all savings: {sum(s["saving"] for s in savings)}')

    more_than_100 = sum(1 for s in savings if s['saving'] >= 100)
    print(f'Number of shortcuts saving more than 100 steps: {more_than_100}')

    for i in range(5):
        print(savings[i])


if __name__ == "__main__":
    main()
