import random

import shapely
from deap import creator
from shapely import affinity, difference

import patternGeneratorAsymmetry
import patternGeneratorSymmetry

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
    (45, 100), (-100, 50), (-100, 50), (-100, 50), (-100, 50), (-100, 50), (-100, 50), (-100, 50), (-100, 50)
]
measurements_bounds_dict = dict(zip(measurements, bounds))


# Function to initialize individuals with random measurements within defined bounds.
def init_individual():
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
    front = affinity.translate(front, xoff=individual['front_x_shift'], yoff=individual['front_y_shift'])
    back = affinity.translate(back, xoff=individual['back_x_shift'], yoff=individual['back_y_shift'])
    sleeveLeft = affinity.translate(sleeveLeft, xoff=individual['sleeve_left_x_shift'],
                                    yoff=individual['sleeve_left_y_shift'])
    sleeveRight = affinity.translate(sleeveRight, xoff=individual['sleeve_right_x_shift'],
                                     yoff=individual['sleeve_right_y_shift'])

    # Initialize total area used
    area = 0

    # Define a function to check if a component fits in any waste piece
    def fits_in_any_waste(component):
        return waste.contains(component)

    # Check if all components fit in any of the waste pieces and don't intersect each other
    if ((fits_in_any_waste(front) and not (
            front.intersects(back) or front.intersects(sleeveLeft) or front.intersects(sleeveRight)))
            and (fits_in_any_waste(back) and not (back.intersects(sleeveLeft) or back.intersects(sleeveRight)))
            and (fits_in_any_waste(sleeveLeft) and not sleeveLeft.intersects(sleeveRight))
            and fits_in_any_waste(sleeveRight)):
        # Sum the areas of all components if all conditions are met
        area = front.area + back.area + sleeveLeft.area + sleeveRight.area

    return (area,)  # Return a tuple with the area


def evaluatePlacementAsymmetry(individual, waste):
    # Generate polygons for each shirt component using the pattern generator
    front = patternGeneratorAsymmetry.generate_shirt_front_polygon(individual)
    back = patternGeneratorAsymmetry.generate_shirt_back_polygon(individual)
    sleeveLeft = patternGeneratorAsymmetry.generate_left_sleeve_polygon(individual)
    sleeveRight = patternGeneratorAsymmetry.generate_right_sleeve_polygon(individual)

    # Translate each component based on individual's specific shift data
    front = (affinity.translate(front, xoff=individual['front_x_shift'], yoff=individual['front_y_shift'])).buffer(0)
    back = (affinity.translate(back, xoff=individual['back_x_shift'], yoff=individual['back_y_shift'])).buffer(0)
    sleeveLeft = (affinity.translate(sleeveLeft, xoff=individual['sleeve_left_x_shift'],
                                     yoff=individual['sleeve_left_y_shift'])).buffer(0)
    sleeveRight = (affinity.translate(sleeveRight, xoff=individual['sleeve_right_x_shift'],
                                      yoff=individual['sleeve_right_y_shift'])).buffer(0)

    # Initialize total area used
    area = 0

    # Define a function to check if a component fits in any waste piece
    def fits_in_any_waste(component):
        return any(w.contains(component) for w in waste)

    # Check if all components fit in any of the waste pieces and don't intersect each other
    if ((fits_in_any_waste(front) and not (
            front.intersects(back) or front.intersects(sleeveLeft) or front.intersects(sleeveRight)))
            and (fits_in_any_waste(back) and not (back.intersects(sleeveLeft) or back.intersects(sleeveRight)))
            and (fits_in_any_waste(sleeveLeft) and not sleeveLeft.intersects(sleeveRight))
            and fits_in_any_waste(sleeveRight)):
        # Sum the areas of all components if all conditions are met
        area = front.area + back.area + sleeveLeft.area + sleeveRight.area

    return (area,)  # Return a tuple with the area


