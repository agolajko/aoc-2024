#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct
{
    long long int result;   // The number before the colon
    int *numbers;           // Array of numbers after the colon
    int count;              // Current count of numbers
    long long int capacity; // Current capacity of numbers array
} Entry;

typedef struct
{
    Entry *entries;
    int size;
    long int capacity;
} Database;

#define MAX_LINES 1024
#define MAX_NUMBERS_PER_LINE 40

void addNumberToEntry(Entry *entry, int number)
{
    // If we need more space
    if (entry->count >= entry->capacity)
    {
        entry->capacity = entry->capacity == 0 ? 2 : entry->capacity * 2;
        entry->numbers = (int *)realloc(entry->numbers, entry->capacity * sizeof(int));
    }
    entry->numbers[entry->count++] = number;
}

// Create a new empty entry with just the result
void createEntry(Database *db, long long int result)
{

    if (db->size >= db->capacity)
    {
        db->capacity *= 2;
        Entry *new_entries = (Entry *)realloc(db->entries, db->capacity * sizeof(Entry));
        if (new_entries == NULL)
        {
            printf("Memory allocation failed\n");
            return;
        }
        db->entries = new_entries;
    }
    Entry *entry = &db->entries[db->size++];
    entry->result = result;
    entry->numbers = NULL;
    entry->count = 0;
    entry->capacity = 0;
}

int read_numbers_from_file(const char *filename, Database *db)

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
        char *token = strtok(line, ":");

        long long int first_num = atoll(token);
        // printf("Line: %d First num: %lld\n", line_count, first_num);
        createEntry(db, first_num);

        token = strtok(NULL, " ");

        while (token != NULL && num_count < MAX_NUMBERS_PER_LINE)
        {

            int next_num = atoi(token);
            addNumberToEntry(&db->entries[db->size - 1], next_num);

            // printf("Next num: %d\n", next_num);
            token = strtok(NULL, " \n");

            // numbers[line_count][num_count++] = atoi(token);
        }
        // line_sizes[line_count] = num_count;
        line_count++;
    }
    // printf("Read %d entries from the file.\n", db->size);

    fclose(file);
    return line_count; // Return the number of lines read
}

int *generate_combinations(int num_digits, int base, int *total_combinations)
{
    *total_combinations = pow(base, num_digits);
    int *combinations = (int *)malloc((*total_combinations) * num_digits * sizeof(int));

    for (int i = 0; i < *total_combinations; i++)
    {
        int num = i;
        for (int j = num_digits - 1; j >= 0; j--)
        {
            combinations[i * num_digits + j] = num % base; // Store digit
            num /= base;                                   // Move to next digit
        }
    }

    return combinations;
}

void print_combinations(int *combinations, int num_digits, int total_combinations)
{
    for (int i = 0; i < total_combinations; i++)
    {
        for (int j = 0; j < num_digits; j++)
        {
            printf("%d", combinations[i * num_digits + j]);
        }
        printf("\n");
    }
}

long long int concatenate_numbers(long long int num1, long long int num2)
{
    // Convert numbers to strings
    char str1[20], str2[20];
    sprintf(str1, "%lld", num1);
    sprintf(str2, "%lld", num2);

    // Concatenate strings
    char result_str[40];
    strcpy(result_str, str1);
    strcat(result_str, str2);

    // Convert the result back to an integer
    return atoll(result_str);
}

int try_all_combinations(int *combinations, int comb_len, int *numbers, int total_combinations, long long int result)
{
    for (int i = 0; i < total_combinations; i++)
    {
        long long int current_result = numbers[0];
        for (int j = 0; j < comb_len; j++)
        {
            int current_number = numbers[j + 1];
            int current_operator = combinations[i * comb_len + j];

            if (current_operator == 0)
            {
                current_result += current_number;
            }
            else if (current_operator == 1)
            {
                current_result *= current_number;
            }
            else if (current_operator == 2)
            {
                current_result = concatenate_numbers(current_result, current_number);
            }
            else
            {
                printf("Invalid operator: %d\n", current_operator);
            }
        }
        if (current_result == result)
        {
            // printf("Found a match: %lld\n", current_result);

            return 1;
        }
    }
    return 0;
}

int main()
{

    Database db;
    db.entries = (Entry *)malloc(1000 * sizeof(Entry));
    db.size = 0;
    db.capacity = 2000;

    const char *filename = "../data/day7.txt";

    read_numbers_from_file(filename, &db);

    printf("Read %d entries from the file.\n", db.size);
    printf("DB capacity is %ld.\n", db.capacity);

    int found_matches = 0;

    long long int sum_res = 0;

    for (int i = 0; i < db.size; i++)
    {

        int num_digits = db.entries[i].count - 1; // Length of combinations
        int base = 3;                             // Number of distinct values (0, 1, 2)
        int total_combinations;

        // Generate combinations
        int *combinations = generate_combinations(num_digits, base, &total_combinations);

        int found_comb;

        found_comb = try_all_combinations(combinations, num_digits, db.entries[i].numbers, total_combinations, db.entries[i].result);

        if (found_comb)
        {
            found_matches++;
            sum_res += db.entries[i].result;
        }

        free(combinations);
    }

    printf("Found %d matches.\n", found_matches);
    printf("Sum of results: %lld\n", sum_res);

    for (int i = 0; i < db.size; i++)
    {
        free(db.entries[i].numbers);
    }
    free(db.entries);
}