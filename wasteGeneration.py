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
