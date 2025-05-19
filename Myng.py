import pygame
import Kaart,Menu,Kuul,Tank,liikumine
import sys
#s
class Myng:
    def __init__(self,resolutsioon, tileSuurus, tankideLiikumisProfiilid):
        pygame.init()
        self.ekraan = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.seinad = []
        self.kaart = Kaart.Kaart(resolutsioon, tileSuurus)
        self.tankideLiikumine = tankideLiikumisProfiilid


    def looKaart(self):
        self.kaart.lammutaKaart()
        self.kaart.randomizedKruskalAlgoritm()
        self.seinad = self.kaart.drawMap()
        pass

    def looTankid(self):
        tekkeKohad = self.kaart.leiaTankideleTekkeKohad(len(self.tankideLiikumine))

        pass


    def nullindaSkoor(self):
        pass




    def events(self):
        pass

    def collisionCheck(self):
        pass

    def run(self):
        nullindaSkoor()
        looKaart()
        looTankid()

        pass