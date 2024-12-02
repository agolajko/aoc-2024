records = []

with open("../data/day2.txt", newline='\n') as f:
    for line in f:
        line = line.replace("\n", "")
        fields = line.split(' ')
        fields = [int(i) for i in fields]
        records.append(fields)

# record2 = [[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1],
#            [1, 3, 2, 4, 5], [8, 6, 4, 4, 1], [1, 3, 6, 7, 9]]


def subtract_self(arr):
    subtracted_records = []
    for j in range(len(arr)-1):
        subtracted_records.append(arr[j] - arr[j+1])
    return subtracted_records


def check_dec_distance(arr):
    checked_arrray = []
    accepted_distance = [-3, -2, -1]

    for i in arr:
        checked_arrray.append(i in accepted_distance)
    return checked_arrray


def check_inc_distance(arr):
    checked_arrray = []

    accepted_distance = [1, 2, 3]

    for i in arr:
        checked_arrray.append(i in accepted_distance)
    return checked_arrray


def monotonic(arr):

    subtracted = subtract_self(arr)
    return (all(check_dec_distance(subtracted)) or all(check_inc_distance(subtracted)))


passes_without_mods = 0
passes_with_mods = 0
for rec in records:
    # check if it passes without modifications
    if monotonic(rec):
        passes_without_mods += 1
    else:
        # iterate through and remove each element
        for i in range(len(rec)):
            temp = rec.copy()
            temp.pop(i)
            if monotonic(temp):
                passes_with_mods += 1
                break

# 463
# 514

print(
    f"From the loaded records {passes_without_mods} are safe, which increases to {passes_without_mods+passes_with_mods} with modifications")
