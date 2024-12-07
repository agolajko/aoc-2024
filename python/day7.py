from itertools import product


results = []
inputs = []

with open("../data/day7.txt", newline='\n') as f:
    for line in f:
        line = line.strip()
        results_num, inputs_num = line.split(":")
        results.append(int(results_num))
        inputs.append([int(i) for i in inputs_num.split()])


def generate_all_combinations(num_op: int):
    input_chars = ['+', '*', '||']

    op_combinations = list(product(input_chars, repeat=num_op))
    # for i in range(len(op_combinations)):

    # print(f'Comb {i}: {op_combinations[i]}')
    return op_combinations


def try_all_combinations(result: int, input_nums: list):

    num_operators = len(input_nums)-1
    num_combinations = 2**num_operators
    # print(
    #     f"Num operators: {num_operators}, Num combinations: {num_combinations}")

    all_combinations = generate_all_combinations(num_operators)

    # print(all_combinations[0])
    # print(all_combinations[-1])

    for combination in all_combinations:
        current_result = input_nums[0]
        for i in range(num_operators):
            # print(f'Current i: {i}/{num_combinations}')
            if combination[i] == '+':
                current_result += input_nums[i+1]
            elif combination[i] == '*':
                current_result *= input_nums[i+1]
            elif combination[i] == '||':
                current_result = int(
                    str(current_result) + str(input_nums[i+1]))

        if current_result == result:
            # print(f"Found match: {input_nums} {combination} {result}")
            return 1
    return 0


if __name__ == "__main__":
    found_matches = 0
    match_sum = 0
    for i in range(len(results)):
        if i % 100 == 0:
            print(f"Current iteration: {i}/{len(results)}")

        if try_all_combinations(results[i], inputs[i]):
            found_matches += 1
            match_sum += results[i]

    print("Number of matches: ", found_matches)
    print("Sum of matches: ", match_sum)
