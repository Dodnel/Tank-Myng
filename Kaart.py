import numpy

class Kaart:
    def __init__(self, resolutsioon="900x900",customMap=""):
        self.resolutsioon = resolutsioon
        if customMap == "":
            self.kaart = self.genereeriMap()
        else:
            self.kaart = customMap


    def drawMap(self,ekraan):
        """
        Tuleb otsustada kui suur üks tile on
        idee,
        Joonistamiseks, paneb igale tileile tyhti mis näitab mis ilmakaartel sellel tileil on sein
        N (north) tilei põhja suunas on sein
        S (south) tilei lõuna sunuas on sein
        W (west) sa saad aru
        E (east) sa saad aru
        Neid saab stackida ka et NSW on lubatud sisend yhe tile jaoks
        ning siis lõppu võib lisada veel mingi tähe mis tähitab tilei pilti kui me tahame keerulisemaid textuure
        nt: 3x3 map [["NW", "N", "NE"],
                     ["W", "", "E"],
                     ["SW", "S", "SE"]]

        :param ekraan:
        :return:
        """


        pass

    def genereeriMap(self):
        #idee
        kaart = numpy.array([1, 2, 3, 4, 5])

        return kaart
        pass
