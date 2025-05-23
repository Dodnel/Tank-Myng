import tkinter as tk
import pygame
from PIL import Image, ImageTk


class Menyy:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.seaded = []

        self.aken = tk.Tk()
        self.aken.title("HÜPERTANKISÕDA - Tony Tuisk, Karl Priido Hoogand, Ander Konsap")
        self.akna_suurus_x, self.akna_suurus_y = 640, 360
        self.aken.geometry(f"{self.akna_suurus_x}x{self.akna_suurus_y}")
        self.aken.resizable(False, False)
        self.taustavarv = "#d18d3e"
        self.nupuvarv = "#d18d3e"
        self.aken.configure(background=self.taustavarv)

        self.taustapilt = Image.open(r"sprite\taustapilt.png")
        self.taustapilt = self.taustapilt.resize((self.akna_suurus_x, self.akna_suurus_y), Image.Resampling.LANCZOS)
        self.taustapilt_pilt = ImageTk.PhotoImage(self.taustapilt)
        self.tausta_silt = tk.Label(self.aken, image=self.taustapilt_pilt)
        self.tausta_silt.place(x=0, y=0, relwidth=1, relheight=1)

        self.heli_mangib = True
        self.helipilt_on = Image.open(r"sprite\heli_on.png").resize((50, 50))
        self.helipilt_off = Image.open(r"sprite\heli_off.png").resize((50, 50))
        self.helipilt = ImageTk.PhotoImage(self.helipilt_on)
        self.helipilt_silt = tk.Label(self.aken, image=self.helipilt, bg=self.taustavarv, bd=0, cursor="hand2")

        self.stardi_heli()
        self.loo_vidinad()

    def stardi_myng(self):
        # Mäng käivitatakse pygame-iga
        self.aken.destroy()

    def ava_satted(self):
        if hasattr(self, 'satete_aken') and self.satete_aken.winfo_exists():
            self.satete_aken.lift()
            return

        self.satete_aken = tk.Toplevel(self.aken)
        self.satete_aken.title("Sätted")
        self.satete_aken.geometry("400x400")
        self.satete_aken.resizable(False, False)

        def sulge_satted():
            self.satete_aken.destroy()
            self.satete_aken = None

        self.satete_aken.protocol("WM_DELETE_WINDOW", sulge_satted)

        raam = tk.Frame(self.satete_aken)
        raam.pack(fill="both", expand=True)

        tahvel = tk.Canvas(raam, highlightthickness=0)
        tahvel.pack(side="left", fill="both", expand=True)

        kerimisriba = tk.Scrollbar(raam, orient="vertical", command=tahvel.yview)
        kerimisriba.pack(side="right", fill="y")

        tahvel.configure(yscrollcommand=kerimisriba.set)

        sisu_raam = tk.Frame(tahvel)
        sisu_aken_id = tahvel.create_window((0, 0), window=sisu_raam, anchor="n")

        def uuenda_scrolli_suurus(sündmus):
            tahvel.configure(scrollregion=tahvel.bbox("all"))
            tahvel.itemconfig(sisu_aken_id, width=sündmus.width)

        sisu_raam.bind("<Configure>", uuenda_scrolli_suurus)
        tahvel.bind("<Configure>", uuenda_scrolli_suurus)

        # Kerimine hiirerulliga
        def kerimine(event):
            tahvel.yview_scroll(int(-1 * (event.delta / 120)), "units")

        tahvel.bind_all("<MouseWheel>", kerimine)
        tahvel.bind_all("<Button-4>", lambda e: tahvel.yview_scroll(-1, "units"))
        tahvel.bind_all("<Button-5>", lambda e: tahvel.yview_scroll(1, "units"))

        tk.Label(sisu_raam, text="Sätted", font=("Arial", 24)).pack(pady=10)

        def lisa_slaider(vanem, nimi, min_v, max_v, muutuja):
            raam = tk.Frame(vanem)
            raam.pack(pady=5)
            tk.Label(raam, text=nimi, width=20, anchor="w").pack(side="left")
            tk.Scale(raam, from_=min_v, to=max_v, orient="horizontal", variable=muutuja).pack(side="right")

        def lisa_tekstisisestus(vanem, nimi, muutuja):
            raam = tk.Frame(vanem)
            raam.pack(pady=5, fill="x", padx=10)
            tk.Label(raam, text=nimi, anchor="w").pack(side="left")
            sisestus = tk.Entry(raam, textvariable=muutuja, font=("Ariel", 12), width=15)
            sisestus.pack(side="right", padx=5)

        # Muutujad
        # tile suurus default 100
        # kaardi laius 12, kõrgus 6


        self.ruuduSuurus = tk.IntVar(value=100)
        self.kuuli_elu = tk.IntVar(value=5)
        self.kuuli_kiirus = tk.IntVar(value=10)
        self.kuuli_suurus = tk.IntVar(value=5)
        self.tangi_kiirus = tk.IntVar(value=3)

        lisa_tekstisisestus(sisu_raam, "Ruudu suurus", self.ruuduSuurus)
        lisa_slaider(sisu_raam, "Kuuli eluaeg (sek)", 1, 10, self.kuuli_elu)
        lisa_slaider(sisu_raam, "Kuuli kiirus", 1, 20, self.kuuli_kiirus)
        lisa_slaider(sisu_raam, "Kuuli suurus", 1, 10, self.kuuli_suurus)
        lisa_slaider(sisu_raam, "Tanki kiirus", 1, 10, self.tangi_kiirus)

        # Powerupid
        tk.Label(sisu_raam, text="Powerupid", font=("Arial", 16)).pack(pady=10)

        tk.Checkbutton(sisu_raam, text="Powerup 1", variable=self.powerup1).pack()
        tk.Checkbutton(sisu_raam, text="Powerup 2", variable=self.powerup2).pack()
        tk.Checkbutton(sisu_raam, text="Powerup 3", variable=self.powerup3).pack()

        tk.Button(sisu_raam, text="Sulge", bg=self.nupuvarv, command=self.satete_aken.destroy, font=("Arial", 16)).pack(pady=20)

    def stardi_heli(self):
        pygame.mixer.music.load(r"audio\Tanki_mangu_peamenyy_laul_copyrighted_trust.mp3")
        pygame.mixer.music.play(-1)

    def lylita_heli(self, syndmus):
        if self.heli_mangib:
            pygame.mixer.music.set_volume(0)
            self.helipilt = ImageTk.PhotoImage(self.helipilt_off)
            self.heli_mangib = False
        else:
            pygame.mixer.music.set_volume(1.0)
            self.helipilt = ImageTk.PhotoImage(self.helipilt_on)
            self.heli_mangib = True

        self.helipilt_silt.config(image=self.helipilt)

    def loo_vidinad(self):
        tk.Label(self.aken, text="HÜPERTANKISÕDA", font=("Arial", 24), bg=self.taustavarv).place(y=7, x=320)
        tk.Button(self.aken, text="START", font=("Arial", 16), bg=self.nupuvarv, command=self.stardi_myng, padx=60).place(x=30, y=150)
        tk.Button(self.aken, text="SÄTTED", font=("Arial", 16), bg=self.nupuvarv, command=self.ava_satted, padx=53).place(x=30, y=200)

        self.helipilt_silt.place(relx=0.95, rely=0.95, anchor="se")

        self.helipilt_silt.bind("<Button-1>", self.lylita_heli)

    def main(self):
        self.aken.mainloop()


if __name__ == "__main__":
    menyy = Menyy()
    menyy.main()