import numpy, pygame

class Kaart:
    def __init__(self, resolutsioon="900x900",customMap="",tileSuurus=50):
        self.resolutsioon = resolutsioon
        self.tileSuurus = tileSuurus
        self.kaardiLaius, self.kaardiKyrgus = self.teiseldaKaardiResolutsioon()
        if customMap == "":
            self.kaart = self.genereeriMap()
        else:
            self.kaart = customMap

    def teiseldaKaardiResolutsioon(self):
        ekraaniX,ekraaniY = map(int,self.resolutsioon.split("x"))

        return ekraaniX // self.tileSuurus, ekraaniY // self.tileSuurus

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
        Lõpuks tagastab jada rectidega mis tuleb joonistada, (nüüd kui mõtlen oleks loogilisem drawSeinad)
        """
        seinaPaksus = 3
        tagastavadRectid = []
        for reaArv,rida in enumerate(self.kaart):
            for reaIndex,tile in rida:
                if "N" in tile:
                    tagastavadRectid.append(pygame.Rect(
                        reaIndex * self.tileSuurus, reaArv * self.tileSuurus, self.tileSuurus,seinaPaksus))
                if "W" in tile:
                    tagastavadRectid.append(pygame.Rect(
                        reaIndex * self.tileSuurus, reaArv * self.tileSuurus,seinaPaksus, self.tileSuurus))
                if "E" in tile:
                    tagastavadRectid.append(pygame.Rect(
                        (reaIndex + 1) * self.tileSuurus, reaArv * self.tileSuurus, seinaPaksus, self.tileSuurus))
                if "S" in tile:
                    tagastavadRectid.append(pygame.Rect(
                        reaIndex * self.tileSuurus, (reaArv + 1) * self.tileSuurus, self.tileSuurus,seinaPaksus
                    ))
        return tagastavadRectid


        pass

    def genereeriMap(self):
        kaart = []
        for i in range(self.kaardiLaius):
            rida = []
            for j in range(self.kaardiKyrgus):
                rida.append("")
            kaart.append(rida)


        return kaart


    def lisaSeinad(self):
        for i in range(len(self.kaart[0])):
            self.kaart[0][i] = "N"
            self.kaart[-1][i] = "S"

        for i in range(len(self.kaart)):
            for j in [0, -1]:
                if j == 0:
                    self.kaart[i][j] = "W"
                else:
                    self.kaart[i][j] = "E"
        self.kaart[0][0] = "NW"
        self.kaart[0][len(self.kaart[0]) - 1] = "NE"
        self.kaart[len(self.kaart) - 1][0] = "SW"
        self.kaart[len(self.kaart) - 1][len(self.kaart[0]) - 1] = "SE"

if __name__ == "__main__":
    kaart = Kaart()
    kaart.lisaSeinad()
    for rida in kaart.kaart:
        print(rida)