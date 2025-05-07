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
        self.h = h

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
        toruVektor = pygame.Vector2.from_polar((self.h/2 + 10, -self.angle+ 90))
        kuuliPunkt = self.rectKeskpunkt + toruVektor
        print(self.angle)

        return Kuul( -self.angle + 90, 5, kuuliPunkt[0], kuuliPunkt[1], kuulSuurus=(5,10))

    def getRect(self):
        return self.rect

    def joonistaTank(self):
        return ""

    def tangiCollisionSeinadCheck(self,seinad):
        maskitavadSeinad = self.rect.collidelistall(seinad)
        print(maskitavadSeinad)
        overlapped = False
        if maskitavadSeinad:
            for sein in maskitavadSeinad:
                sein = seinad[sein]
                rect_mask = pygame.mask.Mask((sein.width, sein.height))
                rect_mask.fill()
                offset_x = sein.left - self.rect.left
                offset_y = sein.top - self.rect.top

                if self.mask.overlap(rect_mask, (offset_x, offset_y)):
                    self.original_image.fill("red")

        else:
            self.original_image.fill("green")

        # vyiks tagastada booleani
        # teeks liikumist nii et simuleerib tangi liikumist yhe frami vyrra eespool ja siis kui
        # peaks collidima siis mitte lubada.


    def tankiKuuliCollision(self, kuuliGrupp) :
        kuulidHit = pygame.sprite.spritecollide(self, kuuliGrupp, True)

        if kuulidHit:
            print("Pahhh")

            kuulidHit.clear()
