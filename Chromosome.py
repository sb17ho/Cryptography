import random


def chromosome(size):
    s = "abbcdefghijklmnopqrstuvwxyz-"
    chromo = ""
    for i in range(size):
        chromo += random.choice(s)
    return chromo


class Chromosome():
    def __init__(self, size, value):
        self.value = value
        self.chromo = chromosome(size)
