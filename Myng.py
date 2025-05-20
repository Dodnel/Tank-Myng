import pygame
from Kaart import Kaart
from Kuul import Kuul
from Tank import Tank
from liikumine import Liikumine
import sys

from testMyng import laius, kyrgus


#s
class Myng:
    def __init__(self, kaardiLaius, kaardiKyrgus, tileSuurus, tankideLiikumisProfiilid):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.kaart = Kaart(kaardiLaius, kaardiKyrgus, tileSuurus)
        self.resolutsioon = self.kaart.saaResolutsioon()
        self.laius, self.kyrgus = map(int, self.resolutsioon.split("x"))
        self.ekraan = pygame.display.set_mode((laius, kyrgus))
        self.liikumisProfiilid = tankideLiikumisProfiilid
        self.seinad = []

    def looKaart(self):
        self.kaart.lammutaKaart()
        self.kaart.randomizedKruskalAlgoritm()
        seinad = self.kaart.drawMap()

        return seinad


    def looTankid(self):
        tankid = []
        tekkeKohad = self.kaart.leiaTankideleTekkeKohad(len(self.tankideLiikumine))
        for koht in tekkeKohad:
            tankid.append(Tank(koht[0], koht[1], 20, 30))

        return tankid


    def nullindaSkoor(self):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        vajutused = pygame.key.get_pressed()
        return [pygame.key.name(k) for k in range(len(vajutused)) if vajutused[k]]


    def collisionCheck(self):
        pass

    def run(self):
        self.seinad = self.looKaart()
        tankid = self.looTankid()
        liikumine = Liikumine(tankid,self.liikumisProfiilid)
        while True:
            clock.tick(60)

        pass