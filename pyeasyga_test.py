import time
import csv

from pyeasyga import pyeasyga

data = [(8, 9), (7, 5), (4, 10), (5, 4), (7, 9), (6, 2), (6, 5), (6, 1), (4, 3), (3, 4)]
max_mass = 30
pop_size = 20


def fitness (individual, data):
    fitness = 0
    sum_mass = 0
    for (selected, (price, mass)) in zip(individual, data):
        if selected:
            sum_mass += mass
            fitness += price
    if sum_mass > max_mass:
        return 0
    return fitness


results_list = []

for _ in range(100):
    ga = pyeasyga.GeneticAlgorithm(data,
                                   population_size=pop_size,
                                   generations=500,
                                   crossover_probability=0.5,
                                   mutation_probability=0.1,
                                   elitism=True,
                                   maximise_fitness=True)

    ga.fitness_function = fitness

    start_time = time.time()
    ga.run()
    time_diff = time.time() - start_time
    results_list.append(
        [time_diff, ga.best_individual()[0], 500, ga.best_individual()[1]])
    print(time_diff)
    print(ga.best_individual())
print(results_list)
with open("pyeasyga_results.csv", "w", newline="") as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(results_list)