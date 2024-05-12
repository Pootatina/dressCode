import numpy as np
import svgwrite
from shapely.geometry import Polygon, LineString


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


def generate_shirt_back_polygon(side_width_back=5, side_height_back=40,
                                neckline_width_back=20, neckline_height_back=5,
                                sleeve_width_back=10, sleeve_height_back=30,
                                shoulder_width_back=15, shoulder_height_back=5,
                                width=80, length=60):
    # Base points
    point_a = (100, 100)  # Start point
    point_b = (point_a[0] + side_width_back, point_a[1] - side_height_back)  # Lower left at hem
    point_c = (point_b[0] + sleeve_width_back, point_b[1])  # Start of left sleeve curve
    point_d = (point_c[0], point_c[1] - sleeve_height_back)  # End of left sleeve curve, start of left shoulder
    point_e = (point_d[0] + shoulder_width_back, point_d[1] - shoulder_height_back)  # End of left shoulder
    point_f = (point_e[0] + neckline_width_back, point_e[1])  # Neckline middle
    point_g = (point_f[0] + shoulder_width_back, point_f[1] + shoulder_height_back)  # Start of right shoulder
    point_h = (point_g[0], point_g[1] + sleeve_height_back)  # End of right shoulder, start of right sleeve curve
    point_i = (point_h[0] + sleeve_width_back, point_h[1])  # End of right sleeve curve
    point_j = (point_i[0] + side_width_back, point_i[1] + side_height_back)  # Lower right at hem

    # Control points for inward curving sleeves
    control_left = (point_c[0], point_c[1] - sleeve_height_back / 2)
    control_right = (point_h[0], point_h[1] - sleeve_height_back / 2)

    # Control point for a subtle inward neckline curve
    neckline_control = (point_e[0] + (point_f[0] - point_e[0]) / 2, point_e[1] + neckline_height_back / 2)

    # Generate curves using Bézier
    curve_left = bezier_curve(point_b, control_left, point_d)
    curve_right = bezier_curve(point_g, control_right, point_i)

    # Curve for the subtle neckline
    neckline_curve = bezier_curve(point_e, neckline_control, point_f)

    # Points list, including curves
    points = [point_a, *curve_left, *neckline_curve, point_g, *curve_right, point_j, point_a]

    # Create the polygon from the points
    polygon = Polygon(points)
    return polygon


def generate_shirt_front_polygon(side_width_front=40, side_height_front=40,
                                 neckline_width_front=20, neckline_height_front=30,
                                 sleeve_width_front=10, sleeve_height_front=30,
                                 shoulder_width_front=15, shoulder_height_front=5,
                                 width=80, length=60):
    # Base points
    point_a = (100, 100)  # Start point
    point_b = (point_a[0] + side_width_front, point_a[1] - side_height_front)  # Lower left at hem
    point_c = (point_b[0] + sleeve_width_front, point_b[1])  # Start of left sleeve curve
    point_d = (point_c[0], point_c[1] - sleeve_height_front)  # End of left sleeve curve, start of left shoulder
    point_e = (point_d[0] + shoulder_width_front, point_d[1] - shoulder_height_front)  # End of left shoulder
    point_f = (point_e[0] + neckline_width_front, point_e[1])  # Neckline middle
    point_g = (point_f[0] + shoulder_width_front, point_f[1] + shoulder_height_front)  # Start of right shoulder
    point_h = (point_g[0], point_g[1] + sleeve_height_front)  # End of right shoulder, start of right sleeve curve
    point_i = (point_h[0] + sleeve_width_front, point_h[1])  # End of right sleeve curve
    point_j = (point_i[0] + side_width_front, point_i[1] + side_height_front)  # Lower right at hem

    # Control points for inward curving sleeves
    control_left = (point_c[0], point_c[1] - sleeve_height_front / 2)
    control_right = (point_h[0], point_h[1] - sleeve_height_front / 2)

    # Generate curves using Bézier
    curve_left = bezier_curve(point_b, control_left, point_d)
    curve_right = bezier_curve(point_g, control_right, point_i)

    # Adjust control point for the neckline based on its height
    neckline_control = (point_e[0] + (point_f[0] - point_e[0]) / 2, point_e[1] + neckline_height_front)

    # Curve for the neckline
    neckline_curve = bezier_curve(point_e, neckline_control, point_f)

    # Points list, including curves
    points = [point_a, *curve_left, *neckline_curve, point_g, *curve_right, point_j, point_a]

    # Create the polygon from the points
    polygon = Polygon(points)
    return polygon


