import svgwrite
from svgpathtools import parse_path
from svgwrite import cm, mm

def load_svg(filename):
    with open(filename, 'r') as f:
        return parse_path(f.read())

def check_fit(big_bbox, small_bbox):
    return (small_bbox[2] <= big_bbox[2] and
            small_bbox[3] <= big_bbox[3])

def find_best_fit(big_bbox, small_bbox):
    x_offset = big_bbox[0] - small_bbox[0]
    y_offset = big_bbox[1] - small_bbox[1]

    if x_offset >= 0 and y_offset >= 0:
        return (x_offset, y_offset)
    else:
        return (0, 0)

def tryout():
    big_polygon_path = "../patternGeneration/test.svg"
    small_polygon_paths = ["patternGeneration/front.svg", "sleeve.svg", "sleeve.svg", "patternGeneration/back.svg"]

    big_polygon = load_svg(big_polygon_path)
    big_bbox = big_polygon.bbox()

    drawing = svgwrite.Drawing(filename="output.svg", size=('100%', '100%'))
    drawing.add(big_polygon)

    for path in small_polygon_paths:
        small_polygon = load_svg(path)
        small_bbox = small_polygon.bbox()

        if not check_fit(big_bbox, small_bbox):
            print("Fehler: Polygon " + path + " passt nicht ins Hauptpolygon.")
            return

        x_offset, y_offset = find_best_fit(big_bbox, small_bbox)
        translated_polygon = small_polygon.translate(x_offset, y_offset)
        drawing.add(translated_polygon)

    drawing.save()

tryout()