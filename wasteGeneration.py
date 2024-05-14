from shapely.geometry import Polygon
import random


def generate_random_polygon(bounds, num_points=10):
    """
    Generate a random polygon within specified bounds.

    Parameters:
        bounds (tuple): A tuple of tuples ((min_x, max_x), (min_y, max_y)) defining the bounding box.
        num_points (int): The number of vertices the polygon should have.

    Returns:
        Polygon: A Shapely polygon object.
    """
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
