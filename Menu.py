import tkinter as tk
import pygame
from PIL import Image, ImageTk

#s
class Menyy:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.aken = tk.Tk()
        self.aken.title("HÜPERTANKISÕDA - Tony Tuisk, Karl Priido Hoogand, Ander Konsap")
        self.akna_suurus_x, self.akna_suurus_y = 640, 360
        self.aken.geometry(f"{self.akna_suurus_x}x{self.akna_suurus_y}")
        self.aken.resizable(False, False)
        self.taustavarv = "#aa6c24"
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
        self.satete_aken = tk.Toplevel(self.aken)
        self.satete_aken.title("Sätted")
        self.satete_aken.geometry("400x300")

        tk.Label(self.satete_aken, text="Sätted", font=("Arial", 24)).pack(pady=80)


        tk.Button(self.satete_aken, text="Sulge", bg=self.nupuvarv, command=self.satete_aken.destroy, font=("Arial", 16)).pack(pady=20)

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
        tk.Label(self.aken, text="HÜPERTANKISÕDA", font=("Arial", 24)).pack(pady=80)
        tk.Button(self.aken, text="START", font=("Arial", 16), bg=self.nupuvarv, command=self.stardi_myng, pady=10, padx=20).pack(pady=10)
        tk.Button(self.aken, text="SÄTTED", font=("Arial", 16), bg=self.nupuvarv, command=self.ava_satted, pady=10, padx=20).pack(pady=10)

        self.helipilt_silt.place(relx=0.95, rely=0.95, anchor="se")

        self.helipilt_silt.bind("<Button-1>", self.lylita_heli)

    def main(self):
        self.aken.mainloop()


if __name__ == "__main__":
    menyy = Menyy()
    menyy.main()