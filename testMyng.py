from winreg import KEY_WRITE

import pygame, sys
from Kaart import Kaart
from Kuul import Kuul
from pygame.locals import *
from Tank import Tank
resolutsioon = "900x500"

laius, kyrgus = map(int,resolutsioon.split("x"))

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((laius,kyrgus))

kaart = Kaart(resolutsioon=resolutsioon,tileSuurus=50)
#kuul = Kuul()
tank = Tank(50, 50, 20, 20, (128, 0, 255))

liikuvadAsjad = pygame.sprite.Group(tank)

kaart.randomizedKruskalAlgoritm()

seinad = kaart.drawMap()
print(seinad)
vajutus = 0
nuppAll = False
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_d]:
                vajutus = 1
            elif keys[pygame.K_a]:
                vajutus = -1
            else:
                pass
            nuppAll = True

        if event.type == pygame.KEYUP:
            keys = pygame.key.get_pressed()
            if not keys[pygame.K_d]:
                vajutus = 0
                nuppAll = False
            elif not keys[pygame.K_a]:
                vajutus = 0
                nuppAll = False
            else:
                pass


    if nuppAll:
        tank.keera(vajutus)

    screen.fill("white")
    for sein in seinad:
        pygame.draw.rect(screen,"black", sein)
    liikuvadAsjad.update()
    liikuvadAsjad.draw(screen)

    pygame.display.flip()
