from datetime import datetime
import time
import tkinter as tk
import tkinter.messagebox as mb

from PIL.ImageTk import PhotoImage

import threading
from random import choice, shuffle
import os

import settings

directory = "images"
files = os.listdir(directory)


class Monkey_window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.repeat_number = None
        self.session_number = None
        self.log = [['Абсолютное время', 'Время на ответ', 'Ответ', 'Правильный ответ']]
        self.test_start = None
        self.right_image = None
        self.delay = None
        self.picture_to_remember = None
        # self.attributes("-fullscreen", True)
        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)
        self.img = PhotoImage(file='settings2.png')
        self.main_image = tk.Label(self, image=self.img)
        self.main_image.grid(row=3, column=1)

        self.picture_to_remember = choice(files)

        self.img = [None, None]
        self.image = [None, None]

        self.load_settings()

        self.t1 = threading.Thread(target=self.update)
        self.t1.start()

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            self.destroy()

    def load_settings(self):
        self.delay = settings.delay
        self.session_number = settings.session_number
        self.repeat_number = settings.repeat_number

    def image_pressed(self, number):
        print(number)
        self.log.append([round(time.perf_counter() - settings.experiment_start, 3),
                         round(time.perf_counter() - self.test_start, 3),
                         number, self.right_image])

    def update(self):
        for i in range(self.session_number):
            for j in range(self.repeat_number):
                self.picture_to_remember = choice(files)
                self.img = PhotoImage(file=f'images/{self.picture_to_remember}')
                self.main_image = tk.Label(self, image=self.img)
                self.main_image.grid(row=3, column=1)

                time.sleep(self.delay[0])

                self.main_image.grid_forget()

                time.sleep(self.delay[1])

                temp = files.copy()
                temp.remove(self.picture_to_remember)
                file = [self.picture_to_remember, choice(temp)]
                shuffle(file)
                self.right_image = file.index(self.picture_to_remember)

                self.img = [PhotoImage(file=f'images/{file[i]}') for i in range(2)]
                self.image = [tk.Label(self, image=self.img[i]) for i in range(2)]

                for k in range(2):
                    self.image[k].grid(row=3, column=k)
                self.image[0].bind('<Button-1>', lambda event: self.image_pressed(0))
                self.image[0].bind('<Button-2>', lambda event: self.image_pressed(0))

                self.image[1].bind('<Button-1>', lambda event: self.image_pressed(1))
                self.image[1].bind('<Button-2>', lambda event: self.image_pressed(1))

                self.test_start = time.perf_counter()

                time.sleep(self.delay[2])

                for k in self.image:
                    k.grid_forget()

                time.sleep(self.delay[3])

            time.sleep(self.delay[4])
