# First try with fixed waste
from functools import partial
import matplotlib.pyplot as plt
import numpy

import shapely as shapely
from deap import creator, base, tools, algorithms
from shapely import Polygon, MultiPolygon

import dressCode
import npDressCode
import patternGeneratorAsymmetry
import svgHelper
import wasteGeneration

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", dict, fitness=creator.FitnessMax)

# waste = [wasteGeneration.generate_a_polygon(((0, 400), (0, 200))),
#          wasteGeneration.generate_a_polygon(((200, 300), (0, 450))),
#          wasteGeneration.generate_a_polygon(((300, 500), (200, 350))),
#          wasteGeneration.generate_a_polygon(((450, 600), (200, 600)))]
waste = wasteGeneration.generate_realWasteOne()
min_x, min_y, max_x, max_y = wasteGeneration.get_minmaxDrift(waste)

toolbox = base.Toolbox()

toolbox.register("individual", npDressCode.init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", partial(npDressCode.evaluatePlacementAsymmetryImproved, waste=waste))
toolbox.register("mate", npDressCode.mate, indpb=0.5)
toolbox.register("mutate", npDressCode.mutateShift, min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=50)

# Generate population and run the algorithm
population = toolbox.population(n=2000)
hof = tools.HallOfFame(3)
stats = tools.Statistics()
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

result, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=10000,
                                      stats=stats, halloffame=hof, verbose=True)

# Print results
print("Best individual is:", hof[0], "with fitness:", hof[0].fitness.values[0])
shirt_front = patternGeneratorAsymmetry.generate_shirt_front_polygon(hof[0])
shirt_back = patternGeneratorAsymmetry.generate_shirt_back_polygon(hof[0])
left_sleeve = patternGeneratorAsymmetry.generate_left_sleeve_polygon(hof[0])
right_sleeve = patternGeneratorAsymmetry.generate_right_sleeve_polygon(hof[0])

front = shapely.affinity.translate(shirt_front, xoff=hof[0]['front_x_shift'], yoff=hof[0]['front_y_shift'],
                                   zoff=0.0)
back = shapely.affinity.translate(shirt_back, xoff=hof[0]['back_x_shift'],
                                  yoff=hof[0]['back_y_shift'], zoff=0.0)
sleeveLeft = shapely.affinity.translate(left_sleeve, xoff=hof[0]['sleeve_left_x_shift'],
                                        yoff=hof[0]['sleeve_left_y_shift'], zoff=0.0)
sleeveRight = shapely.affinity.translate(right_sleeve, xoff=hof[0]['sleeve_right_x_shift'],
                                         yoff=hof[0]['sleeve_right_y_shift'], zoff=0.0)

svgHelper.save_inPlace_polygons_to_svg(
    waste, [front, back, sleeveLeft, sleeveRight],
    "images/bestRandomWasteAsymmetryRealRandomThree.svg")

# # Daten für die Koordinatensystem sammeln
# x_values = [[], [], [], []]
# y_values = [[], [], [], []]
#
# # Schlüssel für die x- und y-Verschiebungen
# keys = ['front', 'back', 'sleeve_left', 'sleeve_right']
# for record in logbook:
#     best_ind = record['best']
#     for i, key in enumerate(keys):
#         x_values[i].append(best_ind[f'{key}_x_shift'])
#         y_values[i].append(best_ind[f'{key}_y_shift'])
#
# # Visualisierung
# colors = [(167, 204, 102), (97, 28, 53), (255, 167, 51), (46, 80, 119)]
# for i, key in enumerate(keys):
#     plt.plot(x_values[i], y_values[i], color=colors[i], label=f'Shift {key.upper()}')
# plt.xlabel('Generation')
# plt.ylabel('Shift-Werte')
# plt.title('Shift-Werte über Generationen')
# plt.legend()
# plt.show()
