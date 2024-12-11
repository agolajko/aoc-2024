import psutil
from typing import Dict


def read_stones(filepath: str) -> Dict[int, int]:
    """Read stones and return as a dictionary of frequencies."""
    stones = {}
    with open(filepath) as f:
        for line in f:
            for num in map(int, line.strip().split()):
                stones[num] = stones.get(num, 0) + 1
    return stones


def step_forward(stone_counts: Dict[int, int]) -> Dict[int, int]:
    """Process stones using dictionary to handle large numbers efficiently."""
    new_stones = {}

    for stone, count in stone_counts.items():
        if stone == 0:
            new_stones[1] = new_stones.get(1, 0) + count
        else:
            str_stone = str(stone)
            if len(str_stone) % 2 == 0:
                mid = len(str_stone) // 2
                first_half = int(str_stone[:mid])
                second_half = int(str_stone[mid:])
                new_stones[first_half] = new_stones.get(first_half, 0) + count
                new_stones[second_half] = new_stones.get(
                    second_half, 0) + count
            else:
                new_val = (stone * 2024) % (10**18)
                new_stones[new_val] = new_stones.get(new_val, 0) + count

    return new_stones


def process_stones(filepath: str, steps: int) -> int:
    """Process stones tracking frequencies using a dictionary."""
    stones = read_stones(filepath)

    for step in range(steps):
        stones = step_forward(stones)
        total_stones = sum(stones.values())
        print(f'Step {step + 1}: {total_stones} stones')

        if total_stones > 10**9:
            print(
                f"Warning: Stone count exceeding safe limits at step {step + 1}")

    total = sum(stones.values())
    print(f'Final stone count: {total}')
    return total


# Optional: Add memory tracking


def memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024  # In MB


# Usage with memory tracking
if __name__ == "__main__":
    print(f"Initial memory usage: {memory_usage():.2f} MB")
    result = process_stones("../data/day11.txt", 75)
    print(f"Final memory usage: {memory_usage():.2f} MB")
