import pygame, sys
from Kaart import Kaart
from Kuul import Kuul

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
kaart = Kaart(resolutsioon="800x300")
#kuul = Kuul()


kaart.lisaSeinad()
kaart.kaart[3][3] = "NSWE"
kaart.kaart[3][4] = "N"

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
