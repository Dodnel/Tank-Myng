import pygame
from Kaart import Kaart
from Kuul import Kuul
from Tank import Tank
from liikumine import Liikumine
import sys
import time
import copy
#s
class Myng:
    def __init__(self, mangu_muusika_voluum=0.7, sfx_voluum=0.2, kaardiLaius=12, kaardiKyrgus=6, tileSuurus=100,
                 tankideLiikumisProfiilid = None,
                 kuuliKiirus=5, voimendus1=False, voimendus2=False, voimendus3=False, heliEfektiValjusus=0.2):
        pygame.init()
        pygame.mixer.init()

        if tankideLiikumisProfiilid == None:
            self.liikumisProfiilid = [{"w": "edasi", "s": "tagasi", "a": "vasakule", "d": "paremale", "f": "tulista"},
                                      {"i": "edasi", "k": "tagasi", "j": "vasakule", "l": "paremale", "o": "tulista"}]
        else:
            self.liikumisProfiilid = tankideLiikumisProfiilid

        self.clock = pygame.time.Clock()
        self.kaart = Kaart(kaardiLaius, kaardiKyrgus, tileSuurus)
        self.tileSuurus = tileSuurus
        self.resolutsioon = self.kaart.saaResolutsioon()
        self.laiusPikslites, self.kyrgusPikslites = map(int, self.resolutsioon.split("x"))

        self.heliEfektiValjusus = heliEfektiValjusus

        self.taustaMuusika = pygame.mixer.music.load(filename="audio/Battle_Symphony.mp3")
        self.muusikaVolyym = mangu_muusika_voluum

        pygame.mixer.music.set_volume(self.muusikaVolyym)
        print(pygame.mixer.music.get_volume())
        pygame.mixer.music.play()


        self.ekraan = pygame.display.set_mode((self.laiusPikslites, self.kyrgusPikslites + 150))



        self.kuulideGrupp = pygame.sprite.Group()
        self.tankideGrupp = pygame.sprite.Group()

        self.seinad = []
        self.tankid = []
        self.liikumine = None
        self.kuulid = []
        self.skoor = [0] * len(tankideLiikumisProfiilid)

        self.font = pygame.font.SysFont(None, 48)

        ikoon = pygame.image.load("pildid/pixil-frame-0.png")
        pygame.display.set_icon(ikoon)
        pygame.display.set_caption("Tanki myng")

    def looKaart(self):
        self.kaart.lammutaKaart()
        self.kaart.randomizedKruskalAlgoritm()
        self.seinad = self.kaart.drawMap()

    def looTankid(self):
        tekkeKohad = self.kaart.leiaTankideleTekkeKohad(len(self.liikumisProfiilid))

        for i, (koht, vyrv) in enumerate(zip(tekkeKohad, ["roheline", "sinine", "punane", "kollane"])):
            uusTank = Tank(x=koht[0] * self.tileSuurus + self.tileSuurus / 2,
                           y=koht[1] * self.tileSuurus + self.tileSuurus / 2,
                            kuuliKiirus=5, vyrv=vyrv,heliEfektiValjusus=self.heliEfektiValjusus)

            uusTank.skooriIndeks = i

            self.tankid.append(uusTank)
            self.tankideGrupp.add(uusTank)

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

        yksVieendikLaiusest = self.laiusPikslites / 5



        taustaPilt = pygame.image.load("pildid/taustaPilt.jpg").convert()
        taustaPilt = pygame.transform.scale(taustaPilt, (self.laiusPikslites,self.kyrgusPikslites))

        while True:

            self.clock.tick(60)
            self.events()

            self.ekraan.fill("White")
            self.ekraan.blit(taustaPilt,(0,0))

            for sein in self.seinad:
                pygame.draw.rect(self.ekraan, "black", sein)

            for kuul in self.kuulid[:]:
                if kuul.alive():
                    kuul.kalkuleeriLiikumine(self.seinad)
                else:
                    self.kuulid.remove(kuul)

            if len(self.tankid) == 1:
                ellujyynu = self.tankid[0]
                self.skoor[ellujyynu.skooriIndeks] += 1
                self.restart()

            elif len(self.tankid) == 0:
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

            for tank in self.tankid:
                tank.joonistaSalveIndikaator(self.ekraan)

            for skoor, pilt, offset in zip(self.skoor, ["rohelineSkoor", "sinineSkoor", "punaneSkoor", "kollaneSkoor"],
                                           range(1, 5)):
                skooriPilt = pygame.image.load(f"pildid/{pilt}.png")
                skooriPilt = pygame.transform.scale(skooriPilt, (75, 75))

                xPos = yksVieendikLaiusest * offset - yksVieendikLaiusest * 0.6
                yPos = self.kyrgusPikslites + 50

                self.ekraan.blit(skooriPilt, (xPos, yPos))

                skooriTekst = self.font.render(str(skoor), True, (0, 0, 0))
                self.ekraan.blit(skooriTekst, (xPos + 100, yPos + 20))

            pygame.display.flip()


if __name__ == '__main__':
    myng = Myng(kaardiLaius=12,kaardiKyrgus=6, tileSuurus=100,tankideLiikumisProfiilid=[{"w": "edasi", "s": "tagasi", "a": "vasakule", "d": "paremale","f": "tulista"},
                           {"i": "edasi", "k": "tagasi", "j": "vasakule", "l": "paremale", "o": "tulista"}],heliEfektiValjusus=0.2)
    myng.run()
