import pygame

class Kuul(pygame.sprite.Sprite):
    def __init__(self, suund, kiirus, x, y, kuulSuurus=(5,10), varv=(125,125,125), eluaeg=1000):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.suund = suund
        self.kiirus = kiirus
        self.eluaeg = eluaeg
        #polaar kordinaatidest vektor
        self.vektor = pygame.Vector2.from_polar((kiirus, suund))

        self.kuul = pygame.Surface(kuulSuurus, pygame.SRCALPHA)
        self.kuul.fill(varv)
        self.image = self.kuul
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


    def muudaSuund(self):
        #Jah uuendab suunaga kuuli image suunda
        self.suund = pygame.Vector2(self.vektor).angle_to(pygame.Vector2(0, 1))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image = pygame.transform.rotate(self.kuul, self.suund)

    def kustutaObject(self):
        self.kill()

    def kalkuleeriLiikumine(self, seinad) -> None:
        # Salvestame eelmise asukoha
        eel_x, eel_y = self.x, self.y

        # Arvutame uue asukoha
        uus_x = self.x + self.vektor.x
        uus_y = self.y + self.vektor.y
        uus_rect = self.rect.copy()
        uus_rect.center = (uus_x, uus_y)

        # Kontrollime kokkupõrkeid

        for sein in seinad:
            if uus_rect.colliderect(sein):
                # Leiame kokkupõrke normaali täpsemalt
                porge_normaal = pygame.Vector2(0, 0)

                # Arvutame sügavuse igas suunas seina sisse minek fix
                dx1 = uus_rect.right - sein.left
                dx2 = sein.right - uus_rect.left
                dy1 = uus_rect.bottom - sein.top
                dy2 = sein.bottom - uus_rect.top

                # Leiame minimaalse suuna seina sisse minek fix
                min_ule = min(dx1, dx2, dy1, dy2)

                if min_ule == dx1:
                    porge_normaal.x = -1  # Põrge paremalt
                elif min_ule == dx2:
                    porge_normaal.x = 1  # Põrge vasakult
                elif min_ule == dy1:
                    porge_normaal.y = -1  # Põrge alt
                elif min_ule == dy2:
                    porge_normaal.y = 1  # Põrge ülevalt

                # Normaliseerime normaali
                if porge_normaal.length() > 0:
                    porge_normaal = porge_normaal.normalize()

                    # Peegeldame kiirusvektorit normaali järgi
                    tapp_korrutis = self.vektor.dot(porge_normaal)
                    self.vektor = self.vektor - 2 * tapp_korrutis * porge_normaal

                    # Tagastame kuuli seest välja, lisades väikese offseti
                    tagasi_kaugus = min_ule + 1  # +1 et kindlasti seest välja
                    self.x = eel_x + porge_normaal.x * tagasi_kaugus
                    self.y = eel_y + porge_normaal.y * tagasi_kaugus
                    self.rect.center = (self.x, self.y)

                    # Vähendame veidi kiirust põrkel (optionaalne)
                    self.vektor *= 0.99
                    break

        # Kui kokkupõrget polnud, liigume edasi
        else:
            self.x = uus_x
            self.y = uus_y
            self.rect.center = (self.x, self.y)

        # Uuendame suunda
        self.muudaSuund()
        print(self.eluaeg)
        print(self)

        # Eluaeg
        if self.eluaeg:
            self.eluaeg -= 1
        else:
            self.kustutaObject()