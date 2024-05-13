import numpy as np
from shapely import LineString


def calculate_bezier_length(points):
    """Calculate the approximate length of a Bézier curve defined by its points."""
    line = LineString(points)
    return line.length

def bezier_curve(p0, p1, p2, num_points=20):
    """Generate points for a quadratic Bézier curve."""
    # Creating a linspace array t that goes from 0 to 1 with num_points elements
    t = np.linspace(0, 1, num_points)

    # Convert points to numpy arrays
    p0 = np.array(p0)
    p1 = np.array(p1)
    p2 = np.array(p2)

    # Reshape t to perform outer operation with points
    t = t.reshape(-1, 1)

    # Calculate the bezier curve
    curve = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2
    return curve


def bezier_curve_cubic(p0, p1, p2, p3, num_points=20):
    """Generate points for a cubic Bézier curve."""
    t = np.linspace(0, 1, num_points)

    # Reshape t to be a column vector for broadcasting
    t = t[:, np.newaxis]  # reshaping t to (num_points, 1)

    # Convert points to numpy arrays
    p0 = np.array(p0)
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    # Calculate the bezier curve
    curve = (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3
    return curve