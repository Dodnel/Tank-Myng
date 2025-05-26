from random import choice

import pygame, random

class Kaart:
    def __init__(self, kaardiLaius, kaardiKyrgus, tileSuurus=100, customMap=""):
        self.kaardiLaius = kaardiLaius
        self.kaardiKyrgus = kaardiKyrgus
        self.tileSuurus = tileSuurus

        if customMap == "":
            self.kaart = self.genereeriKaart()
        else:
            self.kaart = customMap

    def leiaTankideleTekkeKohad(self, tankideArv):
        """
        Leiab antud arv tankidele tekkekohad kaardile vaadates et tankid üksteies kõrvale ei panda.
        :param tankideArv: Mitu tanki on vaja kaardile mahutada
        :return: Tagastab järjendi antud tankide arvule spawn koordinaatidega
        """

        if tankideArv > self.kaardiLaius * self.kaardiKyrgus:
            raise Exception("Liiga palju tanke kaardi suuruse jaoks!")

        def looSpawnJaVoimalikudKohad():
            """
            Loob tühja spawnkaardi ja tekkekohad myngu ala suuruselt sõltuvalt
            :return: tagastab kaks järjendit, esimene kahemõõtmeline ja teine
            ühemõõtmeline iga kohe koordinaadiga
            """
            spawnKaart = []
            voimalikudTekkeKohad = []

            for i in range(self.kaardiLaius):
                rida = []
                for j in range(self.kaardiKyrgus):
                    rida.append((i, j))
                    voimalikudTekkeKohad.append((i, j))
                spawnKaart.append(rida)
            return spawnKaart, voimalikudTekkeKohad

        def looRistkylik(kaheMyytmelineJada, voimalikudKohad, x0, y0, x1, y1):
            """
            Blokeerib kahemõõtmelises jadas antud ala ristkülikuga ja eemaldab voimalikudest
            kohtadest ära kohad mis blokeeriti.
            :param kaheMyytmelineJada: kahemõõtmeline jada kuhu ristkülik asetakse
            :param voimalikudKohad: jada kust eemaldatakse blokeeritud kohad
            :param x0: ristküliku ülemine vasak nurga x
            :param y0: ristküliku ülemise vasak nurga y
            :param x1: ristküliku alumise parema nurga x
            :param y1: ristküliku aluse parema nurga y
            :return: tagastab kahemõõtmelise jada kus on eemaldatud ristküliku ala ja voimaliku kohtade jada
            kus on eemaldatud blokeeritud kohad
            """

            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    try:
                        kaheMyytmelineJada[x][y] = None
                        voimalikudKohad.remove((x, y))
                    except:
                        pass

            return kaheMyytmelineJada, voimalikudKohad


        ristkylikuRaadius = 5 #vaatab kui kaugel tankid üktsteiest olema peaksid
        if self.kaardiLaius >= self.kaardiKyrgus:
            ristKylikuRaadius = self.kaardiKyrgus
        else:
            ristkylikuRaadius = self.kaardiLaius


        tekkeKohad = []
        while len(tekkeKohad) < tankideArv:
            spawnKaart, voimalikudTekkeKohad = looSpawnJaVoimalikudKohad()
            tekkeKohad = []

            for i in range(tankideArv):
                if voimalikudTekkeKohad:
                    tankiX, tankiY = choice(voimalikudTekkeKohad)
                    spawnKaart, voimalikudTekkeKohad = looRistkylik(spawnKaart,voimalikudTekkeKohad,
                                                                    tankiX - ristKylikuRaadius,
                                                                    tankiY - ristKylikuRaadius,
                                                                    tankiX + ristkylikuRaadius,
                                                                    tankiY + ristkylikuRaadius)
                    tekkeKohad.append((tankiX, tankiY))
                else:
                    if ristkylikuRaadius > 1:
                        ristkylikuRaadius -= 1 #kohtde mitte leidmisel vähendakse blokeeritavat ala
                    break

        return tekkeKohad



    def saaResolutsioon(self):
        """
        muudab kaardi laiuse ja pikkuse pikslite suursele ja tagastab selle
        :return: tagastab kaardi resolutsiooni pikslites sõnena
        """
        return f"{self.tileSuurus*self.kaardiLaius}x{self.tileSuurus*self.kaardiKyrgus}"


    def drawMap(self):
        """
        Joonistamiseks, paneb igale tileile tyhti mis näitab mis ilmakaartel sellel tileil on sein
        N (north) põhja suunas on sein
        S (south) lõuna sunuas on sein
        W (west) lääne suunas on sein
        E (east) ida suunas on sein
        Neid saab üksteise peale panna
        nt: 3x3 map [["NW", "N", "NE"],
                     ["W", "", "E"],
                     ["SW", "S", "SE"]]

        :return: Tagastab jada rectidega mis tuleb joonistada
        """
        seinaPaksus = 1 #määrab seinapaksuse pikslites
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
        """
        Loob tühja myngukaard
        :return: tagastab kahemõõtmelise jada mille mõõtmed on kaardiKyrgus ja kaardiLaius
        kõik kohad on täidetud ""ga
        """
        kaart = []
        for i in range(self.kaardiKyrgus):
            rida = []
            for j in range(self.kaardiLaius):
                rida.append("")
            kaart.append(rida)

        return kaart

    def randomizedKruskalAlgoritm(self):
        """
        Kastuab randomised Kruskali algoritmi, et luua laburünt kaardi jaoks. See kasutab sette ja nende ühendamist
        Lõpuks lisab see need seinad kaardile
        :return: None
        """
        setid = {}
        kylastamataSeinad = []

        for i in range(self.kaardiKyrgus): #täidame kaardi seintega
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
        """
        Lisab ükskõik, mis kaardi ümber seinad.
        :return: None
        """
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
        """
        Tühjendab kaardi
        :return: None
        """
        for rida in range(len(self.kaart)):
            for veerg in range(len(self.kaart)):
                self.kaart[rida][veerg] = ""
