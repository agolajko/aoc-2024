import re


def read_file() -> list:
    with open('../data/day19.txt', 'r') as file:
        file_content = file.read()

        blocks = []
        test_words = []
        lines = file_content.strip().split('\n')

        # Process three lines at a time
        for i in range(0, len(lines)):

            if i == 0:
                pattern = r'([a-z]+)(?:,\s*)?'

                blocks = re.findall(
                    pattern, lines[i])

            elif i > 1:
                test_words.append(lines[i])

    return blocks, test_words


def can_form_word(target, blocks, used=None, start=0):
    """
    Check if target word can be formed using given blocks.

    Args:
        target (str): Target word to form
        blocks (list): List of available blocks
        used (set): Set of indices of used blocks
        start (int): Current position in target word

    Returns:
        bool: True if word can be formed, False otherwise
    """

    # Base case: if we've matched the entire target, we're successful
    if start >= len(target):
        return True

    # Try each building block
    for i, block in enumerate(blocks):

        # Check if this block could match at current position
        if start + len(block) <= len(target):
            if target[start:start + len(block)] == block:
                # Try using this block
                if can_form_word(target, blocks, used, start + len(block)):
                    return True

    return False


def count_formations(target: str, blocks: list, start: int = 0, path: list = None) -> int:

    if path is None:
        path = []

    # Base case: if we've matched the entire target, we found a valid formation
    if start >= len(target):
        # Uncomment to see the individual combinations:
        # print(f"Found formation: {' + '.join(path)}")
        return 1

    # Count total formations using each possible block at this position
    total_formations = 0
    for block in blocks:
        if (start + len(block) <= len(target) and
                target[start:start + len(block)] == block):
            # Try this block and count formations for rest of word
            path.append(block)
            total_formations += count_formations(
                target, blocks, start + len(block), path.copy())
            path.pop()

    return total_formations


blocks, test_words = read_file()

# print(blocks)
# print(test_words)

# Check each word
num_formable_words = 0
variations_per_word = 0
for idx, word in enumerate(test_words):
    print(f"Checking word {idx}: {len(test_words)}")

    result = can_form_word(word, blocks)
    num_forms = count_formations(word, blocks)
    variations_per_word += num_forms
    num_formable_words += result
    # print(f"{word}: {'Can' if result else 'Cannot'} be formed")

print(f"Number of formable words: {num_formable_words}")
print(f"Total variations: {variations_per_word}")
