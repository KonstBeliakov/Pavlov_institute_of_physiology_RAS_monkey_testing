import time
import tkinter as tk
import tkinter.messagebox as mb

from PIL.ImageTk import PhotoImage

import threading
from random import choice, shuffle
import os

directory = "images"
files = os.listdir(directory)


class Monkey_window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.picture_to_remember = None
        self.attributes("-fullscreen", True)
        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)
        self.img = PhotoImage(file='settings2.png')
        self.image = tk.Label(self, image=self.img)
        self.image.grid(row=3, column=1)

        self.delay1 = 2
        self.delay2 = 2
        self.delay3 = 2
        self.picture_to_remember = choice(files)

        self.img1, self.img2 = None, None
        self.image1, self.image2 = None, None

        self.t1 = threading.Thread(target=self.update)
        self.t1.start()

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            self.destroy()

    def update(self):
        while True:
            time.sleep(self.delay1)
            self.image.grid_forget()

            time.sleep(self.delay2)

            temp = files.copy()
            temp.remove(self.picture_to_remember)
            file = [self.picture_to_remember, choice(temp)]
            shuffle(file)

            self.img1 = PhotoImage(file=f'images/{file[0]}')
            self.image1 = tk.Label(self, image=self.img1)
            self.image1.grid(row=3, column=0)

            self.img2 = PhotoImage(file=f'images/{file[1]}')
            self.image2 = tk.Label(self, image=self.img2)
            self.image2.grid(row=3, column=1)

            time.sleep(self.delay3)

            self.image1.grid_forget()
            self.image2.grid_forget()

            self.picture_to_remember = choice(files)
            self.img = PhotoImage(file=f'images/{self.picture_to_remember}')
            self.image = tk.Label(self, image=self.img)
            self.image.grid(row=3, column=1)
