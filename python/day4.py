wordsearch = []

with open("../data/day4.txt", newline='\n') as f:
    for line in f:
        line = line.replace("\n", "")
        wordsearch.append(list(line))


def is_xmas(array: list):
    joined_array = "".join(array)
    return "XMAS" == joined_array


def find_east(row: int, col: int, array: list):
    if col < len(array[row]) - 3:
        to_check = array[row][col:col+4]

        return is_xmas(to_check)
    else:
        return False


def find_west(row: int, col: int, array: list):
    # print(f"Checking west at {row}, {col}")
    # print(to_check)

    if col > 2:
        to_check = array[row][col-3:col+1][::-1]

        return is_xmas(to_check)
    else:
        return False


def find_south(row: int, col: int, array: list):

    if row < len(array) - 3:
        # print(f"Checking south at {row}, {col}")
        to_check = [array[row][col], array[row+1][col],
                    array[row+2][col], array[row+3][col]]

        # print(to_check)
        return is_xmas(to_check)
    else:
        return False


def find_north(row: int, col: int, array: list):

    if row > 2:
        # print(f"Checking north at {row}, {col}")
        to_check = [array[row][col], array[row-1][col],
                    array[row-2][col], array[row-3][col]]

        # print(to_check)
        return is_xmas(to_check)
    else:
        return False


def find_north_east(row: int, col: int, array: list):

    if row > 2 and col < len(array[row]) - 3:
        # print(f"Checking north at {row}, {col}")
        to_check = [array[row][col], array[row-1][col+1],
                    array[row-2][col+2], array[row-3][col+3]]

        # print(to_check)
        return is_xmas(to_check)
    else:
        return False


def find_north_west(row: int, col: int, array: list):

    if row > 2 and col > 2:
        # print(f"Checking north at {row}, {col}")
        to_check = [array[row][col], array[row-1][col-1],
                    array[row-2][col-2], array[row-3][col-3]]

        # print(to_check)
        return is_xmas(to_check)
    else:
        return False


def find_south_east(row: int, col: int, array: list):

    if row < len(array) - 3 and col < len(array[row]) - 3:
        # print(f"Checking north at {row}, {col}")
        to_check = [array[row][col], array[row+1][col+1],
                    array[row+2][col+2], array[row+3][col+3]]

        # print(to_check)
        return is_xmas(to_check)
    else:
        return False


def find_south_west(row: int, col: int, array: list):

    if row < len(array) - 3 and col > 2:
        # print(f"Checking north at {row}, {col}")
        to_check = [array[row][col], array[row+1][col-1],
                    array[row+2][col-2], array[row+3][col-3]]

        # print(to_check)
        return is_xmas(to_check)
    else:
        return False


xmas_num = 0

for i in range(len(wordsearch)):
    for j in range(len(wordsearch[i])):
        if wordsearch[i][j] == "X":
            if find_east(i, j, wordsearch):
                xmas_num += 1
                # print(f"XMAS East found at {i}, {j}")
            if find_west(i, j, wordsearch):
                xmas_num += 1
                # print(f"XMAS West found at {i}, {j}")
            if find_south(i, j, wordsearch):
                xmas_num += 1
                # print(f"XMAS South found at {i}, {j}")
            if find_north(i, j, wordsearch):
                xmas_num += 1
                # print(f"XMAS North found at {i}, {j}")
            if find_north_east(i, j, wordsearch):
                xmas_num += 1
                # print(f"XMAS North East found at {i}, {j}")
            if find_north_west(i, j, wordsearch):
                xmas_num += 1
                # print(f"XMAS North West found at {i}, {j}")
            if find_south_east(i, j, wordsearch):
                xmas_num += 1
                # print(f"XMAS South East found at {i}, {j}")
            if find_south_west(i, j, wordsearch):
                xmas_num += 1
                # print(f"XMAS South West found at {i}, {j}")

    else:
        continue
    break

print(f"XMAS found {xmas_num} times")
