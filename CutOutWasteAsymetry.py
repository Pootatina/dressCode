from functools import partial
import random

import numpy
import shapely
from deap import creator, base, tools, algorithms
from shapely import Polygon

import npDressCode
import patternGeneratorAsymmetry
import svgHelper
import wasteGeneration

# Define the dimensions of the fabric rectangle
fabric_width, fabric_height = 600, 600
fabric = Polygon([(0, 0), (fabric_width, 0), (fabric_width, fabric_height), (0, fabric_height)])

# Function to generate random cutouts
def generate_valid_cutouts(num_cutouts, fabric, min_size, max_size, attempts=100):
    cutouts = []
    fabric_width, fabric_height = fabric.bounds[2], fabric.bounds[3]  # get dimensions from fabric bounds

    for _ in range(num_cutouts):
        valid_cutout = False
        for _ in range(attempts):  # Attempt to place each cutout without overlap
            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)
            x = random.randint(0, int(fabric_width - w))  # ensure the cutout stays within fabric bounds
            y = random.randint(0, int(fabric_height - h))
            new_cutout = shapely.box(x, y, x + w, y + h)
            # Check new cutout does not overlap with existing cutouts
            if not any(new_cutout.intersects(cutout) for cutout in cutouts):
                cutouts.append(new_cutout)
                valid_cutout = True
                break
        if not valid_cutout:
            print(f"Failed to place a valid cutout after {attempts} attempts.")
            # If cannot place after many attempts, could adjust strategy, e.g., reduce number of cutouts or size

    # Merge all cutouts with fabric to create final shape with holes
    fabric_with_cutouts = Polygon(fabric.exterior.coords, [cut.exterior.coords for cut in cutouts])
    return fabric_with_cutouts

# Generate 4 random cutouts within the fabric
waste = generate_valid_cutouts(4, fabric, 50, 200)


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", dict, fitness=creator.FitnessMax)


toolbox = base.Toolbox()

toolbox.register("individual", npDressCode.init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", partial(npDressCode.evaluateCutOutAsymmetry, waste=waste))
toolbox.register("mate", npDressCode.mate, indpb=0.5)
toolbox.register("mutate", npDressCode.mutate, indpb=0.2)
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


svgHelper.save_polygons_with_holes_to_svg(
    waste, [front, back, sleeveLeft, sleeveRight], "images/bestCutOutWasteCentroidAsymmetry.svg")