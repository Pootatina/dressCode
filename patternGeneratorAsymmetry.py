from shapely.geometry import Polygon

import bezierCode


def generate_shirt_back_polygon(measurements):
    # mirrored
    side_width = (measurements['waist_width'] - measurements['bust_width']) / 2  # Assuming symmetry for example
    side_height_left = measurements['side_length_right']
    side_height_right = measurements['side_length_left']
    neckline_width = measurements['neckline_width']
    neckline_height = measurements['neckline_height_front']
    armhole_width_left = measurements['armhole_width_right']
    armhole_width_right = measurements['armhole_width_left']
    armhole_height_left = measurements['armhole_height_right']
    armhole_height_right = measurements['armhole_height_left']
    shoulder_width_left = (measurements['bust_width'] / 2) - (neckline_width / 2) - armhole_width_left
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
    side_width = (measurements['waist_width'] - measurements['bust_width']) / 2  # Assuming symmetry for example
    side_height_left = measurements['side_length_left']
    side_height_right = measurements['side_length_right']
    neckline_width = measurements['neckline_width']
    neckline_height = measurements['neckline_height_front']
    armhole_width_left = measurements['armhole_width_left']
    armhole_width_right = measurements['armhole_width_right']
    armhole_height_left = measurements['armhole_height_left']
    armhole_height_right = measurements['armhole_height_right']
    shoulder_width_left = (measurements['bust_width'] / 2) - (neckline_width / 2) - armhole_width_left
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


def generate_left_sleeve_polygon(measurements):
    armhole_width = measurements['armhole_width_left']
    armhole_height = measurements['armhole_height_left']
    sleeve_length = measurements['sleeve_length_left']
    sleeve_width = measurements['sleeve_width_left']
    side_width = (armhole_height * 2 - sleeve_width) / 2
    side_height = sleeve_length - armhole_width

    # Base points
    point_a = (150, 300)  # Start point
    point_b = (point_a[0] + side_width, point_a[1] - side_height)  # Start of left sleeve curve
    point_c = (point_b[0] + armhole_height, point_b[1] - armhole_width)  # End of left sleeve curve
    point_d = (point_c[0] + armhole_height, point_c[1] + armhole_width)  # start of right sleeve curve
    point_e = (point_d[0] + side_width, point_d[1] + side_height)  # End of right sleeve curve

    # Control points for inward curving sleeves
    control_left = (point_b[0] + armhole_width / 2, point_c[1])
    control_right = (point_d[0] - armhole_width / 2, point_c[1])

    # Generate curves using Bézier
    curve_left = bezierCode.bezier_curve(point_b, control_left, point_c)
    curve_right = bezierCode.bezier_curve(point_c, control_right, point_d)

    # Points list, including curves
    points = [point_a, *curve_left, *curve_right, point_e, point_a]

    # Create the polygon from the points
    polygon = Polygon(points)
    return polygon


def generate_right_sleeve_polygon(measurements):
    armhole_width = measurements['armhole_width_right']
    armhole_height = measurements['armhole_height_right']
    sleeve_length = measurements['sleeve_length_right']
    sleeve_width = measurements['sleeve_width_right']
    side_width = (armhole_height * 2 - sleeve_width) / 2

    # Base points
    point_a = (150, 300)  # Start point
    point_b = (point_a[0] + side_width, point_a[1] - sleeve_length)  # Start of right sleeve curve
    point_c = (point_b[0] + armhole_height, point_b[1] - armhole_width)  # End of left sleeve curve
    point_d = (point_c[0] + armhole_height, point_c[1] + armhole_width)  # start of right sleeve curve
    point_e = (point_d[0] + side_width, point_d[1] + sleeve_length)  # End of right sleeve curve

    # Control points for inward curving sleeves
    control_left = (point_b[0] + armhole_width / 2, point_c[1])
    control_right = (point_d[0] - armhole_width / 2, point_c[1])

    # Generate curves using Bézier
    curve_left = bezierCode.bezier_curve(point_b, control_left, point_c)
    curve_right = bezierCode.bezier_curve(point_c, control_right, point_d)

    # Points list, including curves
    points = [point_a, *curve_left, *curve_right, point_e, point_a]

    # Create the polygon from the points
    polygon = Polygon(points)
    return polygon




