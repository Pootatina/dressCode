from shapely.geometry import Polygon
import random

def create_wasteFabric(max_vertices=10, x_range=(0, 100), y_range=(0, 100)):
    num_vertices = random.randint(3, max_vertices)
    points = set()

    while len(points) < num_vertices:
        x = random.randint(*x_range)
        y = random.randint(*y_range)
        points.add((x, y))

    # Ensure points create a valid polygon
    poly = Polygon(list(points))
    if poly.is_valid:
        return poly
    else:
        return create_wasteFabric(max_vertices, x_range, y_range)  # Recursion to ensure a valid polygon

