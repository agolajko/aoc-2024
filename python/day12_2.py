from collections import defaultdict, deque
from typing import List, Set, Tuple, Dict


def find_regions(grid: List[str]) -> Dict[Tuple[str, int], Set[Tuple[int, int]]]:
    """Find all connected regions in the grid and return them as sets of coordinates."""
    height, width = len(grid), len(grid[0])
    visited = set()
    regions = {}
    region_count = defaultdict(int)

    def get_neighbors(x: int, y: int) -> List[Tuple[int, int]]:
        """Get valid neighboring coordinates."""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < height and 0 <= new_y < width:
                neighbors.append((new_x, new_y))
        return neighbors

    def bfs(start_x: int, start_y: int, plant_type: str) -> Set[Tuple[int, int]]:
        """Find all connected cells of the same plant type using BFS."""
        region = set()
        queue = deque([(start_x, start_y)])

        while queue:
            x, y = queue.popleft()
            if (x, y) in visited:
                continue

            visited.add((x, y))
            region.add((x, y))

            for next_x, next_y in get_neighbors(x, y):
                if grid[next_x][next_y] == plant_type and (next_x, next_y) not in visited:
                    queue.append((next_x, next_y))

        return region

    # Find all regions
    for i in range(height):
        for j in range(width):
            if (i, j) not in visited:
                plant_type = grid[i][j]
                region = bfs(i, j, plant_type)
                region_count[plant_type] += 1
                regions[(plant_type, region_count[plant_type]-1)] = region

    return regions


def count_distinct_sides(region: Set[Tuple[int, int]], grid: List[str]) -> int:
    """
    Count the number of distinct sides of a region.
    A distinct side is a straight line that separates the region from different regions or the grid edge.
    """
    height, width = len(grid), len(grid[0])
    sides = set()

    # Helper function to check if a point is outside the grid
    def is_outside(x: int, y: int) -> bool:
        return x < 0 or x >= height or y < 0 or y >= width

    # For each cell in the region
    for x, y in region:
        # For each direction (right, down, left, up)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy

            # If next cell is outside grid or contains a different plant type
            if is_outside(nx, ny) or (nx, ny) not in region:
                # For horizontal sides (dx == 0)
                if dx == 0:
                    # Look up and down to find where this vertical segment starts/ends
                    up = x
                    while (up-1, y) in region and (up-1, ny) not in region:
                        up -= 1
                    down = x
                    while (down+1, y) in region and (down+1, ny) not in region:
                        down += 1
                    print(f'Addig side for {x, y}: "V" {up, down, y, ny}')
                    sides.add(('V', up, down, y, ny))
                # For vertical sides (dy == 0)
                else:
                    # Look left and right to find where this horizontal segment starts/ends
                    left = y
                    while (x, left-1) in region and (nx, left-1) not in region:
                        left -= 1
                    right = y
                    while (x, right+1) in region and (nx, right+1) not in region:
                        right += 1
                    print(f'Addig side for {x, y}: "H" {left, right, x, nx}')

                    sides.add(('H', left, right, x, nx))

    print(f'Sides {sides}')
    return len(sides)


def calculate_total_price(grid: List[str]) -> int:
    """Calculate the total price for all regions using the new method."""
    regions = find_regions(grid)
    total_price = 0

    # For debugging, print details of each region
    for (plant_type, region_num), region in regions.items():
        area = len(region)
        sides = count_distinct_sides(region, grid)
        print(f'Sides for region {plant_type}{region_num}: {sides}')
        price = area * sides
        total_price += price
        # print(
        #     f"Region {plant_type}{region_num}: Area={area}, Sides={sides}, Price={price}")

    return total_price


# Process actual input
try:
    with open("../data/day12_small.txt", 'r') as file:
        grid = [line.strip() for line in file.readlines()]
    print("\nProcessing input file:")
    print(f"Grid dimensions: {len(grid)}x{len(grid[0])}")
    result = calculate_total_price(grid)
    print(f"Final result: {result}")
except FileNotFoundError:
    print("Input file not found")
except Exception as e:
    print(f"Error processing input: {str(e)}")
