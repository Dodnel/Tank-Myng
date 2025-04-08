

class Kuul:
    def __init__(self, vektor, koordinaadid, eluaeg=1000):
        self.koordinaadid = koordinaadid
        self.vektor = vektor
        self.eluaeg = eluaeg

    def tagastaAsukoht(self) -> list:
        return self.koordinaadid

    def drawKuul(self,ekraan):
        pass

    def kalkuleeriLiikumine(self) -> None:
        pass

