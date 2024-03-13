from svgpathtools import svg2paths, wsvg
import numpy as np


class PatternPiece:
    def __init__(self, a, path):
        self.name = a
        self.path = path

    def __str__(self):
        return f"{self.name}({self.path})"

    def myfunc(self):
        print("Hello my name is " + self.name)

    @property
    def area(self):
        path_area = (self.path)
        print("Fläche des Pfades:", path_area)


p1 = PatternPiece("John", 36)