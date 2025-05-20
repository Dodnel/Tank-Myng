"""
Liikumisprofiili format - list, mille pikkus on sama mis tankide list,
iga element Liikumisprofiilis vastab yhele tangile, järjekord loeb:

igal tangil on vaja 5 kysku, selles järjestuses:
edasi, tagasi, vasakule, paremale, tulista

[{"w": "edasi", "s": "tagasi", "a", "vasakule", "d": "paremale",
 "f": "tulista"}
]

"""


class Liikumine:
    def __init__(self, tankid: list, liikumisProfiilid: list):
        self.tankid = tankid
        self.liikumisProfiilid = liikumisProfiilid
        self.tulistas =  [False] * len(tankid)

    def teeLiigutus(self,nupuVajutused, seinad):
        nupuVajutused = set(nupuVajutused)
        kuulid = []
        for tank,liikumisProfiil,i in zip(self.tankid,self.liikumisProfiilid,range(len(self.tankid))):
            yhtsedVyyrtused = liikumisProfiil.keys() & nupuVajutused #tuleb välja et dict_keys töötab nagu set, crazy

            vyyrtused = [liikumisProfiil[vyyrtus] for vyyrtus in list(yhtsedVyyrtused)]
            liikumisSuund = 0
            keeramisSuund = 0

            if "edasi" in vyyrtused:
                liikumisSuund += 1

            if "tagasi" in vyyrtused:
                liikumisSuund -= 1

            if "vasakule" in vyyrtused:
                keeramisSuund += 1

            if "paremale" in vyyrtused:
                keeramisSuund -= 1


            if "tulista" in vyyrtused:
                if not self.tulistas[i]:
                    kuulid.append(tank.tulista())
                    self.tulistas[i] = True
            else:
                self.tulistas[i] = False

            tank.liigu(liikumisSuund, seinad)
            tank.keera(keeramisSuund, seinad)

        return kuulid

    def kustutaTank(self, tank):
        kustutamisIndex = self.tankid.index(tank)
        del self.liikumisProfiilid[kustutamisIndex]
        del self.tankid[kustutamisIndex]
        del self.tulistas[kustutamisIndex]