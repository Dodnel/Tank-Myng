import tkinter as tk
import pygame


class Menyy:
    def __init__(self):
        self.aken = tk.Tk()
        self.aken.title("Tanki mäng - Tony Tuisk, Karl Priido Hoogand, Ander Konsap")
        self.aken.geometry("500x500")
        self.loo_vidinad()

        self.heli_mangib = True
        self.helipilt_on = "heli_on.png"
        self.helipilt_off = "heli_off.png"

    def stardi_myng(self):
        # Mäng käivitatakse pygame-iga
        self.aken.destroy()

    def ava_satted(self):
        self.satete_aken = tk.Toplevel(self.aken)
        self.satete_aken.title("Sätted")
        self.satete_aken.geometry("400x300")

        tk.Label(self.satete_aken, text="Sätted", font=("Arial", 24)).pack(pady=80)


        tk.Button(self.satete_aken, text="Sulge", command=self.satete_aken.destroy, font=("Arial", 16)).pack(pady=20)


    def lylita_heli(self):
        if self.heli:
            pygame.mixer_music.stop()
            self.helipilt = tk.PhotoImage(file=self.helipilt_off)
            self.heli = False
        else:
            pygame.mixer_music.play(-1)
            self.helipilt = tk.PhotoImage(file=self.helipilt_on)
            self.heli_on = True

        self.helipilt_silt.config(image=self.helipilt)
        pass


    def loo_vidinad(self):
        tk.Label(self.aken, text="Faking tanki mäng mida??", font=("Arial", 24)).pack(pady=80)
        tk.Button(self.aken, text="START", font=("Arial", 16), command=self.stardi_myng, pady=10, padx=20).pack(pady=10)
        tk.Button(self.aken, text="SÄTTED", font=("Arial", 16), command=self.ava_satted, pady=10, padx=20).pack(pady=10)

        self.helipilt = tk.PhotoImage(file=self.helipilt_on)
        self.helipilt_silt = tk.Label(self.aken, image=self.helipilt, bg="white", bd=0, cursor="hand2")
        self.helipilt_silt.place(relx=0.95, rely=0.95, anchor="se")

        self.helipilt_silt.bind("<Button-1>", self.lylita_heli)

    def main(self):
        self.aken.mainloop()


if __name__ == "__main__":
    menyy = Menyy()
    menyy.main()