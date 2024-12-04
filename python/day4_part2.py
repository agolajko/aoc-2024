wordsearch = []

with open("../data/day4.txt", newline='\n') as f:
    for line in f:
        line = line.replace("\n", "")
        wordsearch.append(list(line))


def is_mas(array1: list):
    return ['M', 'A', 'S'] == array1


def find_mas_north_east(row: int, col: int, array: list):

    if 0 < row < len(array)-1 and 0 < col < len(array[row])-1:
        # print(f"Checking north at {row}, {col}")
        to_check = [array[row-1][col+1], array[row][col],
                    array[row+1][col-1]]

        # print(to_check)
        return is_mas(to_check)
    else:
        return False


def find_mas_north_west(row: int, col: int, array: list):

    if 0 < row < len(array)-1 and 0 < col < len(array[row])-1:
        # print(f"Checking north at {row}, {col}")
        to_check = [array[row-1][col-1], array[row][col],
                    array[row+1][col+1]]

        # print(to_check)
        return is_mas(to_check)
    else:
        return False


def find_mas_south_east(row: int, col: int, array: list):

    if 0 < row < len(array)-1 and 0 < col < len(array[row])-1:
        # print(f"Checking north at {row}, {col}")
        to_check = [array[row+1][col+1], array[row][col],
                    array[row-1][col-1]]

        # print(to_check)
        return is_mas(to_check)
    else:
        return False


def find_mas_south_west(row: int, col: int, array: list):

    if 0 < row < len(array)-1 and 0 < col < len(array[row])-1:
        # print(f"Checking north at {row}, {col}")
        to_check = [array[row+1][col-1], array[row][col],
                    array[row-1][col+1]]

        # print(to_check)
        return is_mas(to_check)
    else:
        return False


xmas_num = 0

for i in range(len(wordsearch)):
    for j in range(len(wordsearch[i])):
        if wordsearch[i][j] == "A":

            x_found = 0

            if find_mas_north_east(i, j, wordsearch):
                x_found += 1
                # print(f"XMAS North East found at {i}, {j}")
            if find_mas_north_west(i, j, wordsearch):
                x_found += 1
                # print(f"XMAS North West found at {i}, {j}")
            if find_mas_south_east(i, j, wordsearch):
                x_found += 1
                # print(f"XMAS South East found at {i}, {j}")
            if find_mas_south_west(i, j, wordsearch):
                x_found += 1
                # print(f"XMAS South West found at {i}, {j}")

            if x_found == 2:
                xmas_num += 1
            # print(f"MAS found {x_found} times")

    else:
        continue
    break

print(f"X-MAS found {xmas_num} times")
