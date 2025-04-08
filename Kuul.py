

class Kuul:
    def __init__(self, vektor, koordinaadid, varv=(125,125,125), eluaeg=1000):
        self.koordinaadid = koordinaadid
        self.vektor = vektor
        self.eluaeg = eluaeg
        self.varv = varv
        #see pole siin

    def tagastaAsukoht(self) -> list:
        return self.koordinaadid

    def drawKuul(self,ekraan):
        pass

    def kalkuleeriLiikumine(self) -> None:
        pass

