import numpy

class Kaart:
    def __init__(self, resolutsioon="900x900",customMap=""):
        self.resolutsioon = resolutsioon
        if customMap == "":
            self.kaart = self.genereeriMap()
        else:
            self.kaart = customMap


    def drawMap(self,ekraan):

        pass

    def genereeriMap(self):
        kaart = numpy.array([1, 2, 3, 4, 5])

        return kaart
        pass
