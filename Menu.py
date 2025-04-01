import tkinter as tk

class Menu:
    def __init__(self):
        self.aken = tk.Tk()
        self.aken.title("Tank myng")
        self.aken.geometry("500x500")

    def looVidinad(self):
        menyy_silt = tk.Label(self.aken, text="Faking tanki mäng mida??", font=100)
        menyy_silt.pack(pady=80)
        start_nupp = tk.Button(self.aken, text="START", font=80, command="", pady=20, padx=20)
        start_nupp.pack(pady=20)
        setted_nupp = tk.Button(self.aken, text="SÄTTED", font=80, command="", pady=20, padx=20)
        setted_nupp.pack(pady=20)

    def main(self):
        menu.looVidinad()
        self.aken.mainloop()

if __name__ == "__main__":
    menu = Menu()
    menu.main()