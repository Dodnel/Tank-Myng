import tkinter as tk

class Menyy:
    def __init__(self):
        self.aken = tk.Tk()
        self.aken.title("Tank myng")
        self.aken.geometry("500x500")
        self.loo_vidinad()

    def stardi_myng(self):
        # Mäng käivitatakse pygame-iga
        self.aken.destroy()

    def ava_satted(self):
        self.satete_aken = tk.Toplevel(self.aken)
        self.satete_aken.title("Sätted")
        self.satete_aken.geometry("400x300")

        tk.Label(self.satete_aken, text="Sätted", font=("Arial", 24)).pack(pady=80)


        tk.Button(self.satete_aken, text="Sulge", command=self.satete_aken.destroy, font=("Arial", 16)).pack(pady=20)


    def loo_vidinad(self):
        tk.Label(self.aken, text="Faking tanki mäng mida??", font=("Arial", 24)).pack(pady=80)
        tk.Button(self.aken, text="START", font=("Arial", 16), command=self.stardi_myng, pady=10, padx=20).pack(pady=10)
        tk.Button(self.aken, text="SÄTTED", font=("Arial", 16), command=self.ava_satted, pady=10, padx=20).pack(pady=10)

    def main(self):
        self.aken.mainloop()


if __name__ == "__main__":
    menyy = Menyy()
    menyy.main()