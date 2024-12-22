# Classes for different keypads
from itertools import permutations


class DirectionalKeypad:
    def __init__(self):
        # Define the directional keypad layout
        self.layout = {
            (1, 1): '^', (2, 1): 'A',
            (0, 0): '<', (1, 0): 'v', (2, 0): '>'
        }
        # Starting position (A button in upper right)
        self.current_pos = (2, 1)

    def is_valid_move(self, pos):
        """Check if a position is a valid button on the keypad."""
        return pos in self.layout

    def move(self, direction):
        """Move in the specified direction if valid."""
        x, y = self.current_pos
        if direction == '^':
            new_pos = (x, y + 1)
        elif direction == 'v':
            new_pos = (x, y - 1)
        elif direction == '<':
            new_pos = (x - 1, y)
        elif direction == '>':
            new_pos = (x + 1, y)
        else:
            return False

        if self.is_valid_move(new_pos):
            self.current_pos = new_pos
            return True
        return False

    def get_current_button(self):
        """Return the button at current position."""
        return self.layout[self.current_pos]


class NumericKeypad:
    def __init__(self):
        # Define the keypad layout
        self.layout = {
            (0, 2): '7', (1, 2): '8', (2, 2): '9',
            (0, 1): '4', (1, 1): '5', (2, 1): '6',
            (0, 0): '1', (1, 0): '2', (2, 0): '3',
            (1, -1): '0', (2, -1): 'A'
        }

        # Starting position (A button)
        self.current_pos = (2, -1)

    def is_valid_move(self, pos):
        """Check if a position is a valid button on the keypad."""
        return pos in self.layout

    def move(self, direction):
        """
        Move in the specified direction if valid.
        Returns True if move was successful, False otherwise.
        """
        x, y = self.current_pos
        if direction == '^':
            new_pos = (x, y + 1)
        elif direction == 'v':
            new_pos = (x, y - 1)
        elif direction == '<':
            new_pos = (x - 1, y)
        elif direction == '>':
            new_pos = (x + 1, y)
        else:
            return False

        if self.is_valid_move(new_pos):
            self.current_pos = new_pos
            return True
        return False

    def get_current_button(self):
        """Return the button at current position."""
        return self.layout[self.current_pos]


def get_direction_order(keypad_class, current_pos, target_pos=None):
    """
    Determine optimal direction exploration order based on keypad type and positions.
    """
    if isinstance(keypad_class, NumericKeypad):
        # For numeric keypad, prefer vertical movement first when moving between rows
        if target_pos and target_pos[1] != current_pos[1]:
            return ['^', 'v', '<', '>']
        return ['<', '>', '^', 'v']
    else:
        # For directional keypad, maintain consistent ordering
        return ['<', '>', '^', 'v']


def calculate_complexity(code, sequence_length):
    """Calculate complexity for a given code and its sequence length."""
    numeric_part = int(code.rstrip('A'))
    return sequence_length * numeric_part


def forward_sequence(sequence, keypad_class):
    """
    Takes a sequence of inputs on a keypad and returns the sequence of buttons pressed.

    Args:
        sequence: String of directional inputs and button presses (e.g., 'A^A^^>AvvvA')
        keypad_class: Class to use for the keypad (NumericKeypad or DirectionalKeypad)

    Returns:
        String representing the sequence of buttons that would be pressed
    """
    keypad = keypad_class()
    result = []

    # Process each input in the sequence
    for action in sequence:
        if action == 'A':
            # When 'A' is pressed, record the current button
            result.append(keypad.get_current_button())
        else:
            # Otherwise move in the specified direction
            keypad.move(action)

    return ''.join(result)


