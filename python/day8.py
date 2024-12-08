antenna = []


with open("../data/day8.txt", newline='\n') as f:
    for line in f:
        line = line.strip()
        # print(line)
        antenna.append(list(line))


def create_dict(antenna_arr: list):
    antenna_dict = {}
    for i in range(len(antenna_arr)):
        for j in range(len(antenna_arr[i])):
            if antenna_arr[i][j] != '.':
                if antenna_arr[i][j] not in antenna_dict:
                    antenna_dict[antenna_arr[i][j]] = []
                # print(f"Checking {i} {j}, value: {antenna_arr[i][j]}")
                antenna_dict[antenna_arr[i][j]].append((i, j))
    return antenna_dict


def find_symmetry(antenna_arr: list, letter: str, loc1: tuple, loc2: tuple):
    print(f"Checking {loc1} {loc2}")

    dir_vect = (loc2[0] - loc1[0], loc2[1] - loc1[1])

    new_loc1 = (loc1[0] - dir_vect[0],
                loc1[1] - dir_vect[1])

    print(f"New loc1: {new_loc1}")

    new_loc2 = (loc2[0] + dir_vect[0],
                loc2[1] + dir_vect[1])

    print(f"New loc2: {new_loc2}")

    antenna_width = len(antenna_arr[0])
    antenna_height = len(antenna_arr)

    return_list = []

    if new_loc1[0] >= 0 and new_loc1[0] < antenna_height and new_loc1[1] >= 0 and new_loc1[1] < antenna_width:
        return_list.append(new_loc1)
        # return_list += 1

    if new_loc2[0] >= 0 and new_loc2[0] < antenna_height and new_loc2[1] >= 0 and new_loc2[1] < antenna_width:
        return_list.append(new_loc2)
        # return_list += 1

    return return_list


if __name__ == "__main__":

    antenna_dict = create_dict(antenna)
    print(antenna_dict)

    ret_list = []

    for letter in antenna_dict:
        print(f"Checking letter {letter}")
        if len(antenna_dict[letter]) >= 2:
            print(f"Found {len(antenna_dict[letter])} {letter}")

            for i in range(len(antenna_dict[letter])):
                for j in range(i+1, len(antenna_dict[letter])):
                    print(
                        f"Checking {antenna_dict[letter][i]} {antenna_dict[letter][j]}")
                    ret_list.append(find_symmetry(
                        antenna, letter, antenna_dict[letter][i], antenna_dict[letter][j]))
        else:
            print(f"Found 1 {letter}")

    # print(ret_list)
    final_list = set()
    for i in ret_list:
        for j in i:
            final_list.add(j)
    # print(sum(ret_list))

    # print(final_list)
    print(len(final_list))
