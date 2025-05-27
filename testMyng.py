

import pygame, sys
from Kaart import Kaart

from Tank import Tank
from liikumine import Liikumine

#siin on uus kaardi süsteem
kaart = Kaart(kaardiLaius=16, kaardiKyrgus=2 ,tileSuurus=100)

resolutsioon = kaart.saaResolutsioon()

laius, kyrgus = map(int,resolutsioon.split("x"))

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((laius,kyrgus))
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

tankid = [tank,tank2]

liikumine = Liikumine(tankid, [{"w": "edasi", "s": "tagasi", "a": "vasakule", "d": "paremale","f": "tulista"}, {"f": "edasi", "v": "tagasi", "c": "vasakule", "b": "paremale", "o": "tulista"}])

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
            tank.tangiCollisionSeinadCheck(seinad)
            if tank.tankiKuuliCollision(kuulidGrupp):
                tank.kill()
                liikumine.kustutaTank(tank)


    tankidGrupp.draw(screen)
    kuulidGrupp.draw(screen)



    pygame.display.flip()
