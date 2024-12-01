#include <stdio.h>
#include <stdlib.h>

#define MAX_LINE_LENGTH 1024

int compare_ints(const void *a, const void *b)
{
    int arg1 = *(const int *)a;
    int arg2 = *(const int *)b;

    if (arg1 < arg2)
        return -1;
    if (arg1 > arg2)
        return 1;
    return 0;
}

int main()
{
    FILE *inputFile = fopen("/Users/ago/projects/aoc-2024/data/input.txt", "r");

    if (inputFile == NULL)
    {
        fprintf(stderr, "Error opening file.\n");
        return 1; // Exit with a non-zero status code to indicate an error
    }

    char line[MAX_LINE_LENGTH];

    int *row1 = malloc(4 * sizeof(int));
    int *row2 = malloc(4 * sizeof(int));

    int line_count = 0;

    while (fgets(line, MAX_LINE_LENGTH, inputFile))
    {
        int num1, num2;
        while (sscanf(line, "%d %d", &num1, &num2) == 2)
        {
            row1[line_count] = num1;
            row2[line_count] = num2;

            row1 = realloc(row1, (4 + line_count) * sizeof(int));
            row2 = realloc(row2, (4 + line_count) * sizeof(int));

            line_count++;

            break;
        }
    }

    fclose(inputFile); // Close the file when done reading

    qsort(row1, line_count, sizeof(int), compare_ints);
    qsort(row2, line_count, sizeof(int), compare_ints);

    int differences = 0;

    for (int i = 0; i < line_count; i++)
    {
        differences += abs(row1[i] - row2[i]);
    }

    free(row1);
    free(row2);

    printf("Linecount: ");

    printf("%d ", line_count);

    printf("\n");
    printf("\n");

    printf("Differences: ");

    printf("%d ", differences);
    printf("\n");

    return 0;
}
