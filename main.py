import tkinter as tk  # used for the GUI
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import os
import time
import random
import math


#####################################
########## DEF MAIN WINDOW ##########
#####################################
class Jeu:
    def __init__(self):
        self.fenetres = tk.Tk()
        self.fenetres.title("Jeu")

        self.width = self.fenetres.winfo_screenwidth()
        self.height = self.fenetres.winfo_screenheight()
        self.fenetres.attributes('-fullscreen', True)

        self.fenetres.bind('<Key>', self.presse)
        self.fenetres.geometry("%dx%d" % (self.width, self.height))
        self.fenetres.configure(background='red')
        self.fenetres.configure(borderwidth=0)
        self.fenetres.update()

        self.images = []
        self.roue = []
        self.canvas = []
        self.physique = []
        self.path = "asset/roue/3"

        self.Cwidth = self.width/5
        self.decalage = 0.3
        print(self.Cwidth)
        self.Cheight = 500
        self.Cnb = 7

        self.pas = 50

        self.centrejeu = [0, 0.6]

        self.temps = 40
        self.compte = []

        self.Tdepart = 0
        self.duree = 25

        self.retour = 5

        self.resultat = []
        self.nb_roue = 3

        self.pause = True
        self.debut = True
        self.insert = []
        self.image_win = 0
        self.image_actu = 0

        self.images_deco = []
        self.canvas_deco = []
        self.canva_gif = []
        self.image_gif = []
        self.gif_actu = 0
        self.nb_image_gif = 0
        print(self.width/self.Cwidth)
        self.colone = int(self.width/self.Cwidth)

        self.deco()

    def deco(self):
        # bandeau
        path_bandeau = "asset/fond/fond"
        for file in os.listdir(path_bandeau):
            if file.endswith(".png"):

                img = Image.open(os.path.join(path_bandeau, file))
                img = img.resize((int(self.width), int(self.height)))
                self.images_deco.append(ImageTk.PhotoImage(img))
                label = tk.Label(self.fenetres,
                                 image=self.images_deco[-1])
                label.place(y=0, x=0)
        self.gif()

    def gif(self):
        # gif
        if self.canva_gif == []:
            path_gif = "asset/fond/gif"
            for file in os.listdir(path_gif):
                if file.endswith(".png"):
                    self.nb_image_gif += 1
                    img = Image.open(os.path.join(path_gif, file))
                    img = img.resize(
                        (int((4/10)*self.width), int((2/10)*self.height)))
                    self.image_gif.append(ImageTk.PhotoImage(img))
                    label = tk.Label(self.fenetres,
                                     image=self.image_gif[-1], borderwidth=0)
                    self.canva_gif.append(label)

        label = self.canva_gif[self.gif_actu].place_forget()
        self.gif_actu += 1
        if self.gif_actu == self.nb_image_gif:
            self.gif_actu = 0
        self.canva_gif[self.gif_actu].place(rely=self.centrejeu[1]+0.29,
                                            relx=0.5, anchor=tk.CENTER)

        self.fenetres.update()
        self.fenetres.after(1000, self.gif)

    def gagne(self):

        if len(self.insert) == 0:
            self.insert.append(False)
            path_win = "asset/fond/win/"
            for file in os.listdir(path_win):
                if file.endswith(".png"):
                    img = Image.open(os.path.join(path_win, file))
                    self.image_win += 1
                    img = img.resize(
                        (int((1/2)*self.width), int((2/10)*self.height)))
                    self.images_deco.append(ImageTk.PhotoImage(img))
                    label = tk.Label(self.fenetres,
                                     image=self.images_deco[-1], borderwidth=0)
                    self.canvas_deco.append(label)

        label = self.canvas_deco[self.image_actu].place_forget()
        self.image_actu += 1
        if self.image_actu == self.image_win:
            self.image_actu = 0
        self.canvas_deco[self.image_actu].place(rely=self.centrejeu[1]-0.2,
                                                relx=0.5, anchor=tk.CENTER)

        self.fenetres.after(200, self.gagne)
        self.fenetres.update()

    def perdu(self):
        if len(self.insert) == 0:
            self.insert.append(False)
            path_insert = "asset/fond/insert.jpg"
            img = Image.open(path_insert)
            img = img.resize((int((2/3)*self.width), int((2/10)*self.height)))
            self.images_deco.append(ImageTk.PhotoImage(img))
            label = tk.Label(self.fenetres,
                             image=self.images_deco[-1], bg="red", borderwidth=0)
            self.canvas_deco.append(label)

        if self.insert[0] == True:
            self.insert[0] = False
            label = self.canvas_deco[-1].place_forget()
        else:
            self.canvas_deco[-1].place(rely=self.centrejeu[1]-0.2,
                                       relx=0.5, anchor=tk.CENTER)

            self.insert[0] = True
        self.fenetres.after(1000, self.perdu)
        self.fenetres.update()

    def fin(self):
        index_C = 0

        # pour cahque roue
        for canva in self.canvas:
            cords = []
            # on trouve le minimum
            for element in canva.find_all():
                cords.append(canva.coords(element))
                # si c'est le min, on stoke l'index
                if cords[-1][1] == min(cords, key=lambda x: abs(x[1]))[1]:
                    actu = element
            # on enregistre le resultat
            self.resultat.append(self.roue[index_C][actu])
            index_C += 1

        # ici apparait le nuage
        print("fin", self.resultat)
        time.sleep(1)
        if (all(element == self.resultat[0] for element in self.resultat)):
            print("gagné")
            self.gagne()
        else:
            print("perdu")
            self.perdu()

    def update(self):

        index_c = 0
        # pour chaque roue
        for canva in self.canvas:
            # on prend la duree depuis le debut
            k = time.time() - self.Tdepart
            # on regarde si la roue doit partir (décallage d'une seconde)
            if k < 1 * index_c:
                break
            # accélération au début (plafond à 700)
            if k < (1/10) * self.duree + (index_c+1):
                self.physique[index_c] += 0.1 * \
                    self.physique[index_c]
                if self.physique[index_c] > 700:
                    self.physique[index_c] = 700
            # sinon on ralentit
            elif k < (9/10) * self.duree + (index_c+1):
                self.physique[index_c] -= 0.05 * self.physique[index_c]

            # on test si centrale
            cords = []
            for element in canva.find_all():
                cords.append(canva.coords(element))
            minimum = min(cords, key=lambda x: abs(x[1]))
            # si pas centrale mais preseque, maintient peite vitesse
            if self.physique[index_c] < 1.5 and (minimum[1]) > (3/7)*self.Cheight:
                self.physique[index_c] = 2
            # sinon on stop
            elif self.physique[index_c] < 1:
                self.physique[index_c] = 0
                cords = []
                for element in canva.find_all():
                    cords.append(canva.coords(element))
                minimum = min(cords, key=lambda x: abs(x[1]))

                # je calcule le nb de decalage
                nb_decalage = minimum[1] / self.retour
                # je decalle
                for x in range(abs(int(nb_decalage))):
                    for element in canva.find_all():
                        canva.move(element, 0, - 1 *
                                   (1 if nb_decalage > 0 else -1) * self.retour)
            # on update la vitesse
            vitesse = self.physique[index_c]

            # on test la fin
            if self.physique == [0.0 for i in range(self.nb_roue)]:
                self.fin()
                return

            # on modifie le compte du canvas (permet de bien géré les decalage)
            self.compte[index_c] += vitesse
            # on trouve le nb d'image
            derniere = self.Cnb + 1
            # on update les images
            index_i = 0
            for obj in canva.find_all():
                test = True
                # on l'affiche
                # si c'est la fin
                if index_i == derniere and canva.coords(obj)[1] < (1/2)*self.Cheight:
                    canva.move(obj, 0, -vitesse)
                    for obj2 in canva.find_all():
                        # on redecalle tt
                        canva.move(
                            obj2, 0, (self.compte[index_c]))
                    self.compte[index_c] = 0  # on reinit le compte
                    test = False
                if test:  # sinon on décalle
                    canva.move(obj, 0, -vitesse)
                index_i += 1

            index_c += 1
        self.fenetres.update()

        if not self.pause:
            self.fenetres.after(self.temps, self.update)

    def creation_roue(self, path):
        width = self.Cwidth
        height = self.Cheight
        image = []
        # on importe les images
        for file in os.listdir(path):
            if file.endswith(".png"):
                img = Image.open(os.path.join(path, file))
                img = img.resize((int((4/5)*width), int((6/14)*height)))
                image.append(ImageTk.PhotoImage(img))

        # on les mélanges
        ordre = [random.randint(0, len(image)-1) for i in range(self.Cnb)]

        # on fait un canvas
        canvas = tk.Canvas(
            self.fenetres, width=width, height=height, bg="white",  highlightthickness=3, highlightbackground="black")

        # on fait la roue
        # -1, X, 2, chaine, X, 2
        Wimage = (1/2)*width

        canvas.create_image(Wimage, (1/2)*height,
                            image=image[ordre[-1]])
        i = 2
        for x in ordre:
            canvas.create_image(Wimage, i*(1/2)*height, image=image[x])
            i += 1
        canvas.create_image(Wimage, i*(1/2) *
                            height, image=image[ordre[0]])
        canvas.create_image(Wimage, (i+1)*(1/2) *
                            height, image=image[ordre[1]])

        ordre2 = []
        ordre2.append(ordre[-1])
        for i in ordre:
            ordre2.append(i)
        ordre2.append(ordre[0])
        ordre2.append(ordre[1])

        self.roue.append(ordre2)

        for obj in canvas.find_all():
            canvas.move(obj, 0, -(1/2)*height)

        self.images.append(image)
        self.canvas.append(canvas)
        self.compte.append(0)
        self.physique.append(self.pas)
        # canvas.pack(side=tk.LEFT)

        temp = self.decalage + (self.Cwidth/self.width) * \
            (len(self.roue)-1)
        print(temp)
        canvas.place(relx=temp,
                     rely=self.centrejeu[1], anchor=tk.CENTER)
        # canvas.grid(row=1, column=int(self.colone/3) +
        #             len(self.roue)-1)  # , sticky=tk.EW)

        self.fenetres.update()

    def Pause(self):
        if self.pause:
            self.pause = False
        else:
            self.pause = True
        self.update()

    def presse(self, event):
        if event.keysym == "p":
            self.Pause()
        elif event.keysym == "q":
            self.quit()
        elif event.keysym == "r":
            self.restart()
        elif event.keysym == "space":
            if self.debut:
                self.debut = False
                self.start()

                self.Pause()

    def start(self):
        self.Tdepart = time.time()
        self.update()

    def run(self):
        self.fenetres.mainloop()

    def init(self):
        for i in range(self.nb_roue):
            self.creation_roue(self.path)

    def quit(self):
        self.fenetres.destroy()


#####################################
##########   MAINLOOP  ##############
#####################################


def main():
    jeu = Jeu()
    jeu.init()
    jeu.run()


main()
