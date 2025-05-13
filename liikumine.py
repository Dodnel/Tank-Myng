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

    def teeLiigutus(self,nupuVajutused, seinad):
        for tank,liikumisProfiil in zip(self.tankid,self.liikumisProfiilid):
            liikumisProfiiliNupud = liikumisProfiil.keys()
            yhtsedVyyrtused = set(liikumisProfiiliNupud) & set(nupuVajutused)

            if yhtsedVyyrtused:
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
                    tank.tulista()

                tank.liigu(liikumisSuund, seinad)
                tank.keera(keeramisSuund, seinad)
