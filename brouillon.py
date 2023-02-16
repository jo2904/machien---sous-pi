import tkinter as tk  # used for the GUI
from tkinter import filedialog as fd
from tkinter import ttk
import os
import random


#####################################
########## DEF MAIN WINDOW ##########
#####################################
class Jeu:
    def __init__(self):
        self.fenetres = tk.Tk()
        self.fenetres.title("Jeu")

        width = self.fenetres.winfo_screenwidth()
        height = self.fenetres.winfo_screenheight()
        self.fenetres.geometry("%dx%d" % (width, height))

        self.canvas = []
        self.canvas.append(tk.Canvas(
            self.fenetres, width=200, height=400, bg="white"))
        self.canvas.append(tk.Canvas(
            self.fenetres, width=200, height=400, bg="white"))
        for canva in self.canvas:
            canva.pack(anchor=tk.CENTER)
        self.roue = []

        self.temps = 100

    def run(self):
        self.fenetres.mainloop()

    def update(self):

        for canvas in self.canvas:
            for obj in canvas.find_all():
                print(canvas.coords(obj))
                canvas.move(obj, 0, 20)

            self.fenetres.update()

        self.fenetres.after(self.temps, self.update)

    #####################################
    ####### DEF PREMIERE ROUE ###########
    #####################################

    def creation_roue(self):
        # on creer un canvas avec une image

        # roue = [images]
        for canvas in self.canvas:
            path = "asset/roue/1"

            images = []
            for file in os.listdir(path):
                if file.endswith(".png"):
                    images.append(tk.PhotoImage(
                        file=os.path.join(path, file)))
            self.roue.append(images)

            ordre = [random.randint(0, len(self.roue[0])-1)
                     for i in range(15)]

            print(ordre)

            i = 0
            j = 0
            for x in ordre:
                canvas.create_image(100, i, image=self.roue[0][x])
                i += 150
                j += 1

                jeu.fenetres.update()


#####################################
##########   MAINLOOP  ##############
#####################################
jeu = Jeu()
jeu.creation_roue()
jeu.update()
jeu.run()
