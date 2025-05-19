from random import randint

import pygame, random
#s
class Kaart:
    def __init__(self, resolutsioon="900x900",customMap="",tileSuurus=50):
        self.resolutsioon = resolutsioon
        self.tileSuurus = tileSuurus
        self.kaardiLaius, self.kaardiKyrgus = self.teiseldaKaardiResolutsioon()
        if customMap == "":
            self.kaart = self.genereeriKaart()
        else:
            self.kaart = customMap
        self.spawnKaart = []


    def leiaTankideleTekkeKohad(self, tankidArv):
        self.spawnKaart = []
        self.voimalikudKohad = []

        for i in range(self.kaardiLaius):
            rida = []
            for j in range(self.kaardiKyrgus):
                rida.append((i,j))
                self.voimalikudKohad.append((i,j))

            self.spawnKaart.append(rida)

        def looRistkylik(kaheMyytmelineJada,x0,y0,x1,y1):
            for i in range(y0,y1):
                for j in range(x0,x1):
                    try:
                        kaheMyytmelineJada[i][j] = "#"
                    except:
                        pass

            return kaheMyytmelineJada

        for i in range(tankidArv, -1, -1):
            tankiX, tankiY  = randint(0, self.kaardiLaius), randint(0, self.kaardiKyrgus)

            blokk = looRistkylik(self.spawnKaart, tankiX-i, tankiY-i, tankiX+i, tankiY+i)


        return blokk








    def teiseldaKaardiResolutsioon(self):
        ekraaniX,ekraaniY = map(int,self.resolutsioon.split("x"))

        kaardiLaius = ekraaniX // self.tileSuurus
        kaardiKyrgus = ekraaniY // self.tileSuurus

        return kaardiLaius, kaardiKyrgus

    def drawMap(self):
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
        seinaPaksus = 2
        tagastavadRectid = []
        for reaArv,rida in enumerate(self.kaart):
            for reaIndex,tile in enumerate(rida):
                if "N" in tile:
                    tagastavadRectid.append(pygame.Rect(
                        reaIndex * self.tileSuurus, reaArv * self.tileSuurus, self.tileSuurus,seinaPaksus))
                if "W" in tile:
                    tagastavadRectid.append(pygame.Rect(
                        reaIndex * self.tileSuurus, reaArv * self.tileSuurus,seinaPaksus, self.tileSuurus))
                if "E" in tile:
                    tagastavadRectid.append(pygame.Rect(
                        (reaIndex + 1) * self.tileSuurus - seinaPaksus, reaArv * self.tileSuurus, seinaPaksus, self.tileSuurus))
                if "S" in tile:
                    tagastavadRectid.append(pygame.Rect(
                        reaIndex * self.tileSuurus, (reaArv + 1) * self.tileSuurus - seinaPaksus, self.tileSuurus,seinaPaksus
                    ))

        return tagastavadRectid

    def genereeriKaart(self):
        kaart = []
        for i in range(self.kaardiKyrgus):
            rida = []
            for j in range(self.kaardiLaius):
                rida.append("")
            kaart.append(rida)

        return kaart

    def randomizedKruskalAlgoritm(self):
        setid = {}
        kylastamataSeinad = []

        for i in range(self.kaardiKyrgus):
            for j in range(self.kaardiLaius):
                self.kaart[i][j] = "NSEW"
                setid[(i, j)] = {(i, j)}

                for orientatsioon in "NSEW":
                    if orientatsioon == "N" and i == 0:
                        pass
                    elif orientatsioon == "S" and i == self.kaardiKyrgus - 1:
                        pass
                    elif orientatsioon == "W" and j == 0:
                        pass
                    elif orientatsioon == "E" and j == self.kaardiLaius - 1:
                        pass
                    else:
                        kylastamataSeinad.append((i, j, orientatsioon))

        random.shuffle(kylastamataSeinad)

        for rida, veerg, orientatsioon  in kylastamataSeinad:
            if len(setid[(0, 0)]) == self.kaardiKyrgus * self.kaardiLaius:
                break

            match orientatsioon:
                case "N":
                    naaber = (rida - 1, veerg)
                    vastas = "S"
                case "S":
                    naaber = (rida + 1, veerg)
                    vastas = "N"
                case "E":
                    naaber = (rida, veerg + 1)
                    vastas = "W"
                case "W":
                    naaber = (rida, veerg - 1)
                    vastas = "E"

            if setid[(rida,veerg)] is not setid[naaber]:
                self.kaart[rida][veerg] = self.kaart[rida][veerg].replace(orientatsioon, "")
                self.kaart[naaber[0]][naaber[1]] = self.kaart[naaber[0]][naaber[1]].replace(vastas, "")

                uusSet = setid[(rida,veerg)].union(setid[naaber])
                for cell in uusSet:
                    setid[cell] = uusSet

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

        #nurgad
        self.kaart[0][0] = "NW"
        self.kaart[0][len(self.kaart[0]) - 1] = "NE"
        self.kaart[len(self.kaart) - 1][0] = "SW"
        self.kaart[len(self.kaart) - 1][len(self.kaart[0]) - 1] = "SE"

    def lammutaKaart(self):
        for rida in range(len(self.kaart)):
            for veerg in range(len(self.kaart)):
                self.kaart[rida][veerg] = ""


if __name__ == "__main__":
    kaart = Kaart(resolutsioon="1900x500")

    print(kaart.leiaTankideleTekkeKohad(2))
