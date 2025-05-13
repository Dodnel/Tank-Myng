from winreg import KEY_WRITE

import pygame, sys
from Kaart import Kaart
from Kuul import Kuul
from pygame.locals import *
from Tank import Tank
from liikumine import Liikumine
resolutsioon = "900x500"

laius, kyrgus = map(int,resolutsioon.split("x"))

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((laius,kyrgus))

kaart = Kaart(resolutsioon=resolutsioon,tileSuurus=150)
#kuul = Kuul()
tank = Tank(25, 25, 20, 30, (128, 0, 255))

tank2 = Tank(25, 25, 20, 30, (0, 0, 255))

tank3 = Tank(25, 25, 20, 30, (128, 0, 0))

tank4 = Tank(25, 25, 20, 30, (0, 255, 0))

#tankid = [tank,tank2,tank3,tank4]
#
#liikumine = Liikumine(tankid,[{"w": "edasi", "s": "tagasi", "a": "vasakule", "d": "paremale","f": "tulista"},
#                                            {"f": "edasi", "v": "tagasi", "c": "vasakule", "b": "paremale", "o": "tulista"},
#                                            {"y": "edasi", "h": "tagasi", "g": "vasakule", "j": "paremale", "u": "tulista"},
#                                            {"k": "edasi", ",": "tagasi", "m": "vasakule", ".": "paremale", "2": "tulista"}])

tankid = [tank]

liikumine = Liikumine(tankid, [{"w": "edasi", "s": "tagasi", "a": "vasakule", "d": "paremale","f": "tulista"}])

kuulid = []


tankidGrupp = pygame.sprite.Group()

for tankA in tankid:
    tankidGrupp.add(tankA)

kuulidGrupp = pygame.sprite.Group()

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
    keys = pygame.key.get_pressed()
    nupuVajutused = [pygame.key.name(k) for k in range(len(keys)) if keys[k]]
    uuedKuulid = liikumine.teeLiigutus(nupuVajutused, seinad)

    for kuul in uuedKuulid:
        kuulidGrupp.add(kuul)
        kuulid.append(kuul)
    screen.fill("white")

    for sein in seinad:
        pygame.draw.rect(screen,"black", sein)

    for kuul in kuulid[:]:
        if kuul.alive():
            kuul.kalkuleeriLiikumine(seinad)
        else:
            kuulid.remove(kuul)

    for tank in tankid[:]:
        if tank.alive():
            tank.tankiKuuliCollision(kuulidGrupp)
            tank.tangiCollisionSeinadCheck(seinad)
        else:
            tankid.remove(tank)



    tankidGrupp.draw(screen)
    kuulidGrupp.draw(screen)


    pygame.display.flip()
