import random

import shapely
from deap import creator
from shapely import affinity

import patternGeneratorAsymmetry
import patternGeneratorSymmetry

# Setup DEAP fitness and individual structures

# Define possible values for the measurements

'''measurements = [
    Measure(name='neckline_width', bounds=(20, 30)),
    Measure(name='neckline_height_front', bounds=(5, 30)),
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
    'waist_width', 'front_x_shift', 'front_y_shift', 'back_x_shift', 'back_y_shift', 'sleeve_left_x_shift',
    'sleeve_left_y_shift', 'sleeve_right_x_shift', 'sleeve_right_y_shift'
]
bounds = [
    (20, 30), (5, 20), (2, 30), (0, 10), (0, 10), (20, 30), (20, 30), (0, 15),
    (0, 15), (25, 60), (0, 40), (0, 60), (0, 60), (50, 65), (20, 100), (20, 100),
    (45, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100), (-100, 100)
]
measurements_bounds_dict = dict(zip(measurements, bounds))


# Function to initialize individuals with random measurements within defined bounds.
def init_individual():
    """ Initialize an individual as a dictionary with random values within the bounds. """
    return creator.Individual(
        {key: random.randint(measurements_bounds_dict[key][0], measurements_bounds_dict[key][1]) for key in
         measurements_bounds_dict})


# Evaluation functions
def evaluateFixedSymmetry(individual, waste):
    front = patternGeneratorSymmetry.generate_shirt_front_polygon(individual)
    back = patternGeneratorSymmetry.generate_shirt_back_polygon(individual)
    sleeveLeft = patternGeneratorSymmetry.generate_sleeve_polygon(individual)
    sleeveRight = patternGeneratorSymmetry.generate_sleeve_polygon(individual)
    if waste[0].contains(front) and waste[1].contains(back) and waste[2].contains(sleeveLeft) and waste[3].contains(
            sleeveRight):
        area = back.area + front.area + sleeveLeft.area + sleeveRight.area
    else:
        area = 0
    return (area,)  # Return a tuple with the are


def evaluateFixedAsymmetry(individual, waste):
    front = patternGeneratorAsymmetry.generate_shirt_front_polygon(individual)
    back = patternGeneratorAsymmetry.generate_shirt_back_polygon(individual)
    sleeveLeft = patternGeneratorAsymmetry.generate_left_sleeve_polygon(individual)
    sleeveRight = patternGeneratorAsymmetry.generate_right_sleeve_polygon(individual)
    if waste[0].contains(front) and waste[1].contains(back) and waste[2].contains(sleeveLeft) and waste[3].contains(
            sleeveRight):
        area = back.area + front.area + sleeveLeft.area + sleeveRight.area
    else:
        area = 0
    return (area,)  # Return a tuple with the area


def evaluateCentroidSymmetry(individual, waste):
    front = patternGeneratorSymmetry.generate_shirt_front_polygon(individual)
    back = patternGeneratorSymmetry.generate_shirt_back_polygon(individual)
    sleeveLeft = patternGeneratorSymmetry.generate_sleeve_polygon(individual)
    sleeveRight = patternGeneratorSymmetry.generate_sleeve_polygon(individual)

    frontCentroid = front.centroid
    backCentroid = back.centroid
    sleeveLeftCentroid = sleeveLeft.centroid
    sleeveRightCentroid = sleeveRight.centroid

    # Correcting translation logic
    translated_front = shapely.affinity.translate(front, xoff=waste[0].centroid.x - frontCentroid.x,
                                                  yoff=waste[0].centroid.y - frontCentroid.y)
    translated_back = shapely.affinity.translate(back, xoff=waste[1].centroid.x - backCentroid.x,
                                                 yoff=waste[1].centroid.y - backCentroid.y)
    translated_sleeveLeft = shapely.affinity.translate(sleeveLeft, xoff=waste[2].centroid.x - sleeveLeftCentroid.x,
                                                       yoff=waste[2].centroid.y - sleeveLeftCentroid.y)
    translated_sleeveRight = shapely.affinity.translate(sleeveRight, xoff=waste[3].centroid.x - sleeveRightCentroid.x,
                                                        yoff=waste[3].centroid.y - sleeveRightCentroid.y)

    # Evaluate area based on containment and rotation conditions
    area = 0
    if waste[0].contains(translated_front) or waste[0].contains(
            shapely.affinity.rotate(translated_front, 180, 'center')):
        if waste[1].contains(translated_back) or waste[1].contains(
                shapely.affinity.rotate(translated_back, 180, 'center')):
            if waste[2].contains(translated_sleeveLeft) or waste[2].contains(
                    shapely.affinity.rotate(translated_sleeveLeft, 180, 'center')):
                if waste[3].contains(translated_sleeveRight) or waste[3].contains(
                        shapely.affinity.rotate(translated_sleeveRight, 180, 'center')):
                    area = back.area + front.area + sleeveLeft.area + sleeveRight.area

    return (area,)  # Return a tuple with the area


def evaluateCentroidAsymmetry(individual, waste):
    # Generate the polygons
    front = patternGeneratorAsymmetry.generate_shirt_front_polygon(individual)
    back = patternGeneratorAsymmetry.generate_shirt_back_polygon(individual)
    sleeveLeft = patternGeneratorAsymmetry.generate_left_sleeve_polygon(individual)
    sleeveRight = patternGeneratorAsymmetry.generate_right_sleeve_polygon(individual)

    # accessing centroids
    frontCentroid = front.centroid
    backCentroid = back.centroid
    sleeveLeftCentroid = sleeveLeft.centroid
    sleeveRightCentroid = sleeveRight.centroid

    # Correcting translation logic
    translated_front = shapely.affinity.translate(front, xoff=waste[0].centroid.x - frontCentroid.x,
                                                  yoff=waste[0].centroid.y - frontCentroid.y)
    translated_back = shapely.affinity.translate(back, xoff=waste[1].centroid.x - backCentroid.x,
                                                 yoff=waste[1].centroid.y - backCentroid.y)
    translated_sleeveLeft = shapely.affinity.translate(sleeveLeft, xoff=waste[2].centroid.x - sleeveLeftCentroid.x,
                                                       yoff=waste[2].centroid.y - sleeveLeftCentroid.y)
    translated_sleeveRight = shapely.affinity.translate(sleeveRight, xoff=waste[3].centroid.x - sleeveRightCentroid.x,
                                                        yoff=waste[3].centroid.y - sleeveRightCentroid.y)

    # Evaluate area based on containment and rotation conditions
    area = 0
    if waste[0].contains(translated_front) or waste[0].contains(
            shapely.affinity.rotate(translated_front, 180, 'center')):
        if waste[1].contains(translated_back) or waste[1].contains(
                shapely.affinity.rotate(translated_back, 180, 'center')):
            if waste[2].contains(translated_sleeveLeft) or waste[2].contains(
                    shapely.affinity.rotate(translated_sleeveLeft, 180, 'center')):
                if waste[3].contains(translated_sleeveRight) or waste[3].contains(
                        shapely.affinity.rotate(translated_sleeveRight, 180, 'center')):
                    area = back.area + front.area + sleeveLeft.area + sleeveRight.area

    return (area,)  # Return a tuple with the area


def evaluateCutOutAsymmetry(individual, waste):
    # Generate polygons for each shirt component using the pattern generator
    front = patternGeneratorAsymmetry.generate_shirt_front_polygon(individual)
    back = patternGeneratorAsymmetry.generate_shirt_back_polygon(individual)
    sleeveLeft = patternGeneratorAsymmetry.generate_left_sleeve_polygon(individual)
    sleeveRight = patternGeneratorAsymmetry.generate_right_sleeve_polygon(individual)

    # Translate each component based on individual's specific shift data
    front = affinity.translate(front,
                               xoff=individual['front_x_shift'],
                               yoff=individual['front_y_shift'])
    back = affinity.translate(back,
                              xoff=individual['back_x_shift'],
                              yoff=individual['back_y_shift'])
    sleeveLeft = affinity.translate(sleeveLeft,
                                    xoff=individual['sleeve_left_x_shift'],
                                    yoff=individual['sleeve_left_y_shift'])
    sleeveRight = affinity.translate(sleeveRight,
                                     xoff=individual['sleeve_right_x_shift'],
                                     yoff=individual['sleeve_right_y_shift'])

    # Initialize total area used
    area = 0

    # Check each component's placement within the waste material
    # and ensure that components do not cross over each other
    if waste.contains(front) and not (
            front.intersects(back) or front.intersects(sleeveLeft) or front.intersects(sleeveRight)):
        if waste.contains(back) and not (back.intersects(sleeveLeft) or back.intersects(sleeveRight)):
            if waste.contains(sleeveLeft) and not sleeveLeft.intersects(sleeveRight):
                if waste.contains(sleeveRight):
                    # Sum the areas of all components if all conditions are met
                    area = front.area + back.area + sleeveLeft.area + sleeveRight.area

    return (area,)  # Return a tuple with the area


def mate(ind1, ind2, indpb):
    """ Custom crossover that performs uniform crossover for dictionary-based individuals. """
    for key in ind1:
        if random.random() < indpb:
            ind1[key], ind2[key] = ind2[key], ind1[key]
    return ind1, ind2


def mutate(individual, indpb):
    if random.random() < 0.5:
        return mutateNew(individual, indpb)
    else:
        return mutateDiff(individual, indpb)


def mutateNew(individual, indpb):
    """ Custom mutation that mutates an integer in a dictionary based on its specific bounds. """
    for key in individual:
        if random.random() < indpb:
            if key == 'x_shift' or key == 'y_shift':
                individual[key] = individual[key] - random.randint(-5, 5)
            individual[key] = random.randint(measurements_bounds_dict[key][0], measurements_bounds_dict[key][1])
    return individual,


def mutateDiff(individual, indpb):
    """ Custom mutation that mutates an integer in a dictionary based on its specific bounds. """
    for key in individual:
        if random.random() < indpb:
            diff = random.randint(-5, 5)
            if key == 'x_shift' or key == 'y_shift':
                individual[key] = individual[key] - diff
            elif measurements_bounds_dict[key][0] <= (individual[key] - diff) <= measurements_bounds_dict[key][1]:
                individual[key] = individual[key] - diff
            elif measurements_bounds_dict[key][0] <= (individual[key] + diff) <= measurements_bounds_dict[key][1]:
                individual[key] = individual[key] + diff
            else:
                individual[key] = individual[key]

    return individual,
