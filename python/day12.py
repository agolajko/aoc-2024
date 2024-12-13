
input_map = []


with open("../data/day12_small.txt", newline='\n') as f:
    for line in f:
        line = line.strip()

        input_map.append(list(line))


def flood_fill(space: list, i: int, j: int, unique_letters: dict, regions: dict, visited: set, region_no: int):

    direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # print(f'Curr idx {idx}')
    for d in direction:
        if 0 <= i+d[0] < len(space) and 0 <= j+d[1] < len(space[i]):
            if space[i+d[0]][j+d[1]] == space[i][j]:
                if (i+d[0], j+d[1]) not in visited:
                    visited.add((i+d[0], j+d[1]))
                    # regions[region_no] = [(i, j), (i+d[0], j+d[1])]
                    regions[region_no].append((i+d[0], j+d[1]))

                    unique_letters, regions, visited = flood_fill(
                        space, i+d[0], j+d[1], unique_letters, regions, visited, region_no)

    return unique_letters, regions, visited


def loop_over(space: list):
    unique_letters = {}
    regions = {}
    visited = set()

    for i in range(len(space)):
        for j in range(len(space[i])):
            # print(f'Checking {i}, {j}')
            # print(f'Current letter: {space[i][j]}')
            # print(f'Unique letters: {unique_letters}')
            # print(f'Regions: {regions}')
            curr_letter = space[i][j]

            if (i, j) not in visited:
                visited.add((i, j))

                region_no = len(regions.keys())+1

                if curr_letter not in unique_letters.keys():
                    unique_letters[curr_letter] = []
                unique_letters[curr_letter].append(region_no)
                regions[region_no] = [(i, j)]

                unique_letters, regions, visited = flood_fill(
                    space, i, j, unique_letters, regions, visited, region_no)
            else:
                continue

    return unique_letters, regions, visited


def calculate_perimeter(coordinates):
    perimeter = 0

    # For each square, check all four sides
    for x, y in coordinates:
        # Check each adjacent position
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            # If there's no square at this adjacent position,
            # this edge contributes to the perimeter
            if (x + dx, y + dy) not in coordinates:
                perimeter += 1

    return perimeter


def calculate_area(coordinates):
    return len(coordinates)


def calculate_area_perimeter(coordinates):
    return calculate_area(coordinates) * calculate_perimeter(coordinates)


def find_sides(coordinates):
    coordinates = set(coordinates)  # Convert to set for faster lookup
    edges = set()

    for x, y in coordinates:
        # Check right and down
        for dx, dy in [(0, 1), (1, 0)]:
            adj_x, adj_y = x + dx, y + dy
            if (adj_x, adj_y) not in coordinates:
                # Found an exposed edge
                if dx == 0:  # Vertical edge
                    edge = ((x, min(y, adj_y)), (x, max(y, adj_y)))
                else:  # Horizontal edge
                    edge = ((min(x, adj_x), y), (max(x, adj_x), y))
                edges.add(edge)

        # Only check left if we're at an edge
        left = (x-1, y)
        if left not in coordinates:
            edge = ((x, y), (x+1, y))  # Horizontal edge
            edges.add(edge)

    # Rest of the code same as before...
    sides = []
    remaining_edges = set(edges)

    while remaining_edges:
        current_side = []
        current_edge = remaining_edges.pop()
        current_side.append(current_edge)

        while True:
            found_connection = False
            for edge in remaining_edges:
                if edge[0] == current_side[-1][1]:  # Connected at end
                    current_side.append(edge)
                    remaining_edges.remove(edge)
                    found_connection = True
                    break
                elif edge[1] == current_side[0][0]:  # Connected at start
                    current_side.insert(0, edge)
                    remaining_edges.remove(edge)
                    found_connection = True
                    break
            if not found_connection:
                break

        sides.append(current_side)

    return len(sides), sides


def calculate_area_sides(coordinates):
    num_sides, side_list = find_sides(coordinates)
    area_sides_sum = 0

    area = calculate_area(coordinates)

    print(f'Area, sides: {area} {num_sides}')

    return area * num_sides


unique_letters, regions, visited = loop_over(input_map)
# print(f'Visited: {visited}')
# print(f'Len visited: {len(visited)}')
print(f'Unique letters: {unique_letters}')
# print(f'Regions: {regions}')
print(f'Number of regions: {len(regions.keys())}')

area_perimeter_sum = 0
area_sides_sum = 0

for k, v in regions.items():

    print(f'Calculating for letter {k}')
    print(f'Coordinates: {v}')
    area_perimeter_sum += calculate_area_perimeter(v)
    area_sides_sum += calculate_area_sides(v)


print(f'Area * Perimeter sum: {area_perimeter_sum}')
print(f'Area * Sides sum: {area_sides_sum}')
