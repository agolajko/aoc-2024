#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LINES 1024
#define MAX_NUMBERS_PER_LINE 20

// Function to read numbers from a file and store them in an array of arrays
int read_numbers_from_file(const char *filename, int numbers[MAX_LINES][MAX_NUMBERS_PER_LINE], int line_sizes[MAX_LINES])
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
        int num_count = 0;
        char *token = strtok(line, " \t\n");
        while (token != NULL && num_count < MAX_NUMBERS_PER_LINE)
        {
            numbers[line_count][num_count++] = atoi(token);
            token = strtok(NULL, " \t\n");
        }
        line_sizes[line_count] = num_count;
        line_count++;
    }

    fclose(file);
    return line_count; // Return the number of lines read
}

// Function to print the stored numbers
void print_numbers(int numbers[MAX_LINES][MAX_NUMBERS_PER_LINE], int line_sizes[MAX_LINES], int line_count)
{
    for (int i = 0; i < line_count; i++)
    {
        printf("Line %d: ", i + 1);
        for (int j = 0; j < line_sizes[i]; j++)
        {
            printf("%d ", numbers[i][j]);
        }
        printf("\n");
    }
}

int subtract_self(int arr[MAX_NUMBERS_PER_LINE], int copy_arr[MAX_NUMBERS_PER_LINE], int no_elements)
{
    for (int i = 0; i < no_elements - 1; i++)
    {
        copy_arr[i] = arr[i] - arr[i + 1];
    }
    return 0;
}

bool is_in_list(int *array, int size, int target)
{
    for (int i = 0; i < size; i++)
    {
        // printf("Checking %d is %d", target, array[i]);
        if (array[i] == target)
        {
            return true;
        }
    }
    return false;
}

int check_dec_distance(int arr[MAX_NUMBERS_PER_LINE], int copy_arr[MAX_NUMBERS_PER_LINE], int no_elements)
{
    int accepted_distance[] = {1, 2, 3};
    for (int i = 0; i < no_elements; i++)
    {
        if (is_in_list(accepted_distance, 3, arr[i]))
        {
            copy_arr[i] = 1;
        }
    }

    return 0;
}

int check_inc_distance(int arr[MAX_NUMBERS_PER_LINE], int copy_arr[MAX_NUMBERS_PER_LINE], int no_elements)
{
    int accepted_distance[] = {-1, -2, -3};
    for (int i = 0; i < no_elements; i++)
    {
        if (is_in_list(accepted_distance, 3, arr[i]))
        {
            copy_arr[i] = 1;
        }
    }
    return 0;
}

int monotonic(int arr[MAX_NUMBERS_PER_LINE], int no_elements)
{
    int inc_arr[MAX_NUMBERS_PER_LINE] = {0};
    int dec_arr[MAX_NUMBERS_PER_LINE] = {0};

    int monotonic_either_way = 1;

    check_inc_distance(arr, inc_arr, no_elements);
    check_dec_distance(arr, dec_arr, no_elements);

    int mon_inc = 1;
    int mon_dec = 1;

    for (int i = 0; i < no_elements; i++)
    {
        mon_inc &= inc_arr[i];
        mon_dec &= dec_arr[i];
    }

    monotonic_either_way = mon_inc || mon_dec;
    return monotonic_either_way;
}

void remove_element(int arr[MAX_NUMBERS_PER_LINE], int copy_arr[MAX_NUMBERS_PER_LINE], int no_elements, int index)
{
    // printf("Removing element at index %d\n", index);
    for (int i = 0; i < no_elements; i++)
    {
        if (i < index)
        {
            copy_arr[i] = arr[i]; // Copy elements before the index
        }
        else if (i < no_elements - 1)
        {
            copy_arr[i] = arr[i + 1]; // Skip the element at 'index'
        }
        else
        {
            copy_arr[i] = 0; // Optional: Initialize the remaining part
        }
    }
}
int main()
{
    const char *filename = "../data/day2.txt";
    int numbers[MAX_LINES][MAX_NUMBERS_PER_LINE];
    int line_sizes[MAX_LINES]; // To store the number of elements in each line

    int line_count = read_numbers_from_file(filename, numbers, line_sizes);
    if (line_count == -1)
    {
        return 1; // Exit if there was an error reading the file
    }

    int mon_counter = 0;
    printf("Read %d lines from the file.\n", line_count);

    for (int i = 0; i < line_count; i++)
    {
        int sub_arr[MAX_NUMBERS_PER_LINE];
        subtract_self(numbers[i], sub_arr, line_sizes[i]);

        int monotonic_either = monotonic(sub_arr, line_sizes[i] - 1);

        if (monotonic_either)
        {
            mon_counter++;
        }
        else
        {
            for (int j = 0; j < line_sizes[i]; j++)
            {

                int copy_permute[MAX_NUMBERS_PER_LINE] = {0};

                remove_element(numbers[i], copy_permute, line_sizes[i], j);

                int sub_arr2[MAX_NUMBERS_PER_LINE];
                subtract_self(copy_permute, sub_arr2, line_sizes[i] - 1);

                int monotonic_either2 = monotonic(sub_arr2, line_sizes[i] - 2);

                if (monotonic_either2)
                {
                    mon_counter++;
                    break;
                }
            }
        }
    }

    printf("Monotonic either way: %d\n", mon_counter);

    return 0;
}
