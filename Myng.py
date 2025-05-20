import pygame
from Kaart import Kaart
from Kuul import Kuul
from Tank import Tank
from liikumine import Liikumine
import sys
#s
class Myng:
    def __init__(self,resolutsioon, tileSuurus, tankideLiikumisProfiilid):
        pygame.init()
        self.ekraan = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.kaart = Kaart(resolutsioon, tileSuurus)
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
            uusTank = Tank(koht[0] + self.tileSuurus / 2, koht[1]+ self.tileSuurus / 2, 20, 30, (0, 0, 255))
            self.tankid.append(uusTank)
            self.tankideGrupp.add(uusTank)


    def nullindaSkoor(self):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        vajutused = pygame.key.get_pressed()
        uuedKuulid = self.liikumine.teeLiigutus([pygame.key.name(k) for k in range(len(vajutused)) if vajutused[k]], self.seinad)
        for kuul in uuedKuulid:
            self.kuulid.append(kuul)
            self.kuulideGrupp.add(kuul)

    def collisionCheck(self):
        pass

    def run(self):
        self.looKaart()
        self.looTankid()
        self.liikumine = Liikumine(self.tankid, self.liikumisProfiilid)
        self.kuulid = []

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

            for tank in self.tankid[:]:
                if tank.alive():
                    tank.tangiCollisionSeinadCheck(self.seinad)
                    if tank.tankiKuuliCollision(self.kuulideGrupp):
                        tank.kill()
                        self.liikumine.kustutaTank(tank)

            self.tankideGrupp.draw(self.ekraan)
            self.kuulideGrupp.draw(self.ekraan)

            pygame.display.flip()

if __name__ == '__main__':
    myng = Myng("500x500",50, [{"w": "edasi", "s": "tagasi", "a": "vasakule", "d": "paremale","f": "tulista"}])
    myng.run()