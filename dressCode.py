import random
from deap import creator, base, tools, algorithms
import numpy

import patternGeneratorAsymmetry
import patternGeneratorSymmetry
import svgHelper

# Setup DEAP fitness and individual structures
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", dict, fitness=creator.FitnessMax)

# Define possible values for the measurements
'''measurements = [
    Measure(name='neckline_width', bounds=(20, 30)),
    Measure(name='neckline_height_front', bounds=(5, 20)),
    Measure(name='neckline_height_back', bounds=(2, 30)),
    Measure(name='shoulder_height_right', bounds=(0, 10)),
    Measure(name='shoulder_height_left', bounds=(0, 10)),
    Measure(name='armhole_height_right', bounds=(20, 30)),
    Measure(name='armhole_height_left', bounds=(20, 30)),
    Measure(name='armhole_width_right', bounds=(0, 15)),
    Measure(name='armhole_width_left', bounds=(0, 15)),
    Measure(name='sleeve_width_right', bounds=(25, 60)),
    Measure(name='sleeve_width_left', bounds=(25, 60)),
    Measure(name='sleeve_length_right', bounds=(0, 60)),
    Measure(name='sleeve_length_left', bounds=(0, 60)),
    Measure(name='bust_width', bounds=(50, 70)),
    Measure(name='side_length_right', bounds=(20, 100)),
    Measure(name='side_length_left', bounds=(20, 100)),
    Measure(name='waist_width', bounds=(45, 100))
]'''

# List of measurement names and their corresponding bounds
measurements = [
    'neckline_width', 'neckline_height_front', 'neckline_height_back',
    'shoulder_height_right', 'shoulder_height_left', 'armhole_height_right',
    'armhole_height_left', 'armhole_width_right', 'armhole_width_left',
    'sleeve_width_right', 'sleeve_width_left', 'sleeve_length_right',
    'sleeve_length_left', 'bust_width', 'side_length_right', 'side_length_left',
    'waist_width'
]
bounds = [
    (20, 30), (5, 20), (2, 30), (0, 10), (0, 10), (20, 30), (20, 30), (0, 15),
    (0, 15), (25, 60), (0, 40), (0, 60), (0, 60), (50, 65), (20, 100), (20, 100),
    (45, 100)
]
measurements_bounds_dict = dict(zip(measurements, bounds))


toolbox = base.Toolbox()

# Function to initialize individuals with random measurements within defined bounds.
def init_individual():
    """ Initialize an individual as a dictionary with random values within the bounds. """
    return creator.Individual(
        {key: random.randint(measurements_bounds_dict[key][0], measurements_bounds_dict[key][1]) for key in
         measurements_bounds_dict})


# Evaluation function
def evaluate(individual):
    back = patternGeneratorSymmetry.generate_shirt_back_polygon(individual)
    front = patternGeneratorSymmetry.generate_shirt_front_polygon(individual)
    sleeveLeft = patternGeneratorSymmetry.generate_left_sleeve_polygon(individual)
    sleeveRight = patternGeneratorSymmetry.generate_right_sleeve_polygon(individual)
    area = back.area + front.area + sleeveLeft.area + sleeveRight.area # Access the area property correctly
    return (area,)  # Return a tuple with the area


def cxDictUniform(ind1, ind2, indpb):
    """ Custom crossover that performs uniform crossover for dictionary-based individuals. """
    for key in ind1:
        if random.random() < indpb:
            ind1[key], ind2[key] = ind2[key], ind1[key]
    return ind1, ind2


def mutUniformInt(individual, indpb):
    """ Custom mutation that mutates an integer in a dictionary based on its specific bounds. """
    for key in individual:
        if random.random() < indpb:
            individual[key] = random.randint(measurements_bounds_dict[key][0], measurements_bounds_dict[key][1])
    return individual,


toolbox.register("individual", init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", cxDictUniform, indpb=0.5)
toolbox.register("mutate", mutUniformInt, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Generate population and run the algorithm
population = toolbox.population(n=10)
hof = tools.HallOfFame(10)
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

result, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=10,
                                      stats=stats, halloffame=hof, verbose=True)

# Print results
print("Best individual is:", hof[0], "with fitness:", hof[0].fitness.values[0])
svgHelper.save_polygon_to_svg(patternGeneratorSymmetry.generate_shirt_back_polygon(hof[0]), "back1.svg")
svgHelper.save_polygon_to_svg(patternGeneratorSymmetry.generate_right_sleeve_polygon(hof[0]), "sleeve.svg")
svgHelper.save_polygon_to_svg(patternGeneratorSymmetry.generate_shirt_front_polygon(hof[0]), "front1.svg")
svgHelper.save_polygon_to_svg(patternGeneratorAsymmetry.generate_shirt_front_polygon(hof[1]), "front2.svg")
print(hof[0]['waist_width'])