def evaluatePlacementAsymmetryImproved(individual, waste):
    # Generate polygons for each shirt component using the pattern generator
    front = patternGeneratorAsymmetry.generate_shirt_front_polygon(individual)
    back = patternGeneratorAsymmetry.generate_shirt_back_polygon(individual)
    sleeveLeft = patternGeneratorAsymmetry.generate_left_sleeve_polygon(individual)
    sleeveRight = patternGeneratorAsymmetry.generate_right_sleeve_polygon(individual)

    # Translate each component based on individual's specific shift data
    front = (affinity.translate(front, xoff=individual['front_x_shift'], yoff=individual['front_y_shift'])).buffer(0)
    back = (affinity.translate(back, xoff=individual['back_x_shift'], yoff=individual['back_y_shift'])).buffer(0)
    sleeveLeft = (affinity.translate(sleeveLeft, xoff=individual['sleeve_left_x_shift'],
                                     yoff=individual['sleeve_left_y_shift'])).buffer(0)
    sleeveRight = (affinity.translate(sleeveRight, xoff=individual['sleeve_right_x_shift'],
                                      yoff=individual['sleeve_right_y_shift'])).buffer(0)

    # Initialize total area used
    area = 0

    # Define a function to check if a component fits in any waste piece
    def fits_in_any_waste(component):
        return any(w.contains(component) for w in waste)

    # Check if all components fit in any of the waste pieces and don't intersect each other
    if ((fits_in_any_waste(front) and not (
            front.intersects(back) or front.intersects(sleeveLeft) or front.intersects(sleeveRight)))
            and (fits_in_any_waste(back) and not (back.intersects(sleeveLeft) or back.intersects(sleeveRight)))
            and (fits_in_any_waste(sleeveLeft) and not sleeveLeft.intersects(sleeveRight))
            and fits_in_any_waste(sleeveRight)):
        # Sum the areas of all components if all conditions are met
        area = (front.area + back.area + sleeveLeft.area + sleeveRight.area) * 100
    elif not (front.intersects(back) or front.intersects(sleeveLeft) or front.intersects(sleeveRight)) and not (
            back.intersects(sleeveLeft) or back.intersects(sleeveRight)) and not sleeveLeft.intersects(sleeveRight):
        area = area + sum(
            w.intersection(front).area - (difference(front, w).area if front.intersects(w) else 0) for w in waste)
        area = area + sum(w.intersection(back).area - (difference(back, w).area if back.intersects(w) else 0) for w in waste)
        area = area + sum(
            w.intersection(sleeveLeft).area - (difference(sleeveLeft, w).area if sleeveLeft.intersects(w) else 0) for w in
            waste)
        area = area + sum(
            w.intersection(sleeveRight).area - (difference(sleeveRight, w).area if sleeveRight.intersects(w) else 0) for w in
            waste)
        # count the intersections
        count=0
        for part in [front, back, sleeveLeft, sleeveRight]:
            if any(part.intersects(w) for w in waste):
                count += 1
        area = area*(count/4)
    return (area,)  # Return a tuple with the area


def mate(ind1, ind2, indpb):
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
    for key in individual:
        if random.random() < indpb:
            individual[key] = random.randint(measurements_bounds_dict[key][0], measurements_bounds_dict[key][1])
    return individual,


def mutateDiff(individual, indpb):
    for key in individual:
        if random.random() < indpb:
            diff = random.randint(-10, 10)
            if measurements_bounds_dict[key][0] <= (individual[key] - diff) <= measurements_bounds_dict[key][1]:
                individual[key] = individual[key] - diff
            elif measurements_bounds_dict[key][0] <= (individual[key] + diff) <= measurements_bounds_dict[key][1]:
                individual[key] = individual[key] + diff
            else:
                individual[key] = individual[key]

    return individual,


def mutateShift(individual, min_x, min_y, max_x, max_y, indpb):
    if random.random() < 0.5:
        return mutateNewShift(individual, indpb)
    else:
        return mutateDiffShift(individual, min_x, min_y, max_x, max_y, indpb)


def mutateNewShift(individual, indpb):
    for key in individual:
        if random.random() < indpb:
            individual[key] = random.randint(measurements_bounds_dict[key][0], measurements_bounds_dict[key][1])
    return individual,


def mutateDiffShift(individual, min_x, min_y, max_x, max_y, indpb):
    for key in individual:
        if random.random() < indpb:
            diff = random.randint(-10, 10)
            if key.endswith('x_shift'):
                if min_x <= (100 + individual[key] - diff) <= max_x:
                    individual[key] = individual[key] - diff
                elif min_x <= (100 + individual[key] + diff) <= max_x:
                    individual[key] = individual[key] + diff
            elif key.endswith('y_shift'):
                if min_y <= (100 + individual[key] - diff) <= max_y:
                    individual[key] = individual[key] - diff
                elif min_y <= (100 + individual[key] + diff) <= max_y:
                    individual[key] = individual[key] + diff
            elif measurements_bounds_dict[key][0] <= (individual[key] - diff) <= measurements_bounds_dict[key][1]:
                individual[key] = individual[key] - diff
            elif measurements_bounds_dict[key][0] <= (individual[key] + diff) <= measurements_bounds_dict[key][1]:
                individual[key] = individual[key] + diff
            else:
                individual[key] = individual[key]

    return individual,
