import Chromosome

POP_Size = 600


def population(key_size, value):
    population = [None] * POP_Size
    count = 0
    # if key != None:
    #     for i in key:
    #         if 97 <= ord(i) <= 122:
    #             count += 1
    #     for i in range(len(population)):
    #         population[i] = Chromosome.Chromosome(count, value)
    # else:
    for i in range(len(population)):
        population[i] = Chromosome.Chromosome(key_size, value)
    return population
