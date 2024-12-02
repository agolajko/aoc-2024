from collections import Counter

# row1 = [3, 4, 2, 1, 3, 3]
# row2 = [4, 3, 5, 3, 9, 3]


row1 = []
row2 = []

with open("../data/day1.txt", "r") as f:
    for line in f:
        fields = line.split('   ')  # Split on three spaces
        row1.append(int(fields[0]))
        row2.append(int(fields[1][:-1]))


distances = 0

dict2 = Counter(row2)

for i in row1:
    if i in dict2:
        distances += i*dict2[i]

print(distances)
