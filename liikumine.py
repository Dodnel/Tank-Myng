
class Liikumine:
    def __init__(self, tankid: list, liikumisProfiilid: list):
        """
        :param tankid: tankid mis mängus on
        :param liikumisProfiilid: nende tankide liikumisprofiilid (keybindid)
        """
        self.tankid = tankid
        self.liikumisProfiilid = liikumisProfiilid
        self.tulistas =  [False] * len(tankid) #myrge et kas tulistamise nupp on all hoitud, igale tankile eraldi
        self.liikumisBlokk = []

    def teeLiigutus(self, nupuVajutused):
        """
        viib läbi tanki liigutamise, saates tanki objektile otse käske

        :param nupuVajutused: kõik nupud mis on klaviatuuri peal parajasti vajutatud selle kutsumise hetkel
        :return: tanki tulistamine tagastab kuule, neid kuule on vaja saada mängu loogikale, seega funktsioon tagastab
        lõpuks need kuulid.
        """
        kuulid = []
        for tank,liikumisProfiil,i in zip(self.tankid,self.liikumisProfiilid,range(len(self.tankid))): #
            if tank in self.liikumisBlokk: #kui tankil on keelatud käskude saamine, minnakse järgmisse tanki
                continue

            yhtsedVyyrtused = liikumisProfiil.keys() & set(nupuVajutused) #kasutab setti et leida kõik nupud, mis on esindatud liikumisprofiilides

            vyyrtused = [liikumisProfiil[vyyrtus] for vyyrtus in list(yhtsedVyyrtused)] #missugused käsud leiti

            #kui lõpuks on 1 liigub tank edasi/keerab paremale, kui -1, siis vastupidi
            liikumisSuund = 0
            keeramisSuund = 0

            if "edasi" in vyyrtused:
                liikumisSuund += 1

            if "tagasi" in vyyrtused:
                liikumisSuund -= 1

            if "vasakule" in vyyrtused:
                keeramisSuund += 1

            if "paremale" in vyyrtused:
                keeramisSuund -= 1

            if "tulista" in vyyrtused:
                if not self.tulistas[i]: #kontrollib, et nuppu all hoides ei laseks tank igal võimalusel
                    uusKuul = tank.tulista()

                    if uusKuul != None:
                        kuulid.append(uusKuul)
                    self.tulistas[i] = True #myrgib et nupp on all hetkel
            else:
                self.tulistas[i] = False #myrgib et nupp ei ole all enam

            tank.liigu(liikumisSuund)
            tank.keera(keeramisSuund)

        return kuulid

    def blokeeriLiikumist(self, tank):
        """
        Lisab liikumiblokki ühe tanki, seda kasutatakse ainult tanki plahvatus animatsiooni ajal, et see on veidikene
        üleliigne
        :param tank: tank, mille liikumist blokeeritakse
        :return: None
        """
        self.liikumisBlokk.append(tank)

    def kustutaTank(self, tank):
        """
        Kustutab tanki täiesti liikumisest, peatades kõiksuguse sisendi tanki liikumiseks.
        :param tank:
        :return:
        """
        kustutamisIndex = self.tankid.index(tank)
        del self.liikumisProfiilid[kustutamisIndex]
        del self.tankid[kustutamisIndex]
        del self.tulistas[kustutamisIndex]