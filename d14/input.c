#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <err.h>

#define NUM_LINES 1024
#define MEM_SIZE 100 * 1024
#define MASK_OFFSET 7
#define BITMASK_LENGTH 36

enum instruction_type
{
    I_MASK,
    I_MEM
};

struct instruction
{
    enum instruction_type type;
    union {
        char *mask;
        struct {
            size_t offset;
            size_t value;
        } mem;
    } data;
};

struct program
{
    size_t num_instructions;
    struct instruction **instructions;
    char use_floating;

    char *mask;
    size_t mem[MEM_SIZE];
};

struct map
{
    size_t key;
    size_t value;
    struct map *next;
};

struct map *mem = NULL;

ssize_t get_mem(size_t offset)
{
    if (!mem)
        return -1;

    for (struct map *cp = mem; cp; cp = cp->next)
    {
        if (mem->key == offset)
            return mem->value;
    }

    return -1;
}

void set_mem(size_t offset, size_t value)
{
    struct map *prev = NULL;
    struct map *elem = mem;

    for (; elem; prev = elem, elem = elem->next)
    {
        if (elem->key == offset)
            break;
    }

    if (!elem)
    {
        elem = calloc(sizeof(struct map), 1);
        elem->key = offset;

        if (prev)
            prev->next = elem;
        else
            mem = elem;
    }

    elem->value = value;
}

struct program *new_program(char **lines, size_t num_lines)
{
    struct program *new = calloc(sizeof(struct program), 1);

    new->num_instructions = 0;
    new->instructions = calloc(sizeof(struct instruction *), num_lines);

    for (size_t i = 0; i < MEM_SIZE; i++)
        new->mem[i] = 0;

    for (size_t i = 0; i < num_lines; i++)
    {
        struct instruction *instruction = calloc(sizeof(struct instruction), 1);
        if (!strncmp(lines[i], "mask", 4))
        {
            instruction->type = I_MASK;
            instruction->data.mask = lines[i] + MASK_OFFSET;
        }
        else if (!strncmp(lines[i], "mem", 3))
        {
            instruction->type = I_MEM;

            int offset_start = 4, offset_end = 0;
            while (lines[i][offset_end++] != ']')
                ;
            offset_end--;

            int value_start = offset_end + 4;

            size_t offset = 0, value = 0;
            sscanf(lines[i] + offset_start, "%lu", &offset);
            sscanf(lines[i] + value_start, "%lu", &value);

            instruction->data.mem.offset = offset;
            instruction->data.mem.value = value;

            /*
            printf("%.*s: %.*s - %.*s\n", (int)strlen(lines[i]) - 1, lines[i],
                    offset_end - offset_start, lines[i] + offset_start,
                    value_end - value_start, lines[i] + value_start);
            printf("got: %lu - %lu\n", offset, value);
            */
        }
        else
        {
            if (lines[i][0])
                errx(1, "invalid instruction found: %s\n", lines[i]);
            free(instruction);
            continue;
        }

        new->instructions[new->num_instructions++] = instruction;
    }

    new->instructions = realloc(new->instructions,
            sizeof(struct instruction *) * new->num_instructions);

    return new;
}

void print_instruction(struct instruction *instruction)
{
    if (instruction->type == I_MASK)
        printf("MASK: %s\n", instruction->data.mask);
    else
        printf("MEM: %lu: %lu\n", instruction->data.mem.offset,
                instruction->data.mem.value);
}

void print_program(struct program *program)
{
    printf("Program: (%s floating)\n%lu instructions:\n",
            program->use_floating ? "with" : "no", program->num_instructions);

    for (size_t i = 0; i < program->num_instructions; i++)
        print_instruction(program->instructions[i]);
}

void free_program(struct program *program)
{
    for (size_t i = 0; i < program->num_instructions; i++)
        free(program->instructions[i]);
    free(program->instructions);
    free(program);
}

void write_all(struct program *program, size_t index, size_t offset, size_t value)
{
    size_t i = index;

    while (i < BITMASK_LENGTH && program->mask[i] != 'X')
        i++;

    if (i >= BITMASK_LENGTH)
    {
        set_mem(offset, value);
        return;
    }

    size_t bit_index = BITMASK_LENGTH - i - 1;
    size_t bit_mask = 1ULL << bit_index; // Don't forget the `ULL` !

    // set to 0
    offset &= ~bit_mask;
    write_all(program, i + 1, offset, value);

    // set to 1
    offset |= bit_mask;
    write_all(program, i + 1, offset, value);
}

void write_to_all_adresses(struct program *program, size_t offset, size_t value)
{
    for (size_t i = 0; i < BITMASK_LENGTH; i++)
    {
        size_t bit_value = program->mask[i];
        if (bit_value == '1')
        {
            size_t bit_index = BITMASK_LENGTH - i - 1;
            size_t bit_mask = 1ULL << bit_index; // Don't forget the `ULL` !

            offset |= bit_mask;
        }
    }

    write_all(program, 0, offset, value);
}

void process_instruction(struct program *program, size_t i)
{
    if (i >= program->num_instructions)
        return;

    if (program->instructions[i]->type == I_MASK)
    {
        program->mask = program->instructions[i]->data.mask;
    }
    else
    {
        char *current_mask = program->mask;

        size_t offset = program->instructions[i]->data.mem.offset;
        size_t value = program->instructions[i]->data.mem.value;

        if (!program->use_floating)
        {
            for (size_t mi = 0; current_mask[mi]; mi++)
            {
                if (current_mask[mi] == 'X')
                    continue;

                size_t bit_value = current_mask[mi] == '1';
                size_t bit_index = BITMASK_LENGTH - mi - 1;
                size_t bit_mask = 1ULL << bit_index; // Don't forget the `ULL` !

                if (bit_value)
                {
                    value |= bit_mask;
                }
                else
                {
                    value &= ~bit_mask;
                }
            }

            program->mem[offset] = value;
        }
        else
        {
            write_to_all_adresses(program, offset, value);
        }
    }
}

size_t solve_part_one(struct program *program)
{
    for (size_t i = 0; i < program->num_instructions; i++)
        process_instruction(program, i);

    size_t n = 0;

    for (size_t i = 0; i < MEM_SIZE; i++)
        n += program->mem[i];

    return n;
}

size_t solve_part_two(struct program *program)
{
    program->use_floating = 1;

    for (size_t i = 0; i < program->num_instructions; i++)
        process_instruction(program, i);

    size_t n = 0;

    for (struct map *cp = mem; cp; cp = cp->next)
        n += cp->value;

    return n;
}

int main(int argc, char **argv)
{
    if (argc != 2)
        errx(1, "%s <input file>", argv[0]);

    FILE *f = fopen(argv[1], "r");
    char **lines = calloc(sizeof(char *), NUM_LINES);
    size_t lines_read = 0;
    size_t n = 0;
    while (getline(lines + (lines_read++), &n, f) != -1)
        ;

    struct program *program = new_program(lines, lines_read);
    // print_program(program);

    printf("p1: %lu\n", solve_part_one(program));

    // Reset program between execution
    free_program(program);
    program = new_program(lines, lines_read);

    printf("p2: %lu\n", solve_part_two(program));

    free_program(program);

    for (size_t i = 0; i < NUM_LINES; i++)
        free(lines[i]);
    free(lines);

    fclose(f);

    for (struct map *cp = mem; cp;)
    {
        struct map *tmp = cp->next;
        free(cp);
        cp = tmp;
    }

    return 0;
}
