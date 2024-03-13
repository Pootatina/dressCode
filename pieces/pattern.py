from pieces.front import Front
from pieces.back import Back
from pieces.sleeve import Sleeve

class Pattern:
    def __init__(pattern):
        pattern.front = Front()
        pattern.back = Back()
        pattern.sleeve_right = Sleeve()
        pattern.sleeve_left = Sleeve()    