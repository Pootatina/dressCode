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
                polygon = shapely.affinity.translate(polygon, xoff=100 * count, yoff=0, zoff=0.0)
            color = "rgb(77, 161, 169)"
        else:
            if count > 1:
                polygon = shapely.affinity.translate(polygon, xoff=100 * (count - 1), yoff=0, zoff=0.0)
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


def save_inPlace_polygons_to_svg(waste_polygons, polygons, filename):
    # Create a new SVG drawing
    dwg = svgwrite.Drawing(filename, profile='tiny')
    count = 0

    # Add holes of the main polygon
    for polygon in waste_polygons:
        points = polygon.exterior.coords
        path_data = "M" + " L".join(f"{x},{y}" for x, y in points) + " Z"
        dwg.add(dwg.path(d=path_data, fill="rgb(77, 161, 169)", stroke="black", stroke_width=1))

    # Add other polygons in different colors
    for polygon in polygons:
        points = polygon.exterior.coords
        path_data = "M" + " L".join(f"{x},{y}" for x, y in points) + " Z"
        dwg.add(dwg.path(d=path_data, fill="rgb(255, 167, 51)", stroke="black", stroke_width=1))

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


def save_polygons_with_holes_to_svg(main_polygon, other_polygons, filename):
    # Create a new SVG drawing
    dwg = svgwrite.Drawing(filename, profile='tiny')

    # Add the main polygon with holes
    main_exterior = main_polygon.exterior.coords
    main_path = "M " + " L ".join("{},{}".format(x, y) for x, y in main_exterior) + " Z"
    dwg.add(dwg.path(d=main_path, fill="rgb(77, 161, 169)", stroke="black", stroke_width=1))

    # Add holes of the main polygon
    for interior in main_polygon.interiors:
        interior_coords = interior.coords
        hole_path = "M " + " L ".join("{},{}".format(x, y) for x, y in interior_coords) + " Z"
        dwg.add(dwg.path(d=hole_path, fill="white", stroke="black", stroke_width=1))

    # Add other polygons in different colors
    for polygon in other_polygons:
        exterior = polygon.exterior.coords
        path = "M " + " L ".join("{},{}".format(x, y) for x, y in exterior) + " Z"
        dwg.add(dwg.path(d=path, fill="rgb(255, 167, 51)", stroke="black", stroke_width=1))

    # Save the SVG to a file
    dwg.save()
    print(f"SVG file saved to {filename}")
