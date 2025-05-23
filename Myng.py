import pygame
from Kaart import Kaart
from Kuul import Kuul
from Tank import Tank
from liikumine import Liikumine
import sys
import time
import copy

class Myng:
    def __init__(self, kaardiLaius, kaardiKyrgus, tileSuurus, tankideLiikumisProfiilid):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.kaart = Kaart(kaardiLaius, kaardiKyrgus, tileSuurus)
        self.resolutsioon = self.kaart.saaResolutsioon()
        self.laius, self.kyrgus = map(int, self.resolutsioon.split("x"))

        self.ekraan = pygame.display.set_mode((kaardiLaius * tileSuurus, kaardiKyrgus * tileSuurus))
        self.liikumisProfiilid = tankideLiikumisProfiilid
        self.tileSuurus = tileSuurus

        self.kuulideGrupp = pygame.sprite.Group()
        self.tankideGrupp = pygame.sprite.Group()

        self.seinad = []
        self.tankid = []
        self.liikumine = None
        self.kuulid = []

    def looKaart(self):
        self.kaart.lammutaKaart()
        self.kaart.randomizedKruskalAlgoritm()
        self.seinad = self.kaart.drawMap()

    def looTankid(self):
        tekkeKohad = self.kaart.leiaTankideleTekkeKohad(len(self.liikumisProfiilid))
        for koht in tekkeKohad:
            uusTank = Tank(
                koht[0] * self.tileSuurus + self.tileSuurus / 2,
                koht[1] * self.tileSuurus + self.tileSuurus / 2,
                20, 30, (0, 0, 255)
            )
            self.tankid.append(uusTank)
            self.tankideGrupp.add(uusTank)

    def nullindaSkoor(self):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        vajutused = pygame.key.get_pressed()
        nupud = [pygame.key.name(k) for k in range(len(vajutused)) if vajutused[k]]
        uuedKuulid = self.liikumine.teeLiigutus(nupud, self.seinad)
        for kuul in uuedKuulid:
            self.kuulid.append(kuul)
            self.kuulideGrupp.add(kuul)

    def collisionCheck(self):
        pass

    def restart(self):
        self.tankid = []
        self.kuulid = []
        self.kuulideGrupp = pygame.sprite.Group()
        self.tankideGrupp = pygame.sprite.Group()
        self.looKaart()
        self.looTankid()
        self.liikumine = Liikumine(self.tankid, copy.deepcopy(self.liikumisProfiilid))

    def run(self):
        self.restart()

        while True:
            self.clock.tick(60)
            self.events()

            self.ekraan.fill("white")
            for sein in self.seinad:
                pygame.draw.rect(self.ekraan, "black", sein)

            for kuul in self.kuulid[:]:
                if kuul.alive():
                    kuul.kalkuleeriLiikumine(self.seinad)
                else:
                    self.kuulid.remove(kuul)

            # ↪ Kui ainult 1 tank jääb järele, restartime
            if len(self.tankid) <= 1:
                self.restart()


            # Kuulid joonistame sprite-grupiga
            self.kuulideGrupp.draw(self.ekraan)
            self.tankideGrupp.draw(self.ekraan)

            for tank in self.tankid[:]:
                tank.uuendaSalv()

                if tank.alive():
                    tank.tangiCollisionSeinadCheck(self.seinad)
                    if tank.tankiKuuliCollision(self.kuulideGrupp):
                        if not tank.plahvatus_aktiivne:
                            self.liikumine.blokeeriLiikumist(tank)
                            tank.alustaPlahvatus()

                if tank.plahvatus_valmis:
                    tank.kill()
                    self.liikumine.kustutaTank(tank)

                tank.joonistaPauk(self.ekraan)

            # Salve indikaatorid
            for tank in self.tankid:
                tank.joonistaSalveIndikaator(self.ekraan)

            pygame.display.flip()


if __name__ == '__main__':
    myng = Myng(
        12, 6, 100,
        [
            {"w": "edasi", "s": "tagasi", "a": "vasakule", "d": "paremale", "f": "tulista"},
            {"i": "edasi", "k": "tagasi", "j": "vasakule", "l": "paremale", "o": "tulista"}
        ]
    )
    myng.run()
