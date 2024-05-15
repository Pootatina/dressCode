import random

import shapely
from deap import creator
from shapely import Polygon, affinity

import patternGeneratorAsymmetry
import patternGeneratorSymmetry

# Setup DEAP fitness and individual structures

# Define possible values for the measurements
import svgHelper

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
    'waist_width'
]
bounds = [
    (20, 30), (5, 20), (2, 30), (0, 10), (0, 10), (20, 30), (20, 30), (0, 15),
    (0, 15), (25, 60), (0, 40), (0, 60), (0, 60), (50, 65), (20, 100), (20, 100),
    (45, 100)
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

    #accessing centroids
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
    # Generate polygons for each shirt component using a fictional pattern generator
    front = patternGeneratorAsymmetry.generate_shirt_front_polygon(individual)
    back = patternGeneratorAsymmetry.generate_shirt_back_polygon(individual)
    sleeveLeft = patternGeneratorAsymmetry.generate_left_sleeve_polygon(individual)
    sleeveRight = patternGeneratorAsymmetry.generate_right_sleeve_polygon(individual)

    # Translate each component to standardize starting positions
    components = [front, back, sleeveLeft, sleeveRight]
    components = [affinity.translate(comp, xoff=-150, yoff=-300) for comp in components]

    # Initialize total area used
    area = 0

    # Place each component into the waste polygon, check if placement was successful
    for comp in components:
        waste, placed = place(comp, waste)
        if not placed:
            return 0,
        area += placed.area

    # Save the final arrangement to SVG
    svgHelper.save_polygons_cutout_to_svg([waste] + components, "images/test.svg")

    return (area,)

def place(pattern, waste):
    """ Try to place a pattern onto the waste material; translate randomly if not fitting. """
    for attempt in range(1000):  # Attempt placement up to 1000 times
        if waste.contains(pattern):
            new_holes = list(waste.interiors) + [pattern.exterior.coords]
            waste = Polygon(waste.exterior, new_holes)
            return waste, pattern
        pattern = affinity.translate(pattern, xoff=random.randint(0, 600), yoff=random.randint(0, 600))
    return waste, None

def evaluateMove(individual, waste):
    shapely.affinity.translate(waste, xoff=50, yoff=100, zoff=0.0)
    if waste.contains(patternGeneratorSymmetry.generate_shirt_front_polygon(individual)):
        back = patternGeneratorSymmetry.generate_shirt_back_polygon(individual)
        front = patternGeneratorSymmetry.generate_shirt_front_polygon(individual)
        sleeveLeft = patternGeneratorSymmetry.generate_sleeve_polygon(individual)
        sleeveRight = patternGeneratorSymmetry.generate_sleeve_polygon(individual)
        area = back.area + front.area + sleeveLeft.area + sleeveRight.area  # Access the area property correctly
    else:
        area = 0
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
            individual[key] = random.randint(measurements_bounds_dict[key][0], measurements_bounds_dict[key][1])
    return individual,


def mutateDiff(individual, indpb):
    """ Custom mutation that mutates an integer in a dictionary based on its specific bounds. """
    for key in individual:
        if random.random() < indpb:
            diff = random.randint(-5, 5)
            if measurements_bounds_dict[key][0] <= (individual[key] - diff) <= measurements_bounds_dict[key][1]:
                individual[key] = individual[key] - diff
            elif measurements_bounds_dict[key][0] <= (individual[key] + diff) <= measurements_bounds_dict[key][1]:
                individual[key] = individual[key] + diff
            else:
                individual[key] = individual[key]

    return individual,
