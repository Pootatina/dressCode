# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from typing import List

from pieces import back
from pieces import front
from pieces import pattern
from pieces import patternPiece
from pieces import sleeve
from svgpathtools import svg2paths, wsvg
from deap import base, creator, tools, algorithms

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

FrontPattern = List[int]
BackPattern = List[int]
LeftSleevePattern = List[int]
RightSleevePattern = List[int]
Pattern = [FrontPattern, BackPattern, LeftSleevePattern, RightSleevePattern]
Population = List[Pattern]

def generate_pattern()-> Pattern:
    return

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.

def some():
    paths, attributes = svg2paths('patternGeneration/curve.svg')
    print(paths[0])
    print("path is continuous? ", paths[0].iscontinuous())
    print("path is closed? ", paths[0].isclosed())
    print(paths[0].area())

    paths, attributes = svg2paths('patternGeneration/curve1.svg')
    print(paths[0])
    print("path is continuous? ", paths[0].iscontinuous())
    print("path is closed? ", paths[0].isclosed())
    print(paths[0].area())

    paths, attributes = svg2paths('patternGeneration/curve2.svg')
    print(paths[0])
    print("path is continuous? ", paths[0].iscontinuous())
    print("path is closed? ", paths[0].isclosed())
    print(paths[0].area())
    #path.py wurde angepasst weil hat zu lange gedauert
    

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    some()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
