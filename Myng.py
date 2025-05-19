import pygame
import Kaart,Menu,Kuul,Tank,liikumine
#s
class Myng:
    def __init__(self): 
        pygame.init()
        self.ekraan = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.kaart = Kaart
        self.tankid = []
        self.kuulid = []

        self.tankidGrupp = pygame.sprite.Group()
        self.kuulidGrupp = pygame.sprite.Group()



        self.active = False

    def events(self):
        for event in pygame.event.get():
            pass

    def collisionCheck(self):
        pass

    def run(self):
        while True:
            self.clock.tick(60)
            if not self.active:
                self.kaart.drawMap(self.ekraan)
                self.tank1.drawTank(self.ekraan)
                self.tank2.drawTank(self.ekraan)
                for kuul in self.kuulid:
                    kuul.drawKuul(self.ekraan)
                self.collisionCheck()
