from collections import defaultdict, deque


rules = []
update_list = []

after_break = False

with open("../data/day5.txt", newline='\n') as f:
    for line in f:
        line = line.strip()

        if line != '':
            if after_break == False:
                # print(line)
                rule = line.split("|")
                rules.append((int(rule[0]), int(rule[1])))

            if after_break == True:
                line = line.strip()
                update_list.append([int(i) for i in str(line).split(",")])
        if line == '':  # This checks if the line is empty
            # print("Found empty line!")
            after_break = True


def check_sequence_rules(update_inst, rules_list):

    upd_positions = {num: idx for idx, num in enumerate(update_inst)}

    # Check each rule
    for before, after in rules_list:
        # Check if 'before' appears before 'after'
        if before in upd_positions and after in upd_positions:
            if upd_positions[before] > upd_positions[after]:
                return False

    return True


def reorder_list(update_inst, rules_list):
    # print("Before: ", update_inst)
    # Check each rule

    for i in range(len(update_inst)):
        for before, after in rules_list:
            upd_positions = {num: idx for idx, num in enumerate(update_inst)}

            # Check if 'before' appears before 'after'
            if before in upd_positions and after in upd_positions:
                if upd_positions[before] > upd_positions[after]:
                    # Swap the two values
                    before_idx = upd_positions[before]
                    after_idx = upd_positions[after]

                    update_inst[before_idx], update_inst[after_idx] = update_inst[after_idx], update_inst[before_idx]
    # print("After: ", update_inst)
    return update_inst


def reorder_sequence(numbers, rules):

    # Build graph and calculate in-degrees
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    numbers_set = set(numbers)

    # Initialize all numbers with 0 in-degree
    for num in numbers:
        in_degree[num] = 0

    # Build the graph and calculate in-degrees
    for before, after in rules:
        if before in numbers_set and after in numbers_set:

            graph[before].append(after)
            in_degree[after] += 1

    # print('Graph:')
    # print(graph)

    # print('In-degree:')
    # print(in_degree)

    # Initialize queue with all nodes that have no incoming edges
    queue = deque([num for num in numbers if in_degree[num] == 0])

    # print('Queue:')
    # print(queue)

    # Process the queue
    result = []
    while queue:
        current = queue.popleft()
        result.append(current)

        # Process neighbors
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If result length doesn't match input length, there's a cycle
    if len(result) != len(numbers):
        print("Cycle detected!")
        print(numbers)
        print(result)
        print(len(result))
        print(len(numbers))
        return None

    return result


def count_middle():
    right_oder = 0
    sum_middle = 0
    reorder_middle = 0
    for i in range(len(update_list)):
        # print(update_list[i])
        if check_sequence_rules(update_list[i], rules):
            right_oder += 1
            middle_num = update_list[i][len(update_list[i])//2]
            sum_middle += middle_num
        else:
            # print("No right order")
            reordered_list = reorder_sequence(update_list[i], rules)
            # print(reordered_list)
            middle_num = reordered_list[len(reordered_list)//2]
            reorder_middle += middle_num

    print(right_oder)
    print(sum_middle)
    print(reorder_middle)


if __name__ == "__main__":
    count_middle()
