from game import play
from ai import Net
import numpy as np
import math
import random
import heapq
import copy

CROSS_RATE = .9
MUT_RATE = .05
GENERATIONS = 20
POP_SIZE = 20

def get_fitness(n):
	print 'Getting fitness of ' + str(n)
	return play(True, n)

def init_pop(size=POP_SIZE):
	pop = []
	for i in xrange(size):
		n = Net()
		pop.append(n)

	return pop

def breed(n1, n2):
	if random.random() < CROSS_RATE:
		gene1 = np.array(n1.encode())
		gene2 = np.array(n2.encode())

		r = random.random()
		# take average
		child1 = [i * 0.5 for i in np.add(gene1, gene2)]
		r = random.random()
		child2 = [i * 0.5 for i in np.add(gene1, gene2)]

		child1 = mutate(child1)
		child2 = mutate(child2)

		n1.decode(gene1)
		n2.decode(gene2)

	return (n1, n2)

def mutate(gene):
	if random.random() < MUT_RATE:
		index = random.randint(0, len(gene) - 1)
		gene[index] += random.triangular(-1, 1) * gene[index]

def select(pop):
	first = pop[random.randint(0, len(pop) - 1)]
	second = pop[random.randint(0, len(pop) - 1)]
	if get_fitness(first) < get_fitness(second):
		return first

	return second

def get_new_pop(pop):
	new_pop = []
	pop = sorted(pop, key=get_fitness)
	new_pop.extend(pop[0:5])
	while len(new_pop) < len(pop):
		first = select(pop)
		second = select(pop)
		first, second = breed(first, second)
		new_pop.extend([first, second])

	return new_pop

# test AI
n = Net()
good = [-.5524816518, -0.251785039, -1.2697808633, -0.72796955875826, -0.81684247849, 3.97877468847]
n.decode(good)
play(False, n)

# start genetic algo
pop = init_pop()
for i in xrange(GENERATIONS):
    print '==========================='
    print 'GENERATION ' + str(i)
    pop = get_new_pop(pop)

play(False, pop[0])
