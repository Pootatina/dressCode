from shapely.geometry import Polygon
import random


def generate_random_polygon(bounds, num_points=10):
    print("Received bounds:", bounds)
    min_x, max_x = bounds[0]
    min_y, max_y = bounds[1]

    # Generate random points within the bounds
    points = [(random.randint(min_x, max_x), random.randint(min_y, max_y)) for _ in range(num_points)]
    points.append((140, 310))
    print(points)
    # Create the polygon from the convex hull of these points to ensure a valid polygon
    polygon = Polygon(points).convex_hull

    return polygon


def generate_a_polygon(bounds, num_points=10):
    print("Received bounds:", bounds)
    min_x, max_x = bounds[0]
    min_y, max_y = bounds[1]

    # Generate random points within the bounds
    points = [(random.randint(min_x, max_x), random.randint(min_y, max_y)) for _ in range(num_points)]

    # Create the polygon from the convex hull of these points to ensure a valid polygon
    polygon = Polygon(points).convex_hull

    return polygon

def generate_fixed_polygons():
    return [
        Polygon([(10, 10), (160, 5), (180, 10), (145, 120), (85, 85), (60, 100), (10, 145)]),
        Polygon([(250, 30), (350, 5), (340, 120), (360, 210), (160, 120), (180, 85), (210, 5)]),
        Polygon([(30, 135), (75, 100), (110, 110), (100, 150), (130, 240), (30, 270), (5, 195)]),
        Polygon([(120, 150), (110, 125), (240, 180), (290, 210), (155, 265), (135, 225), (120, 150)])
    ]

def generate_realWasteOne():
    return [
        Polygon([(10, 10), (160, 10), (160, 130), (10, 130)]),
    ]

# Get bounds of the waste
def get_minmaxDrift(waste):
    min_x = 100
    min_y = 100
    max_x = 0
    max_y = 0
    for w in waste:
        minx, miny, maxx, maxy = w.bounds
        min_x = min(min_x, minx)
        min_y = min(min_y, miny)
        max_x = max(max_x, maxx)
        max_y = max(max_y, maxy)
    return min_x, min_y, max_x, max_y