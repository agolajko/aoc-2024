import re

# Input string
# testr = "do()xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))don't()"


testr = ""

with open("../data/day3.txt", newline='\n') as f:
    for line in f:
        line = line.replace("\n", "")
        testr += line

testr = "do()" + testr + "don't()"

pattern = r"mul\((\d+),\s*(\d+)\)"

matches = re.findall(pattern, testr)

print(f"Found {len(matches)} mul() matches")

mul_sum = 0
for match in matches:
    num1, num2 = match
    mul_sum += int(num1) * int(num2)

print(f"Part 1: Sum of all multiplications: {mul_sum}")

# Regular expressions to capture substrings
between_dont_and_do = r"don't\(\)(.*?)do\(\)"
between_do_and_dont = r"do\(\)(.*?)don't\(\)"

# Find all matches for each case
donts = re.findall(between_dont_and_do, testr, re.DOTALL)
dos = re.findall(between_do_and_dont, testr, re.DOTALL)

# Display the results
# print("Strings between don't() and do():", donts)
# print("Strings between do() and don't():", dos)

# join emelents of list2
joined_dos = "".join(dos)


pattern = r"mul\((\d+),\s*(\d+)\)"

matches = re.findall(pattern, joined_dos)

print(f"Found {len(matches)} do matches")

mul_sum = 0
for match in matches:
    num1, num2 = match
    mul_sum += int(num1) * int(num2)

print(f"Part 2: Sum of all multiplications discarding the don'ts : {mul_sum}")
