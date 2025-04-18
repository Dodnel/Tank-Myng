"""
Tank on tõenaoliselt sprite? Maskiga? Surfaceiga?.
Igastahes collisioneid vaadates, paneme talle peale ühe nähtamatu recti, mis kohati väheneb kui palju/mis Seinu peame checkima collisioni jaoks
Kui ei pane seda recti peame kontrollima kas ta kontrollib kõik seintega mapi peal mis ei ole praktiline

"""
import pygame
from math import sin, cos,sqrt, radians
from Kuul import Kuul

#see on varastatud, ma vist teen yppimise pyhimyttel ise mingi hetk
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, vyrv):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 0
        self.original_image = pygame.Surface([w, h], pygame.SRCALPHA)
        self.original_image.fill(vyrv)

        #self.original_image = pygame.image.load("sprite/pixil-frame-0.png")

        self.image = self.original_image

        self.rectKeskpunkt = (x,y)
        self.rect = self.image.get_rect(center=self.rectKeskpunkt)
        self.mask = pygame.mask.from_surface(self.image)

    def keera(self, suund):
        if suund == 1:
            self.angle += 5
        elif suund == -1:
            self.angle -= 5
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def liigu(self, suund):
        kiirus = 5
        kraadid = self.angle % 360
        xMuutja = kiirus * sin(radians(kraadid))
        yMuutja = kiirus * cos(radians(kraadid))

        if 0 < kraadid < 90:
            pass
        elif 90 < kraadid < 180:
            pass

        self.rectKeskpunkt = (self.rectKeskpunkt[0] + xMuutja * suund, self.rectKeskpunkt[1] + yMuutja * suund)
        self.rect = self.image.get_rect(center=self.rectKeskpunkt)

    def tulista(self):
        return Kuul(10, -20, self.rectKeskpunkt[0], self.rectKeskpunkt[1])

    def joonistaTank(self):
        return ""