def find_all_sequences(target_sequence, keypad_class, max_extra_moves=5):
    """
    Find all valid sequences with multiple direction orderings.
    """
    keypad = keypad_class()
    start_pos = keypad.current_pos
    sequences = []
    min_length = float('inf')

    # print(f"\nFinding sequences for target: {target_sequence}")
    # print(f"Starting position: {start_pos}")

    # Try all possible direction orderings
    for direction_order in permutations(['<', '>', '^', 'v']):
        queue = [([], start_pos, 0)]
        visited = set()

        while queue:
            path, pos, target_idx = queue.pop(0)

            if sequences and len(path) > min_length + max_extra_moves:
                continue

            # Try pressing A
            test_keypad = keypad_class()
            test_keypad.current_pos = pos
            current = test_keypad.get_current_button()

            if target_idx < len(target_sequence) and current == target_sequence[target_idx]:
                new_path = path + ['A']

                if target_idx == len(target_sequence) - 1:
                    path_str = ''.join(new_path)
                    if not sequences or len(path_str) <= min_length + max_extra_moves:
                        # print(f"Found valid sequence: {path_str}")
                        sequences.append((path_str, pos))
                        min_length = min(min_length, len(path_str))
                    continue

                state = (pos, target_idx + 1)
                if state not in visited:
                    visited.add(state)
                    queue.append((new_path, pos, target_idx + 1))

            # Try each direction in current ordering
            for direction in direction_order:
                test_keypad = keypad_class()
                test_keypad.current_pos = pos

                if test_keypad.move(direction):
                    new_pos = test_keypad.current_pos
                    state = (new_pos, target_idx)
                    if state not in visited:
                        visited.add(state)
                        queue.append((path + [direction], new_pos, target_idx))

    # print(f"Sequences found: {len(sequences)}")
    sequences = sorted(sequences, key=lambda x: len(x[0]))  # Sort by length
    # for seq, pos in sequences[:5]:  # Show first 5 sequences only
    # print(f"Sequence: {seq}, Final pos: {pos}")

    return sequences


def solve_for_codes(codes):
    """Solve the puzzle for a list of codes and return total complexity."""
    total_complexity = 0

    for code in codes:
        # Get all possible sequences for each level
        level1_sequences = find_all_sequences(code, NumericKeypad)
        # print(f"\nCode: {code}")
        # print(f"Found {len(level1_sequences)} level 1 sequences")

        best_final_sequence = None
        best_length = float('inf')
        best_sequences = None

        # Try each Level 1 sequence
        for level1_seq, _ in level1_sequences:
            # Find all possible Level 2 sequences for this Level 1 sequence
            level2_sequences = find_all_sequences(
                level1_seq, DirectionalKeypad)

            # print(f"Found {len(level2_sequences)} level 2 sequences")

            # Try each Level 2 sequence
            for level2_seq, _ in level2_sequences:
                # Find Level 3 sequence
                level3_sequences = find_all_sequences(
                    level2_seq, DirectionalKeypad)

                # print(f"Found {len(level3_sequences)} level 3 sequences")

                # Check if we found a better combination
                for level3_seq, _ in level3_sequences:
                    if len(level3_seq) < best_length:
                        best_length = len(level3_seq)
                        best_final_sequence = level3_seq
                        best_sequences = (level1_seq, level2_seq, level3_seq)

        if best_sequences:
            level1_seq, level2_seq, level3_seq = best_sequences
            complexity = calculate_complexity(code, len(best_final_sequence))
            total_complexity += complexity

            print(
                f"Level 1 (numeric) sequence length: {len(level1_seq)}, sequence: {level1_seq}")
            print(
                f"Level 2 (robot) sequence length: {len(level2_seq)}, sequence: {level2_seq}")
            print(f"Level 3 (final) sequence length: {len(level3_seq)}")
            print(f"Final sequence: {level3_seq}")
            print(f"Complexity: {complexity}")

            # Verify sequences using forward_sequence
            print("Testing forward sequence:", level3_seq)
            l2_output = forward_sequence(level3_seq, DirectionalKeypad)
            print("Level 2 output:", l2_output)
            l1_output = forward_sequence(l2_output, DirectionalKeypad)
            print("Level 1 output:", l1_output)
            result = forward_sequence(l1_output, NumericKeypad)
            print("Final output:", result)

    print(f"\nTotal complexity: {total_complexity}")
    return total_complexity


# Example usage:
if __name__ == "__main__":
    # Test with example codes
    # example_codes = ["029A"]
    example_codes = ["805A", "964A", "459A", "968A", "671A"]
    print("Testing with example codes:")
    solve_for_codes(example_codes)
