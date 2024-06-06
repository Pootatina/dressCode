from shapely.geometry import Polygon
import svgwrite

def get_hardcoded_complex_polygons():
    # Define four hardcoded complex polygons with additional vertices
    return [
        Polygon([(10, 10), (160, 5), (180, 10), (145, 120), (85, 85), (60, 100), (10, 145)]),
        Polygon([(250, 30), (350, 5), (340, 120), (360, 210), (160, 120), (180, 85), (210, 5)]),
        Polygon([(30, 135), (75, 100), (110, 110), (100, 150), (130, 240), (30, 270), (5, 195)]),
        Polygon([(120, 150), (110, 125), (240, 180), (290, 210), (155, 265), (135, 225), (120, 150)])
    ]

def create_svg_with_polygons(filename):
    # Get polygons
    polygons = get_hardcoded_complex_polygons()
    dwg = svgwrite.Drawing(filename, profile='tiny')

    # Iterate over each polygon to add them to the SVG
    for poly in polygons:
        # Extract points and create SVG path data
        points = [(x, y) for x, y in poly.exterior.coords]
        poly_path = dwg.add(dwg.polygon(points))
        poly_path.fill('none').stroke('black', width=1)

    # Save the SVG file
    dwg.save()

# Use the function to create an SVG file
create_svg_with_polygons('complex_polygons.svg')
