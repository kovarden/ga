import csv

from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.operator import SPXCrossover, BitFlipMutation, BinaryTournamentSelection
from jmetal.problem.singleobjective.knapsack import Knapsack
from jmetal.util.termination_criterion import StoppingByEvaluations


data = [(8, 9), (7, 5), (4, 10), (5, 4), (7, 9), (6, 2), (6, 5), (6, 1), (4, 3), (3, 4)]
problem = Knapsack(10, 30, [x[1] for x in data], [x[0] for x in data])

algorithm = GeneticAlgorithm(
    problem=problem,
    population_size=20,
    offspring_population_size=20,
    mutation=BitFlipMutation(probability=0.1),
    crossover=SPXCrossover(probability=0.5),
    selection=BinaryTournamentSelection(),
    termination_criterion=StoppingByEvaluations(max_evaluations=500)
)

results_list = []

for _ in range(100):
    algorithm.run()
    subset = algorithm.get_result()
    time_diff = algorithm.total_computing_time
    best_fitness = -subset.objectives[0]
    best_individual = [1 if gen else 0 for gen in subset.variables[0]]
    results_list.append([time_diff, int(best_fitness), 500, best_individual])
    print(time_diff, best_individual)
print(results_list)
with open("jmetalpy_results.csv", "w", newline="") as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(results_list)