def generate_shirt_sleeve_polygon(sleeve_width_front=10, sleeve_height_front=30,
                                  sleeve_width_back=10, sleeve_height_back=30,
                                  sleeve_length=40, sleeve_width=45,
                                  right_sleeve=True):
    width = sleeve_height_front + sleeve_height_back
    shoulder = (sleeve_width_front + sleeve_width_back) / 2
    point_a = (100, 100)
    point_b = (point_a[0] - ((width - sleeve_width) / 2), point_a[1] - (sleeve_length - shoulder))
    control_b1 = (point_b[0] + sleeve_width_front, point_b[1])
    control_b2 = (point_b[0] + (sleeve_height_front * 0.25), point_b[1] - sleeve_width_front)
    point_c = (point_b[0] + sleeve_height_front, point_b[1] - sleeve_width_front)
    control_c1 = (point_c[0] + (sleeve_height_back * 0.75), point_c[1])
    control_c2 = (point_c[0] + sleeve_height_back - sleeve_width_back, point_c[1] + sleeve_width_back)
    point_d = (point_c[0] + sleeve_height_back, point_c[1] + sleeve_width_back)
    point_e = (point_d[0] - ((width - sleeve_width) / 2), point_d[1] + (sleeve_length - shoulder))

    # Generate curves using cubic Bézier
    curve_bc = bezier_curve_cubic(point_b, control_b1, control_b2, point_c, num_points=30)
    curve_cd = bezier_curve_cubic(point_c, control_c1, control_c2, point_d, num_points=30)

    # Points list, including curves
    points = [point_a, *curve_bc, *curve_cd, point_e, point_a]

    # Create the polygon from the points
    polygon = Polygon(points)
    return polygon


def save_polygon_to_svg(polygon, filename):
    # Create a new SVG drawing
    dwg = svgwrite.Drawing(filename, profile='tiny')

    # Extract polygon exterior coordinates
    points = polygon.exterior.coords

    # Convert points to a path data string
    path_data = "M" + " L".join(f"{x},{y}" for x, y in points) + " Z"

    # Add the path to the drawing
    dwg.add(dwg.path(d=path_data, fill="none", stroke="black"))

    # Save the SVG to a file
    dwg.save()

    print(f"SVG file saved to {filename}")

def calculate_bezier_length(points):
    """Calculate the approximate length of a Bézier curve defined by its points."""
    line = LineString(points)
    return line.length

# Assume bezier_curve function is already defined and correctly computes the curve points
# Generate curves for the armholes and the sleeve top
# Example control points for demonstration; replace these with your actual points and control points
front_armhole_curve = bezier_curve((100, 100), (110, 90), (120, 100), num_points=100)
back_armhole_curve = bezier_curve((120, 100), (130, 90), (140, 100), num_points=100)
sleeve_top_curve = bezier_curve_cubic((100, 100), (105, 85), (115, 85), (120, 100), num_points=100)

# Calculate lengths
front_armhole_length = calculate_bezier_length(front_armhole_curve)
back_armhole_length = calculate_bezier_length(back_armhole_curve)
sleeve_top_length = calculate_bezier_length(sleeve_top_curve)

# Sum of front and back armhole lengths
total_armhole_length = front_armhole_length + back_armhole_length

# Output the lengths to compare
print("Front Armhole Length:", front_armhole_length)
print("Back Armhole Length:", back_armhole_length)
print("Total Armhole Length:", total_armhole_length)
print("Sleeve Top Length:", sleeve_top_length)

# Check if they match or how close they are
if np.isclose(total_armhole_length, sleeve_top_length, rtol=0.05):  # Allowing 5% tolerance
    print("The armhole and sleeve top lengths are approximately equal.")
else:
    print("There is a discrepancy in the lengths.")

# Example usage:
back_shirt_polygon = generate_shirt_back_polygon()
print(back_shirt_polygon)  # Outputs the polygon object
print("Area of the polygon:", back_shirt_polygon.area)  # Example of accessing polygon property
save_polygon_to_svg(back_shirt_polygon, "polygonB.svg")

front_shirt_polygon = generate_shirt_front_polygon()
print(front_shirt_polygon)  # Outputs the polygon object
print("Area of the polygon:", front_shirt_polygon.area)  # Example of accessing polygon property
save_polygon_to_svg(front_shirt_polygon, "polygonF.svg")

sleeve_polygon = generate_shirt_sleeve_polygon()
print(sleeve_polygon)  # Outputs the polygon object
print("Area of the polygon:", sleeve_polygon.area)  # Example of accessing polygon property
save_polygon_to_svg(sleeve_polygon, "polygonS.svg")