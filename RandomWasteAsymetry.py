# First try with fixed waste
from functools import partial

import numpy
import shapely
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

waste = [wasteGeneration.generate_a_polygon(((0, 400), (0, 200))),
         wasteGeneration.generate_a_polygon(((200, 300), (0, 450))),
         wasteGeneration.generate_a_polygon(((300, 500), (200, 350))),
         wasteGeneration.generate_a_polygon(((450, 600), (200, 600)))]


toolbox = base.Toolbox()

toolbox.register("individual", npDressCode.init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", partial(npDressCode.evaluatePlacementAsymmetry, waste=waste))
toolbox.register("mate", npDressCode.mate, indpb=0.5)
toolbox.register("mutate", npDressCode.mutate, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=5)

# Generate population and run the algorithm
population = toolbox.population(n=500)
hof = tools.HallOfFame(3)
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

result, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=5000,
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
    "images/bestRandomWasteAsymmetry.svg")