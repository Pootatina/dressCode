from random import choice

import shapely
import svgwrite
from shapely import affinity


def save_polygon_to_svg(polygon, filename):
    # Create a new SVG drawing
    dwg = svgwrite.Drawing(filename, profile='tiny')

    # Extract polygon exterior coordinates
    points = polygon.exterior.coords

    # Convert points to a path data string
    path_data = "M" + " L".join(f"{x},{y}" for x, y in points) + " Z"

    # Add the path to the drawing
    dwg.add(dwg.path(d=path_data, fill="rgb(255, 167, 51)", stroke="black"))

    # Save the SVG to a file
    dwg.save()

    print(f"SVG file saved to {filename}")


def save_polygons_to_svg(polygons, filename):
    # Create a new SVG drawing
    dwg = svgwrite.Drawing(filename, profile='tiny')
    count = 0

    # Loop through each polygon in the list
    for polygon in polygons:

        if count % 2 == 0:
            if count > 0:
                polygon = shapely.affinity.translate(polygon, xoff=100*count, yoff=0, zoff=0.0)
            color = "rgb(77, 161, 169)"
        else:
            if count > 1:
                polygon = shapely.affinity.translate(polygon, xoff=100*(count-1), yoff=0, zoff=0.0)
            color = "rgb(255, 167, 51)"
        # Extract polygon exterior coordinates
        points = polygon.exterior.coords

        count = count + 1
        # Convert points to a path data string
        path_data = "M" + " L".join(f"{x},{y}" for x, y in points) + " Z"

        # Add the path to the drawing with consistent fill and stroke
        dwg.add(dwg.path(d=path_data, fill=color, stroke="black", stroke_width=1))

    # Save the SVG to a file
    dwg.save()

    print(f"SVG file saved to {filename}")


def save_polygons_cutout_to_svg(polygons, filename):
    # Create a new SVG drawing
    dwg = svgwrite.Drawing(filename, profile='tiny')
    count = 0

    # Loop through each polygon in the list
    for polygon in polygons:

        if count == 0:
            color = "rgb(77, 161, 169)"
        else:
            color = "rgb(255, 167, 51)"
        # Extract polygon exterior coordinates
        points = polygon.exterior.coords

        count = count + 1
        # Convert points to a path data string
        path_data = "M" + " L".join(f"{x},{y}" for x, y in points) + " Z"

        # Add the path to the drawing with consistent fill and stroke
        dwg.add(dwg.path(d=path_data, fill=color, stroke="black", stroke_width=1))

    # Save the SVG to a file
    dwg.save()

    print(f"SVG file saved to {filename}")

def save_holy_polygons_to_svg(polygons, filename):
    # Create a new SVG drawing
    dwg = svgwrite.Drawing(filename, profile='tiny')
    count = 0

    # Loop through each polygon in the list
    for polygon in polygons:
        # Apply translation based on the count to avoid overlap
        if count > 0:
            polygon = affinity.translate(polygon, xoff=100*count, yoff=0)

        # Choose color based on even/odd count
        color = "rgb(77, 161, 169)" if count % 2 == 0 else "rgb(255, 167, 51)"

        # Extract the exterior coordinates of the polygon
        exterior_points = polygon.exterior.coords
        path_data = "M" + " L".join(f"{x},{y}" for x, y in exterior_points) + " Z"

        # Add the exterior path to the drawing
        dwg.add(dwg.path(d=path_data, fill=color, stroke="black", stroke_width=1))

        # Process each interior boundary (hole)
        for interior in polygon.interiors:
            interior_points = interior.coords
            interior_path_data = "M" + " L".join(f"{x},{y}" for x, y in interior_points) + " Z"

            # Add the interior path to the drawing as a hole
            # Set fill="none" or use the same fill as the exterior to create a hole effect
            dwg.add(dwg.path(d=interior_path_data, fill="none", stroke="black", stroke_width=1))

        count += 1

    # Save the SVG to a file
    dwg.save()
    print(f"SVG file saved to {filename}")