import pygame, sys
from Kaart import Kaart

pygame.init()
screen = pygame.display.set_mode((500, 500))
kaart = Kaart(resolutsioon="500x500")
kaart.lisaSeinad()
kaart.kaart[3][3] = ""

seinad = kaart.drawMap()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill("white")
    for sein in seinad:
        pygame.draw.rect(screen,"black", sein)
    pygame.display.flip()
