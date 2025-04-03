import pygame, sys
from Kaart import Kaart

pygame.init()
screen = pygame.display.set_mode((900, 900))
kaart = Kaart()

seinad = kaart.drawMap()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill("white")
    for sein in seinad:
        pygame.draw.rect(screen,"black", sein)
    pygame.display.flip()
