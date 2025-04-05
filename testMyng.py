import pygame, sys
from Kaart import Kaart
from Kuul import Kuul

resolutsioon = "900x500"

laius, kyrgus = map(int,resolutsioon.split("x"))

pygame.init()

screen = pygame.display.set_mode((laius,kyrgus))

kaart = Kaart(resolutsioon=resolutsioon,tileSuurus=50)
#kuul = Kuul()


kaart.randomizedKruskalAlgoritm()

seinad = kaart.drawMap()
print(seinad)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill("white")
    for sein in seinad:
        pygame.draw.rect(screen,"black", sein)
    pygame.display.flip()
