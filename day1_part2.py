row1 = []
row2 = []

with open('/Users/ago/projects/aoc-2024/data/input.txt', 'r') as f:
    for line in f:
        fields = line.split('   ')  # Split on three spaces
        row1.append(int(fields[0]))
        row2.append(int(fields[1][:-1]))

# sort the two rows

sorted1 = sorted(row1)
sorted2 = sorted(row2)

distances = 0

for i, j in zip(sorted1, sorted2):
    distances += abs(i-j)

print(distances)
