import random
import time
import csv

from deap import creator, base, tools, algorithms


data = [(8, 9), (7, 5), (4, 10), (5, 4), (7, 9), (6, 2), (6, 5), (6, 1), (4, 3), (3, 4)]
max_mass = 30

pop_size = 20

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)

def evalOneMax(individual):
    fitness = 0
    sum_mass = 0
    for selected, (price, mass) in zip(individual, data):
        if selected:
            fitness += price
            sum_mass += mass
    if sum_mass > max_mass:
        return 0,
    else:
        return fitness,

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

results_list = []

for _ in range(100):
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(data))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    population = toolbox.population(n=pop_size)

    NGEN=500
    best_fit = 0
    best_gen = 0
    differential = 30
    start_time = time.time()
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        current_gen_best_individual = tools.selBest(population, k=1)[0]
        current_gen_best_fit = current_gen_best_individual.fitness.values[0]
        if current_gen_best_fit > best_fit:
            best_individual = current_gen_best_individual
            best_fit = current_gen_best_fit
            best_gen = gen
    time_diff = time.time() - start_time
    results_list.append(
        [time_diff, best_individual.fitness.values[0], best_gen, best_individual])
    print(time_diff)
    print(best_individual.fitness.values[0], best_individual)
print(results_list)
with open("DEAP_results.csv", "w", newline="") as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(results_list)