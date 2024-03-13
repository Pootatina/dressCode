from pieces.patternPiece import PatternPiece

class Sleeve(PatternPiece):
    def __init__(self, fname, lname, neckline):
        super.__init__(fname, lname)
        self.neckline = 32

    def welcome(self):
        print("Welcome", self.firstname, self.lastname, "to the class of", self.neckline)