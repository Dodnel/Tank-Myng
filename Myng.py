import pygame

class Myng:
    def __init__(self):
        pygame.init()
        self.ekraan = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        pass

    def events(self):
        for event in pygame.event.get():
            pass


    def run(self):
        while True:
            self.clock.tick(60)