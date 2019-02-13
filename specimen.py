import numpy as np

MUTATION_AMOUNT = 0.1
MUTATION_CHANCE = 0.5
GENERATION_SIZE = 1000
TOP_CUTOFF = 20


class Specimen:
	#This class contains all the info for the specimen
	#the 'dna' defines how much to change each part of the image
	def __init__(self, dna, mutate):

		if type(dna) == int and dna == 0:
			#hardcoded for the cifar-10 dataset
			self.dna = np.zeros(1024)
		else:
			self.dna = dna

		if mutate:
			self.mutate(MUTATION_CHANCE, MUTATION_AMOUNT)

		self.generation = 0

	def mutate(self, chance, mutation_amount):
		for sample, value in enumerate(np.random.uniform(0, 1, 1024)):
			#mutate that dna variable if the generated float is less than that percentage
			if value <= chance:
				#randomly adds or subtracts the mutation amount
				self.dna[sample] += mutation_amount * ((-1)** np.random.randint(2))

	def evaluate_specimen(self):
		pass

#a generation is a collection of specimens
class Generation:

	def __init__(self, generation_size, random):
		self.members = []
		for i in range(generation_size):
			#add new individuals to the members of the generation
			if random:
				self.members.append(Specimen(np.random.uniform(0,1,1024), True))
			else:
				self.members.append(Specimen(0, True))
		self.epoch = 0
	def clear(self):
		self.members = []

	def evolve(self, fitness):
		sorted_members = []
		#apply the fitness function to each of the members of the generation
		for specimen in self.members:
			sorted_members.append((specimen, fitness(specimen)))

		#select the top performers of each generation
		sorted_members = sorted(sorted_members, key=lambda x : x[1])
		sorted_members.reverse()
		sorted_members = sorted_members[TOP_CUTOFF:]

		self.clear()

		#breed the top performers to generate new members
		while len(self.members) < GENERATION_SIZE:
			father = sorted_members[np.random.randint(TOP_CUTOFF)][0]
			mother = sorted_members[np.random.randint(TOP_CUTOFF)][0]

			child = breed(mother, father)

			self.members.append(child)




#breed defined outside for philosophical reasons
#it makes more sense to me to apply the function to two specimens and return one than call it on a specimen

def breed(specimen1, specimen2):
	#we will mutate after breeding
	child = Specimen(0, False)

	#both specimens have the exact sample number of genes by design
	#choose a random gene from each parent
	for index, gene in enumerate(specimen1.dna):
		if np.random.randint(2):
			child.dna[index] = gene
		else:
			child.dna[index] = specimen2.dna[index]

	#mutates the new child
	child.mutate(MUTATION_CHANCE, MUTATION_AMOUNT)
	child.generation = specimen1.generation + 1

	return child

#fitness function for debugging
def fitness_test(specimen):
	return np.sum(specimen.dna) / 1024.0

def average_fitness(generation):
	average = 0.0
	for member in generation.members:
		average += fitness_test(member)
	return average / GENERATION_SIZE


g = Generation(GENERATION_SIZE, True)

for epoch in range(100):
	print("evolving, epoch: %d" % epoch)
	g.evolve(fitness_test)
	print("generation fitness: %f" % average_fitness(g))
