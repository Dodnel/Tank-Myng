"""
Tank on tõenaoliselt sprite? Maskiga? Surfaceiga?.
Igastahes collisioneid vaadates, paneme talle peale ühe nähtamatu recti, mis kohati väheneb kui palju/mis Seinu peame checkima collisioni jaoks
Kui ei pane seda recti peame kontrollima kas ta kontrollib kõik seintega mapi peal mis ei ole praktiline
"""
import pygame
from math import sin, cos,sqrt, radians, dist
from Kuul import Kuul
from PIL import Image

#see on varastatud, ma vist teen yppimise pyhimyttel ise mingi hetk
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, vyrv, seinad: list, kuuliKiirus=5, heliEfektiValjusus: float=0.2, voimendus1: bool=False, voimendus2: bool=False, voimendus3: bool=False):
        pygame.sprite.Sprite.__init__(self)

        vyrvid = ["sinine", "roheline", "punane", "kollane"]
        if vyrv in vyrvid:
            vyrv = f"Sprites/{vyrv}.png"
        else:
            vyrv = "Sprites/default.png"

        self.original_image = pygame.image.load(vyrv)
        self.image = self.original_image
        self.rectKeskpunkt = (x,y)
        self.rect = self.image.get_rect(center=self.rectKeskpunkt)
        self.mask = pygame.mask.from_surface(self.image)
        self.h = self.image.get_height()
        self.angle = 0

        self.kuuliKiirus = kuuliKiirus
        self.kiirus = 5
        self.seinad = seinad

        self.salve_maht = 1
        self.salv = self.salve_maht
        self.laadib = False
        self.laadimise_algus = None
        self.laadimise_kestus = 2000

        self.voimendus1 = voimendus1
        self.voimendus2 = voimendus2
        self.voimendus3 = voimendus3

        self.tulistamisHeli = pygame.mixer.Sound("audio/tulistamine.mp3")
        self.plahvatusHeli = pygame.mixer.Sound("audio/plahvatus.mp3")
        self.tulistamisHeli.set_volume(heliEfektiValjusus)
        self.plahvatusHeli.set_volume(heliEfektiValjusus)

        self.plahvatus_kaadrid = []
        self.plahvatus_aktiivne = False
        self.plahvatus_frame_index = 0
        self.plahvatus_timer = 0
        self.plahvatus_valmis = False

        # Lae kaadrid .gif-failist
        gif_path = "gif/tankiPauk.gif"
        gif = Image.open(gif_path)
        try:

            while True:
                frame = gif.copy().convert("RGBA")
                pygame_kaader = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                self.plahvatus_kaadrid.append(pygame.transform.scale(pygame_kaader, (50, 50)))
                gif.seek(gif.tell() + 1)

        except EOFError:
            pass


    def keera(self, suund):
        """
        Keerab tanki spritei kindlat arv kraade.
        :param suund: mis suunas tank peaks keerama, 1 - paremale, -1 - vasakule
        :return: None
        """
        if suund == 0:
            return

        angleRevert = self.angle
        if suund == 1:
            self.angle += 5
        elif suund == -1:
            self.angle -= 5
        imageRevert = self.image
        rectRevert = self.rect
        maskRevert = self.mask

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

        if self.tangiCollisionSeinadCheck():
            self.image = imageRevert
            self.rect = rectRevert
            self.mask = maskRevert
            self.angle = angleRevert

    def liigu(self, suund):
        """
        Liigutab tanki spriti edasi või tagasi kindlal kiirusel
        :param suund: mis suunas tank liigub, kas edasi või tagasi. Märgitud 1ga (edasi) ja -1 (tagasi)
        :return:
        """
        if suund == 0:
            return
        kraadid = self.angle % 360
        xMuutja = self.kiirus * sin(radians(kraadid))
        yMuutja = self.kiirus * cos(radians(kraadid))

        if 0 < kraadid < 90:
            pass
        elif 90 < kraadid < 180:
            pass

        rectKeskpunktRevert = self.rectKeskpunkt
        rectRevert = self.rect

        self.rectKeskpunkt = (self.rectKeskpunkt[0] + xMuutja * suund, self.rectKeskpunkt[1] + yMuutja * suund)
        self.rect = self.image.get_rect(center=self.rectKeskpunkt)

        if self.tangiCollisionSeinadCheck():
            self.rectKeskpunkt = rectKeskpunktRevert
            self.rect = rectRevert

    def tulista(self):
        """
        Loob kuuli tanki suunaga ja kiirusega arvestades
        :return: tagastab Kuuli objekti juhul kui tal on salves kuule, teisel juhul mitte midagi
        """
        if self.laadib:
            return None

        if self.salv > 0:
            self.salv -= 1
            if self.salv == 0:
                self.laadib = True
                self.laadimise_algus = pygame.time.get_ticks()
            toruVektor = pygame.Vector2.from_polar((self.h / 2 + 9, -self.angle + 90))
            kuuliPunkt = self.rectKeskpunkt + toruVektor

            self.tulistamisHeli.play()

            return Kuul(suund=-self.angle + 90, kiirus=self.kuuliKiirus, x=kuuliPunkt[0], y=kuuliPunkt[1],
                        powerupCosinus=self.voimendus3, powerupKiirus=self.voimendus1, powerupSuurus=self.voimendus2, powerupLaser=self.voimendus3)
        return None

    def uuendaSalv(self):
        """
        Laeb tanki salve ära jälle kui on mõõdunud aeg, mis kulub tanki laadimisele
        :return: None
        """
        if self.laadib:
            aeg = pygame.time.get_ticks()
            if aeg - self.laadimise_algus >= self.laadimise_kestus:
                self.salv = self.salve_maht
                self.laadib = False

    def tangiCollisionSeinadCheck(self):
        """
        Võtab kõik seinad mängus ja siis vaatab kas ta collidib ühe nendega, kui collidib loob sellest seinast maski
        ja võrdleb seda maski enda maskiga et aru saada kas nad collidavad. Nii on tehtud sest maskide collisionid
        on päris kallid ajaliselt.
        :return: tagastab tõeväärtuse sõltuvalt sellest, et kas tank on lõikanud enda lähedal olevat seina
        """
        maskitavadSeinad = self.rect.collidelistall(self.seinad)
        if maskitavadSeinad:
            for sein in maskitavadSeinad:
                sein = self.seinad[sein]
                rectMask = pygame.mask.Mask((sein.width, sein.height))
                rectMask.fill()
                offsetX = sein.left - self.rect.left
                offsetY = sein.top - self.rect.top

                if self.mask.overlap(rectMask, (offsetX, offsetY)):
                    return True
        return False


    def tankiKuuliCollision(self, kuuliGrupp):
        """
        vaatab kas tank collidib ühegi kuuliga, mis mängus on peal
        :param kuuliGrupp: Kuulide sprite group
        :return: tagastab tõeväärtuse sõltuvalt sellest, et kas collidib
        """
        hit = []
        for i in kuuliGrupp:
            if pygame.sprite.collide_mask(self,i):
                i.kill()
                self.plahvatusHeli.play()
                return True
        return False

    def joonistaSalveIndikaator(self):
        """
        Joonistab väikse kastikese tanki ette, mis kuvab mängijale, et kas tal on võimalik tulistada
        :return: tagastab recti ja selle vyrvi
        """
        toruVektor = pygame.Vector2.from_polar((self.h / 2 + 9, -self.angle + 90))
        indikaatori_pos = self.rectKeskpunkt + toruVektor

        varv = (0, 255, 0) if self.salv > 0 else (255, 0, 0)  # roheline kui on kuule, muidu punane

        return pygame.Rect(indikaatori_pos[0] - 4, indikaatori_pos[1] - 4, 8, 8), varv


    def alustaPlahvatus(self):
        """
        Alustab tanki plahvatuse gifi kuvamist
        :return: None
        """
        self.plahvatus_aktiivne = True
        self.plahvatus_frame_index = 0
        self.plahvatus_timer = pygame.time.get_ticks()

    def joonistaPauk(self, ekraan):
        """
        joonistab plahvatuse kaadreid
        :param ekraan: ekraan kuhu need kaadrid joonistatake
        :return: None
        """
        if self.plahvatus_aktiivne:
            aeg = pygame.time.get_ticks()
            if aeg - self.plahvatus_timer > 50:
                self.plahvatus_timer = aeg
                self.plahvatus_frame_index += 1

            if self.plahvatus_frame_index < len(self.plahvatus_kaadrid):
                kaader = self.plahvatus_kaadrid[self.plahvatus_frame_index]
                rect = kaader.get_rect(center=self.rect.center)
                ekraan.blit(kaader, rect)
            else:
                self.plahvatus_aktiivne = False
                self.plahvatus_valmis = True