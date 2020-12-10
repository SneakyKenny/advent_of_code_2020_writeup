#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <err.h>

size_t max(size_t *inputs, size_t length)
{
    if (length == 0)
        errx(1, "can't max on length 0");

    size_t m = inputs[0];

    for (size_t i = 1; i < length; i++)
        m = inputs[i] > m ? inputs[i] : m;

    return m;
}

size_t in(size_t num, size_t *inputs, size_t length)
{
    static size_t *map = NULL;

    if (map == NULL)
    {
        map = calloc(1000, sizeof(size_t));

        for (size_t i = 0; i < length; i++)
            map[inputs[i]] = 1;
    }

    return map[num] != 0;
}

size_t rec(size_t *inputs, size_t length, size_t curr, size_t target)
{
    if (curr + 3 == target)
        return 1;

    static size_t *map = NULL;

    if (map == NULL)
        map = calloc(1000, sizeof(size_t));

    if (map[curr] != 0)
        return map[curr];

    size_t num = 0;

    for (size_t delta = 1; delta <= 3; delta++)
    {
        size_t n = curr + delta;

        if (!in(n, inputs, length))
            continue;

        num += rec(inputs, length, n, target);
    }

    map[curr] = num;
    return num;
}

size_t bfs(size_t *inputs, size_t length)
{
    size_t target = max(inputs, length) + 3;
    return rec(inputs, length, 0, target);
}

int main(int argc, char **argv)
{
    if (argc != 2)
        errx(1, "Please provide a file to open");

    FILE *f = fopen(argv[1], "r");

    size_t num_inputs = 200;
    size_t *inputs = malloc(sizeof(size_t) * num_inputs);
    size_t length = 0;

    while (fscanf(f, "%lu", inputs + length++) == 1)
        ;

    /* for (size_t i = 0; i < length; i++)
        printf("%d\n", inputs[i]); */

    printf("%lu\n", bfs(inputs, length));

    free(inputs);

    fclose(f);

    return 0;
}
