#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LINES 1024
#define MAX_CHARACTERS_PER_LINE 200

int read_characters_from_file(const char *filename, char characters[MAX_LINES][MAX_CHARACTERS_PER_LINE], int line_sizes[MAX_LINES])
{
    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        perror("Error opening file");
        return -1;
    }

    char line[1024];
    int line_count = 0;

    while (fgets(line, sizeof(line), file) != NULL && line_count < MAX_LINES)
    {
        int char_count = 0;
        for (int i = 0; line[i] != '\0' && line[i] != '\n'; i++)
        {
            if (char_count < MAX_CHARACTERS_PER_LINE)
            {
                characters[line_count][char_count++] = line[i];
            }
        }
        line_sizes[line_count] = char_count;
        line_count++;
    }

    fclose(file);
    return line_count; // Return the number of lines read
}

// Function to print the stored numbers
void print_chars(char characters[MAX_LINES][MAX_CHARACTERS_PER_LINE], int line_sizes[MAX_LINES], int line_count)
{
    for (int i = 0; i < line_count; i++)
    {
        printf("Line %d: ", i + 1);
        for (int j = 0; j < line_sizes[i]; j++)
        {
            printf("%c ", characters[i][j]);
        }
        printf("\n");
    }
}

bool is_mas(char char_array[3])
{
    if (char_array[0] == 'M' && char_array[1] == 'A' && char_array[2] == 'S')
    {
        return true;
    }
    return false;
}

bool find_mas_north_east(int row, int col, char characters[MAX_LINES][MAX_CHARACTERS_PER_LINE], int line_sizes[MAX_LINES], int line_count)
{
    if (row > 0 && row < line_count - 1 && col > 0 && col < line_sizes[row] - 1)
    {
        char mas[3] = {characters[row - 1][col + 1], characters[row][col], characters[row + 1][col - 1]};
        return is_mas(mas);
    }
    return false;
}

int main()
{
    const char *filename = "../data/day4_small.txt";
    char characters[MAX_LINES][MAX_CHARACTERS_PER_LINE];
    int line_sizes[MAX_LINES]; // To store the number of elements in each line

    int line_count = read_characters_from_file(filename, characters, line_sizes);
    if (line_count == -1)
    {
        return 1; // Exit if there was an error reading the file
    }

    int mon_counter = 0;
    printf("Read %d lines from the file.\n", line_count);
    // print_chars(characters, line_sizes, line_count);

    for (int i = 0; i < line_count; i++)
    {
        for (int j = 0; j < line_sizes[i]; j++)
        {
            if (characters[i][j] == 'A')
            {
                // printf("Found A at %d, %d\n", i, j);
                if (find_mas_north_east(i, j, characters, line_sizes, line_count))
                {
                    printf("Found MAS at %d, %d\n", i, j);
                }
            }
        }
        // printf("\n");
    }
}