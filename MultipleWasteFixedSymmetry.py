# First try with fixed waste
from functools import partial

import numpy
from deap import creator, base, tools, algorithms

import dressCode
import patternGeneratorSymmetry
import svgHelper
import wasteGeneration

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", dict, fitness=creator.FitnessMax)

waste = [wasteGeneration.generate_random_polygon(((140, 250), (100, 350))),
         wasteGeneration.generate_random_polygon(((140, 250), (100, 350))),
         wasteGeneration.generate_random_polygon(((140, 220), (200, 350))),
         wasteGeneration.generate_random_polygon(((140, 220), (200, 350)))]

# waste = [
#     Polygon([(269, 289), (205, 188), (143, 308), (294, 285), (278, 133), (219, 340), (231, 314), (223, 311), (274, 113),
#              (168, 306), (140, 310)]).convex_hull,
#     Polygon([(285, 262), (244, 270), (156, 401), (271, 130), (259, 176), (201, 164), (219, 222), (287, 396), (294, 449),
#              (157, 211), (140, 310)]).convex_hull,
#     Polygon([(158, 315), (159, 230), (208, 324), (141, 319), (212, 298), (164, 337), (234, 257), (219, 263), (217, 244),
#              (207, 209), (140, 310)]).convex_hull,
#     Polygon([(159, 252), (235, 292), (156, 203), (182, 285), (249, 289), (147, 315), (149, 213), (200, 216), (170, 327),
#              (231, 218), (140, 310)]).convex_hull]


toolbox = base.Toolbox()

toolbox.register("individual", dressCode.init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", partial(dressCode.evaluateFixedSymmetry, waste=waste))
toolbox.register("mate", dressCode.mate, indpb=0.5)
toolbox.register("mutate", dressCode.mutate, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=5)

# Generate population and run the algorithm
population = toolbox.population(n=100)
hof = tools.HallOfFame(3)
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

result, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=100,
                                      stats=stats, halloffame=hof, verbose=True)

# Print results
print("Best individual is:", hof[0], "with fitness:", hof[0].fitness.values[0])
shirt_front = patternGeneratorSymmetry.generate_shirt_front_polygon(hof[0])
shirt_back = patternGeneratorSymmetry.generate_shirt_back_polygon(hof[0])
shirt_sleeve = patternGeneratorSymmetry.generate_sleeve_polygon(hof[0])

svgHelper.save_polygons_to_svg(
    [waste[0], shirt_front, waste[1], shirt_back, waste[2], shirt_sleeve, waste[3], shirt_sleeve],
    "images/bestMultipleWasteFixedSymmetry.svg")
