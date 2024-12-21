#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAX_OUTPUT_LENGTH 4096
#define INSTRUCTION_SIZE 2

typedef struct
{
    int64_t reg_a;
    int64_t reg_b;
    int64_t reg_c;
    int64_t program[16];
    size_t program_length;
} VM_State;

static inline int64_t find_combo(const VM_State *state, int64_t operand)
{
    switch (operand)
    {
    case 0:
    case 1:
    case 2:
    case 3:
        return operand;
    case 4:
        return state->reg_a;
    case 5:
        return state->reg_b;
    case 6:
        return state->reg_c;
    default:
        fprintf(stderr, "Error! Invalid operand: %lld\n", operand);
        return -1;
    }
}

static inline int64_t op0(VM_State *state, int64_t operand)
{
    int64_t to_power = find_combo(state, operand);
    return state->reg_a >> to_power;
}

static inline int64_t op1(VM_State *state, int64_t operand)
{
    return state->reg_b ^ operand;
}

static inline int64_t op2(VM_State *state, int64_t operand)
{
    return find_combo(state, operand) & 0x7;
}

static inline int op3(VM_State *state, int64_t operand, size_t *ip)
{
    if (state->reg_a == 0)
    {
        return 0;
    }
    *ip = operand;
    return 1;
}

static inline int64_t op4(VM_State *state, int64_t operand)
{
    return state->reg_b ^ state->reg_c;
}

static inline int64_t op5(VM_State *state, int64_t operand)
{
    return find_combo(state, operand) & 0x7;
}

static inline int64_t op6(VM_State *state, int64_t operand)
{
    int64_t to_power = find_combo(state, operand);
    return state->reg_a >> to_power;
}

static inline int64_t op7(VM_State *state, int64_t operand)
{
    int64_t to_power = find_combo(state, operand);
    return state->reg_a >> to_power;
}

char *run_process(VM_State *state)
{
    if (!state)
        return NULL;

    char *output = malloc(MAX_OUTPUT_LENGTH);
    if (!output)
        return NULL;

    char *current_pos = output;
    size_t remaining_space = MAX_OUTPUT_LENGTH - 1;
    size_t ip = 0;

    while (ip < state->program_length)
    {
        int64_t opcode = state->program[ip];
        int64_t operand = state->program[ip + 1];
        int jump_occurred = 0;

        switch (opcode)
        {
        case 0:
            state->reg_a = op0(state, operand);
            break;
        case 1:
            state->reg_b = op1(state, operand);
            break;
        case 2:
            state->reg_b = op2(state, operand);
            break;
        case 3:
            jump_occurred = op3(state, operand, &ip);
            if (!jump_occurred)
            {
                ip += INSTRUCTION_SIZE;
            }
            continue;
        case 4:
            state->reg_b = op4(state, operand);
            break;
        case 5:
        {
            int64_t result = op5(state, operand);
            int written = snprintf(current_pos, remaining_space, "%lld,", result);
            if (written > 0 && written < remaining_space)
            {
                current_pos += written;
                remaining_space -= written;
            }
            break;
        }
        case 6:
            state->reg_b = op6(state, operand);
            break;
        case 7:
            state->reg_c = op7(state, operand);
            break;
        }

        if (!jump_occurred)
        {
            ip += INSTRUCTION_SIZE;
        }
    }

    // Remove trailing comma if exists
    if (current_pos > output && *(current_pos - 1) == ',')
    {
        *(current_pos - 1) = '\0';
    }

    return output;
}

int main()
{
    VM_State state = {
        .reg_b = 0,
        .reg_c = 0,
        .program = {2, 4, 1, 1, 7, 5, 1, 5, 4, 1, 5, 5, 0, 3, 3, 0},
        .program_length = 16};

    const char *target_output = "2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0";
    const int64_t target_value = 999999117440LL; // You can make this much larger now

    printf("Starting search up to %lld\n", target_value);

    for (int64_t i = 0; i <= target_value; i++)
    {
        // Print progress every 5000 iterations
        if (i % 500000 == 0)
        {
            printf("Progress: %lld / %lld\n", i, target_value);
        }

        // Set up state for this iteration
        state.reg_a = i;
        state.reg_b = 0;
        state.reg_c = 0;

        // Run the program
        char *output = run_process(&state);
        if (!output)
        {
            fprintf(stderr, "Error: Failed to get output\n");
            continue;
        }

        // Check if we found a match
        if (strcmp(output, target_output) == 0)
        {
            printf("\nFound matching value!\n");
            printf("Register A value: %lld\n", i);
            printf("Output: %s\n", output);
            free(output);
            break;
        }

        free(output);
    }

    return 0;
}