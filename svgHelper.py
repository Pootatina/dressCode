import svgwrite


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