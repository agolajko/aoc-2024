#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int from;
    int to;
} Relation;

typedef struct
{
    int *numbers; // Pointer to the list of numbers
    int size;     // Number of elements in the list
} NumberList;

void add_relation(Relation **relations, int *count, int *capacity, int from, int to)
{
    if (*count == *capacity)
    {
        *capacity = (*capacity == 0) ? 10 : (*capacity * 2); // Increase capacity
        *relations = realloc(*relations, (*capacity) * sizeof(Relation));
        if (*relations == NULL)
        {
            perror("Failed to allocate memory");
            exit(EXIT_FAILURE);
        }
    }
    (*relations)[*count].from = from;
    (*relations)[*count].to = to;
    (*count)++;
}

void add_list(NumberList **all_lists, int *list_count, int *capacity, int *numbers, int size)
{
    if (*list_count == *capacity)
    {
        *capacity = (*capacity == 0) ? 10 : (*capacity * 2); // Increase capacity
        *all_lists = realloc(*all_lists, (*capacity) * sizeof(NumberList));
        if (*all_lists == NULL)
        {
            perror("Failed to allocate memory for lists");
            exit(EXIT_FAILURE);
        }
    }
    (*all_lists)[*list_count].numbers = numbers;
    (*all_lists)[*list_count].size = size;
    (*list_count)++;
}

void read_file(FILE *file, Relation **relations, int *count, NumberList **all_lists, int *list_count)
{
    char line[256]; // Buffer to store each line
    int capacity = 0;
    int after_break = 0;

    while (fgets(line, sizeof(line), file))
    {
        if (strcmp(line, "\n") == 0)
        {
            // break; // Stop at the blank line
            after_break = 1;
        }
        if (after_break == 0)
        {

            // Parse the "from|to" format
            char *token = strtok(line, "|");
            int from = atoi(token);

            token = strtok(NULL, "\n");
            int to = atoi(token);

            // Add the parsed relation to the list
            add_relation(relations, count, &capacity, from, to);
        }
        else if (after_break == 1)
        {
            char line[256];
            int capacity2 = 0;

            line[strcspn(line, "\n")] = 0;

            // Parse numbers from the line
            int *numbers = NULL;
            int size = 0;
            int num_capacity = 0;

            char *token = strtok(line, ",");
            while (token)
            {
                printf("Token: %s\n", token);
                if (size == num_capacity)
                {
                    num_capacity = (num_capacity == 0) ? 10 : (num_capacity * 2);
                    numbers = realloc(numbers, num_capacity * sizeof(int));
                    if (numbers == NULL)
                    {
                        perror("Failed to allocate memory for list");
                        exit(EXIT_FAILURE);
                    }
                }
                numbers[size++] = atoi(token);
                token = strtok(NULL, ",");
            }

            // Add the parsed list to the dynamic array of lists
            add_list(all_lists, list_count, &capacity2, numbers, size);
        }
    }
}

int main()
{
    FILE *file = fopen("../data/day5_small.txt", "r");
    if (!file)
    {
        perror("Failed to open file");
        return EXIT_FAILURE;
    }

    Relation *relations = NULL;
    int relation_count = 0;

    NumberList *all_lists = NULL;
    int list_count = 0;

    read_file(file, &relations, &relation_count, &all_lists, &list_count);

    printf("Read %d relations:\n", relation_count);
    for (int i = 0; i < relation_count; i++)
    {
        printf("%d -> %d\n", relations[i].from, relations[i].to);
    }

    // Print the lists
    for (int i = 0; i < list_count; i++)
    {
        printf("List %d: ", i + 1);
        for (int j = 0; j < all_lists[i].size; j++)
        {
            printf("%d ", all_lists[i].numbers[j]);
        }
        printf("\n");
    }

    // Clean up
    free(relations);
    for (int i = 0; i < list_count; i++)
    {
        free(all_lists[i].numbers);
    }
    free(all_lists);
    fclose(file);

    return 0;
}
