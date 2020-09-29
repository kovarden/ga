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

    def run(self):
        for _ in range(self.generations):
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
            # new_population.calculation_fit_values(self.fit_function)
            self.population = Population([])
            for _ in range(self.population_length):
                individual = new_population.roulette_coupling()
                self.population.individuals.append(individual)

    def top(self, k=1):
        return sorted(self.population.individuals, key=lambda x: x.fitness, reverse=True)[:k]


if __name__ == '__main__':
    import math
    individuals =[[0 for _ in range(5)] for _ in range(5)]
    data = [(6, 5), (4, 3), (3, 1), (2, 3), (5, 6)]
    full_mass = sum([item[1] for item in data])
    max_mass = 15
    delta_mass = max(max_mass, full_mass - max_mass)

    def fit_func(individual):
        fitness = 0
        sum_mass = 0
        if sum(individual) > 4:
            return 0
        for selected, (price, mass) in zip(individual, data):
            if selected:
                fitness += price
                sum_mass += mass
        if sum_mass > max_mass:
            fitness = 1 - math.sqrt((sum_mass - max_mass) / delta_mass)
        else:
            fitness = 1 - math.sqrt((max_mass - sum_mass) / max_mass)
        return fitness

    my_ga = GA(
        individuals,
        fit_func,
        population_length=10,
        generations=10,
        mutation_chance=0.1,
        crossover_chance=0.5
    )
    my_ga.run()
    print(my_ga.top()[0])