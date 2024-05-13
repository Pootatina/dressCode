import numpy as np
import svgwrite
from shapely.geometry import Polygon, LineString

import bezierCode
import svgHelper


def generate_shirt_back_polygon(measurements):
    # mirrored
    side_width = (measurements['waist_width'] - measurements['bust_width'])/2   # Assuming symmetry for example
    side_height_left = measurements['side_length_right']
    side_height_right = measurements['side_length_left']
    neckline_width = measurements['neckline_width']
    neckline_height = measurements['neckline_height_front']
    armhole_width_left = measurements['armhole_width_right']
    armhole_width_right = measurements['armhole_width_left']
    armhole_height_left = measurements['armhole_height_right']
    armhole_height_right = measurements['armhole_height_left']
    shoulder_width_left = (measurements['bust_width']/2) - (neckline_width/2) - armhole_width_left
    shoulder_width_right = (measurements['bust_width'] / 2) - (neckline_width / 2) - armhole_width_right
    shoulder_height_left = measurements['shoulder_height_right']
    shoulder_height_right = measurements['shoulder_height_left']

    # Base points
    point_a = (150, 300)  # Start point
    point_b = (point_a[0] + side_width, point_a[1] - side_height_left)  # Lower left at hem
    point_c = (point_b[0] + armhole_width_left, point_b[1])  # Start of left sleeve curve
    point_d = (point_c[0], point_c[1] - armhole_height_left)  # End of left sleeve curve, start of left shoulder
    point_e = (point_d[0] + shoulder_width_left, point_d[1] - shoulder_height_left)  # End of left shoulder
    point_f = (point_e[0] + neckline_width, point_e[1])  # Neckline middle
    point_g = (point_f[0] + shoulder_width_right, point_f[1] + shoulder_height_right)  # Start of right shoulder
    point_h = (point_g[0], point_g[1] + armhole_height_right)  # End of right shoulder, start of right sleeve curve
    point_i = (point_h[0] + armhole_width_right, point_h[1])  # End of right sleeve curve
    point_j = (point_i[0] + side_width, point_i[1] + side_height_right)  # Lower right at hem

    # Control points for inward curving sleeves
    control_left = (point_c[0], point_c[1] - armhole_height_left / 2)
    control_right = (point_h[0], point_h[1] - armhole_height_right / 2)

    # Control point for a subtle inward neckline curve
    neckline_control = (point_e[0] + (point_f[0] - point_e[0]) / 2, point_e[1] + neckline_height / 2)

    # Generate curves using Bézier
    curve_left = bezierCode.bezier_curve(point_b, control_left, point_d)
    curve_right = bezierCode.bezier_curve(point_g, control_right, point_i)

    # Curve for the subtle neckline
    neckline_curve = bezierCode.bezier_curve(point_e, neckline_control, point_f)

    # Points list, including curves
    points = [point_a, *curve_left, *neckline_curve, point_g, *curve_right, point_j, point_a]

    # Create the polygon from the points
    polygon = Polygon(points)
    return polygon


def generate_shirt_front_polygon(measurements):
    side_width = (measurements['waist_width'] - measurements['bust_width'])/2   # Assuming symmetry for example
    side_height_left = measurements['side_length_left']
    side_height_right = measurements['side_length_right']
    neckline_width = measurements['neckline_width']
    neckline_height = measurements['neckline_height_front']
    armhole_width_left = measurements['armhole_width_left']
    armhole_width_right = measurements['armhole_width_right']
    armhole_height_left = measurements['armhole_height_left']
    armhole_height_right = measurements['armhole_height_right']
    shoulder_width_left = (measurements['bust_width']/2) - (neckline_width/2) - armhole_width_left
    shoulder_width_right = (measurements['bust_width'] / 2) - (neckline_width / 2) - armhole_width_right
    shoulder_height_left = measurements['shoulder_height_left']
    shoulder_height_right = measurements['shoulder_height_right']

    # Base points
    point_a = (150, 300)  # Start point
    point_b = (point_a[0] + side_width, point_a[1] - side_height_left)  # Lower left at hem
    point_c = (point_b[0] + armhole_width_left, point_b[1])  # Start of left sleeve curve
    point_d = (point_c[0], point_c[1] - armhole_height_left)  # End of left sleeve curve, start of left shoulder
    point_e = (point_d[0] + shoulder_width_left, point_d[1] - shoulder_height_left)  # End of left shoulder
    point_f = (point_e[0] + neckline_width, point_e[1])  # Neckline middle
    point_g = (point_f[0] + shoulder_width_right, point_f[1] + shoulder_height_right)  # Start of right shoulder
    point_h = (point_g[0], point_g[1] + armhole_height_right)  # End of right shoulder, start of right sleeve curve
    point_i = (point_h[0] + armhole_width_right, point_h[1])  # End of right sleeve curve
    point_j = (point_i[0] + side_width, point_i[1] + side_height_right)  # Lower right at hem

    # Control points for inward curving sleeves
    control_left = (point_c[0], point_c[1] - armhole_height_left / 2)
    control_right = (point_h[0], point_h[1] - armhole_height_right / 2)

    # Generate curves using Bézier
    curve_left = bezierCode.bezier_curve(point_b, control_left, point_d)
    curve_right = bezierCode.bezier_curve(point_g, control_right, point_i)

    # Adjust control point for the neckline based on its height
    neckline_control = (point_e[0] + (point_f[0] - point_e[0]) / 2, point_e[1] + neckline_height)

    # Curve for the neckline
    neckline_curve = bezierCode.bezier_curve(point_e, neckline_control, point_f)

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
    curve_bc = bezierCode.bezier_curve_cubic(point_b, control_b1, control_b2, point_c, num_points=30)
    curve_cd = bezierCode.bezier_curve_cubic(point_c, control_c1, control_c2, point_d, num_points=30)

    # Points list, including curves
    points = [point_a, *curve_bc, *curve_cd, point_e, point_a]

    # Create the polygon from the points
    polygon = Polygon(points)
    return polygon


# Assume bezier_curve function is already defined and correctly computes the curve points
# Generate curves for the armholes and the sleeve top
# Example control points for demonstration; replace these with your actual points and control points
front_armhole_curve = bezierCode.bezier_curve((100, 100), (110, 90), (120, 100), num_points=100)
back_armhole_curve = bezierCode.bezier_curve((120, 100), (130, 90), (140, 100), num_points=100)
sleeve_top_curve = bezierCode.bezier_curve_cubic((100, 100), (105, 85), (115, 85), (120, 100), num_points=100)

# Calculate lengths
front_armhole_length = bezierCode.calculate_bezier_length(front_armhole_curve)
back_armhole_length = bezierCode.calculate_bezier_length(back_armhole_curve)
sleeve_top_length = bezierCode.calculate_bezier_length(sleeve_top_curve)

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

