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
tank = Tank(100, 50, 20, 30, (128, 0, 255))


kuul = Kuul(40,10,315,317, (5,10))

kuulid = [kuul]


tankidGrupp = pygame.sprite.Group(tank)

kuulidGrupp = pygame.sprite.Group(kuul)

kaart.randomizedKruskalAlgoritm()

seinad = kaart.drawMap()

vajutus = 0
vajutus2 = 0
nuppAll = False
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                vajutus = 1
            elif keys[pygame.K_d]:
                vajutus = -1

            if keys[pygame.K_w]:
                vajutus2 = 1
            elif keys[pygame.K_s]:
                vajutus2 = -1
            else:
                pass
            nuppAll = True

            if keys[pygame.K_f]:
                uusKuul = tank.tulista()
                kuulid.append(uusKuul)
                kuulidGrupp.add(uusKuul)

        if event.type == pygame.KEYUP:
            keys = pygame.key.get_pressed()
            if not keys[pygame.K_a]:
                vajutus = 0
                nuppAll = False
            elif not keys[pygame.K_d]:
                vajutus = 0
                nuppAll = False
            else:
                pass

            if not keys[pygame.K_w]:
                vajutus2 = 0
                nuppAll = False
            elif not keys[pygame.K_s]:
                vajutus2 = 0
                nuppAll = False



    if nuppAll:
        tank.keera(vajutus)
    tank.liigu(vajutus2)
    screen.fill("white")

    for sein in seinad:
        pygame.draw.rect(screen,"black", sein)

    for kuul in kuulid:
        kuul.kalkuleeriLiikumine(seinad)

    tank.tankiKuuliCollision(kuulidGrupp)
    tank.tangiCollisionSeinadCheck(seinad)

    tankidGrupp.draw(screen)
    kuulidGrupp.draw(screen)


    pygame.display.flip()
