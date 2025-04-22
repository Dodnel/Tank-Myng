import pygame

class Kuul(pygame.sprite.Sprite):
    def __init__(self, vektorX, vektorY, x, y, kuulSuurus=(10,20), varv=(125,125,125), eluaeg=1000):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.vektorX = vektorX
        self.vektorY = vektorY
        self.vektor = pygame.math.Vector2(vektorX,vektorY)
        self.eluaeg = eluaeg
        self.suund = pygame.math.Vector2(0, 1).angle_to((vektorX, -vektorY))

        self.kuul = pygame.Surface(kuulSuurus, pygame.SRCALPHA)
        self.kuul.fill(varv)
        self.image = self.kuul
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def tagastaAsukoht(self) -> list:
        pass

    def drawKuul(self,ekraan):
        pass



    def kalkuleeriLiikumine(self, seinad) -> None:

        """if self.rect.collidelist(seinad):
            sein = self.rect.collidelist(seinad)
            print(sein)
            sein = seinad[sein]
            if sein.width > sein.height:
                self.vektorY = -self.vektorY
            if sein.width < sein.height:
                self.vektorX = -self.vektorX"""


        if self.eluaeg:
            print(self.eluaeg)
            self.x += self.vektorX
            self.y += self.vektorY

            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.image = pygame.transform.rotate(self.kuul, self.suund)
            self.eluaeg -= 1
        else:
            pygame.sprite.Sprite.kill(self)
