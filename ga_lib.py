import random


class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = None

    def single_point_crossing(self, second_individual):
        middle_point = int(len(self.chromosome) / 2)
        new_chromosome = self.chromosome[:middle_point] + second_individual.chromosome[middle_point:]
        return Individual(new_chromosome)

    def mutation(self, index):
        if self.chromosome[index] == 0:
            self.chromosome[index] = 1
        else:
            self.chromosome[index] = 0

    def __str__(self):
        return f'{self.fitness} {self.chromosome}'


class Population:
    def __init__(self, individuals_list):
        self.individuals = individuals_list

    def roulette_coupling(self):
        if len(self.individuals) != 0:
            summ = 0
            for individual in self.individuals:
                summ += individual.fitness
            while True:
                individual = random.choice(self.individuals)
                if summ == 0 or random.random() < (individual.fitness/summ):
                    return individual

    def calculation_fit_values(self, fit_function):
        for individual in self.individuals:
            individual.fitness = fit_function(individual.chromosome)


class GA:
    def __init__(self,
                 init_population,
                 fit_function,
                 population_length=10,
                 generations=100,
                 mutation_chance=0.1,
                 crossover_chance=0.5
                 ):
        self.population = Population([Individual(individual) for individual in init_population])
        for individual in self.population.individuals:
            individual.fitness = fit_function(individual.chromosome)
        self.fit_function = fit_function
        self.population_length = population_length
        self.generations = generations
        self.mutation_chance = mutation_chance
        self.crossover_chance = crossover_chance
        self.best_individual = self.population.individuals[1]
        self.best_generation = 0

    def run(self):
        current_generation = 0
        for i in range(self.generations):
            new_population = Population(self.population.individuals)
            for _ in range(self.population_length):
                if random.random() < self.crossover_chance:
                    first_parent, second_parent = self.population.roulette_coupling(),\
                                                  self.population.roulette_coupling()
                    new_individual = first_parent.single_point_crossing(second_parent)
                    new_individual.fitness = self.fit_function(new_individual.chromosome)
                    new_population.individuals.append(new_individual)
            for individual in new_population.individuals:
                if random.random() < self.mutation_chance:
                    individual.mutation(random.randint(0, len(individual.chromosome)-1))
                    individual.fitness = self.fit_function(individual.chromosome)
            self.population = Population([])
            for _ in range(self.population_length):
                individual = new_population.roulette_coupling()
                if individual.fitness > self.best_individual.fitness:
                    self.best_individual = individual
                    self.best_generation = i
                self.population.individuals.append(individual)
            if current_generation - self.best_generation > 100:
                break

    def top(self, k=1):
        return sorted(self.population.individuals, key=lambda x: x.fitness, reverse=True)[:k]


if __name__ == '__main__':

    POPUlATION_LENGTH = 20
    data = [(8, 9), (7, 5), (4, 10), (5, 4), (7, 9), (6, 2), (6, 5), (6, 1), (4, 3), (3, 4)]
    max_mass = 30

    individuals =[[random.randint(0, 1) for _ in range(len(data))] for _ in range(POPUlATION_LENGTH)]

    def fit_func(individual):
        fitness = 0
        sum_mass = 0
        for selected, (price, mass) in zip(individual, data):
            if selected:
                fitness += price
                sum_mass += mass
        if sum_mass > max_mass:
            return 0
        else:
            return fitness

    my_ga = GA(
        individuals,
        fit_func,
        population_length=POPUlATION_LENGTH,
        generations=1000,
        mutation_chance=0.1,
        crossover_chance=0.5
    )
    my_ga.run()
    print(my_ga.best_individual)