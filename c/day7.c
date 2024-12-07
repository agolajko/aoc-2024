#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

    // for (int i = 0; i < 9; i++)
    // {
    //     printf("Entry %d: %d\n", i, db.entries[i].result);
    //     for (int j = 0; j < db.entries[i].count; j++)
    //     {
    //         printf("%d \n", db.entries[i].numbers[j]);
    //     }
    //     printf("\n");
    // }

    for (int i = 0; i < db.size; i++)
    {
        free(db.entries[i].numbers);
    }
    free(db.entries);
}