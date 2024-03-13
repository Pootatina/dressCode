from pieces.patternPiece import PatternPiece

class Front(PatternPiece):
    def __init__(self, fname, lname, neckline):
        super().__init__(fname, lname)
        self.neckline = 32

    def welcome(self):
        print("Welcome", self.firstname, self.lastname, "to the class of", self.neckline)

    def generate(self):
        print("Hello my name is " + self.name)

p1 = Front("John", 36, 34)

print(p1)
print('hey')     