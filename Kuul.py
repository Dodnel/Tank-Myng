import pygame, math

class Kuul(pygame.sprite.Sprite):
    def __init__(self, suund, kiirus: int, x, y, tileSuurus, powerupSuurus = False, powerupKiirus = False, powerupCosinus = False):
        pygame.sprite.Sprite.__init__(self)

        # Kuuli x ja y kordinaat
        self.x = x
        self.y = y

        # Suund kuuli vektorile
        self.suund = suund

        # Kuuli eluaeg
        self.eluaeg = 500
        self.aeg = self.eluaeg

        # Kuuli liikumise vektor
        self.suunaVektor = pygame.Vector2()

        # Et hiljem liikumises testida kas see on True
        self.powerupCosinus = powerupCosinus

        # 2 kordistab suuruse kui võimendi on True
        if powerupSuurus:
            # polaar kordinaatidest otseLiikumiseVektor
            self.kuul = pygame.Surface((10,20), pygame.SRCALPHA)
        else:
            self.kuul = pygame.Surface((5, 10), pygame.SRCALPHA)

        # 2 kordistab kiiruse kui võimendi on True
        if powerupKiirus:
            self.otseLiikumiseVektor = pygame.Vector2.from_polar((2 * (kiirus * (tileSuurus / 100)), suund))
        else:
            self.otseLiikumiseVektor = pygame.Vector2.from_polar((kiirus * (tileSuurus / 100), suund))

        # Kuuli halliks tegemine
        self.kuul.fill((125,125,125))

        # Kuuli recti ja maski loomine

        self.kuul = pygame.transform.scale(self.kuul, (
            self.kuul.get_width() * tileSuurus / 100,
            self.kuul.get_height() * tileSuurus / 100))

        self.image = self.kuul
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


    def muudaSuund(self):
        #Jah uuendab suunaga kuuli image suunda
        self.suund = pygame.Vector2(self.suunaVektor).angle_to(pygame.Vector2(0, 1))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image = pygame.transform.rotate(self.kuul, self.suund)

    def kustutaObject(self):
        """
        Kustutab kuuli ära
        :return: None
        """
        self.kill()

    def kalkuleeriLiikumine(self, seinad):
        """

        :param seinad:
        :return:
        """
        # Salvestame eelmise asukoha
        eel_x, eel_y = self.x, self.y

        if self.powerupCosinus:
            # Arvutame uue asukoha (sinusoidne liikumine)
            cos_offset = math.cos((self.aeg-self.eluaeg)*math.pi/10) * 5

            cosVector = pygame.Vector2(-self.otseLiikumiseVektor.y, self.otseLiikumiseVektor.x).normalize() * cos_offset

            # Kuuli asukohale tanki liikumisvektori ja cos Liikumisvektori
            uus_x = self.x + self.otseLiikumiseVektor.x + cosVector.x
            uus_y = self.y + self.otseLiikumiseVektor.y + cosVector.y

            # Kuuli suunavektori salvestamine
            self.suunaVektor = pygame.Vector2(self.otseLiikumiseVektor.x + cosVector.x, self.otseLiikumiseVektor.y + cosVector.y)

            # Kuuli recti asukoha muutmine
            uus_rect = self.rect.copy()
            uus_rect.center = (uus_x, uus_y)
        else:
            # Arvutame uue asukoha (tavaline liikumine)
            uus_x = self.x + self.otseLiikumiseVektor.x
            uus_y = self.y + self.otseLiikumiseVektor.y

            # Kuuli suunavektori salvestamine
            self.suunaVektor = self.otseLiikumiseVektor

            # Kuuli recti asukoha muutmine
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
                    tapp_korrutis = self.otseLiikumiseVektor.dot(porge_normaal)
                    self.otseLiikumiseVektor = self.otseLiikumiseVektor - 2 * tapp_korrutis * porge_normaal

                    # Tagastame kuuli seest välja, lisades väikese offseti
                    tagasi_kaugus = min_ule + 1  # +1 et kindlasti seest välja
                    self.x = eel_x + porge_normaal.x * tagasi_kaugus
                    self.y = eel_y + porge_normaal.y * tagasi_kaugus
                    self.rect.center = (self.x, self.y)

                    # Vähendame veidi kiirust põrkel (optionaalne)
                    self.otseLiikumiseVektor *= 0.99
                    break

        # Kui kokkupõrget polnud, liigume edasi
        else:
            self.x = uus_x
            self.y = uus_y
            self.rect.center = (self.x, self.y)

        # Uuendame suunda
        self.muudaSuund()

        # Eluaeg
        if self.eluaeg:
            self.eluaeg -= 1
        else:
            self.kustutaObject()