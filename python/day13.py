import re
from math import gcd


def parse_puzzles(file_content: str) -> list:
    puzzles = []
    lines = file_content.strip().split('\n')

    # Process three lines at a time
    for i in range(0, len(lines), 4):
        if i + 2 >= len(lines):
            break

        # Extract numbers using regex
        button_a = re.findall(r'X\+(\d+), Y\+(\d+)', lines[i])[0]
        button_b = re.findall(r'X\+(\d+), Y\+(\d+)', lines[i + 1])[0]
        prize = re.findall(r'X=(\d+), Y=(\d+)', lines[i + 2])[0]

        puzzle = {
            'button_a': {
                'x': int(button_a[0]),
                'y': int(button_a[1]),
                'cost': 3
            },
            'button_b': {
                'x': int(button_b[0]),
                'y': int(button_b[1]),
                'cost': 1
            },
            'prize': {
                'x': 10000000000000 + int(prize[0]),
                'y': 10000000000000 + int(prize[1])
            }
        }
        puzzles.append(puzzle)

    return puzzles


def check_gcd(but_a: int, but_b: int, prize: int) -> int:

    # print(f'Checking {but_a}, {but_b}, {prize}')

    gcd_num = gcd(but_a, but_b)
    print(f'GCD: {gcd_num}')

    if prize % gcd_num == 0:
        return True

    return False


def solve_eqn(puzzle: dict) -> int:

    frac_top = (puzzle['prize']['x'] * puzzle['button_a']['y']) - \
        (puzzle['prize']['y'] * puzzle['button_a']['x'])
    fract_bottom = (puzzle['button_b']['x'] * puzzle['button_a']
                    ['y']) - (puzzle['button_b']['y'] * puzzle['button_a']['x'])

    b_sol = frac_top / fract_bottom
    a_sol = (puzzle['prize']['x'] - (puzzle['button_b']
             ['x'] * b_sol)) / puzzle['button_a']['x']

    return a_sol, b_sol


def sol_satisfies_constraints(a: int, b: int) -> bool:
    if a < 0 or b < 0:
        return False

    # if a > 100 or b > 100:
    #     return False

    if not a.is_integer() or not b.is_integer():
        return False

    return True


def calculate_cost(a: int, b: int) -> int:
    return (a * 3) + (b * 1)


def find_more_sols(puzzle: dict, a_sol: int, b_sol: int) -> list:
    sols = set()

    gcd_1 = gcd(puzzle['button_a']['x'], puzzle['button_b']['x'])
    gcd_2 = gcd(puzzle['button_a']['y'], puzzle['button_b']['y'])

    target_x, target_y = puzzle['prize']['x'], puzzle['prize']['y']

    # Find more solutions

    for k in range(-20, 21):
        a_new_sol = a_sol + k * (puzzle['button_b']['x'] // gcd_1)

        b_new_sol = b_sol - k * (puzzle['button_a']['x'] // gcd_1)

        if sol_satisfies_constraints(a_new_sol, b_new_sol):

            first_sum = a_new_sol * \
                puzzle['button_a']['x'] + b_new_sol * \
                puzzle['button_b']['x'] == target_x
            second_sum = a_new_sol * \
                puzzle['button_a']['y'] + b_new_sol * \
                puzzle['button_b']['y'] == target_y

            if first_sum and second_sum:
                sols.add((a_new_sol, b_new_sol))

    return sorted(list(sols))


# Example usage:
if __name__ == "__main__":
    with open('../data/day13.txt', 'r') as file:
        content = file.read()

    puzzles = parse_puzzles(content)

    costs_sum = 0

    for idx, puzzle in enumerate(puzzles):
        print(f'Puzzle {idx}')

        x_pass = check_gcd(puzzle['button_a']['x'],
                           puzzle['button_b']['x'], puzzle['prize']['x'])
        y_pass = check_gcd(puzzle['button_a']['y'],
                           puzzle['button_b']['y'], puzzle['prize']['y'])

        if x_pass and y_pass:
            # print('Puzzle is solvable!')
            a_sol, b_sol = solve_eqn(puzzle)

            print(f'Base Solution: A = {a_sol}, B = {b_sol}')
            print(f' x pass: {x_pass}, y pass: {y_pass}')
            if sol_satisfies_constraints(a_sol, b_sol):
                # print(f'Solution: A = {a_sol}, B = {b_sol}')

                # generate more sols
                sols = find_more_sols(puzzle, a_sol, b_sol)

                # print(f'Additional solutions: {sols}')

                for sol in sols:
                    costs = []
                    print(f'Additional solution: A = {sol[0]}, B = {sol[1]}')
                    if sol_satisfies_constraints(sol[0], sol[1]):
                        costs.append(calculate_cost(sol[0], sol[1]))

                # print(f'Costs: {costs}')
                cost = min(costs)
                print(f'Puzzle {idx}: {cost}')

                costs_sum += cost
    print(f'Costs sum: {costs_sum}')

    # print(f'X pass: {x_pass}, Y pass: {y_pass}')
