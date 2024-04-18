import time
import tkinter as tk
import tkinter.messagebox as mb

from PIL.ImageTk import PhotoImage

import threading
from random import choice, shuffle
import os
from monkey_windows.monkey_window import MonkeyWindow
import settings
import utils

directory = "images"
temp_image_file = 'settings.png'


class MonkeyWindow1(MonkeyWindow):
    def __init__(self):
        super().__init__()
        self.image_size = 128
        self.pressed = None
        self.repeat_number = None
        self.session_number = None
        self.log = [['Номер', 'Абсолютное время', 'Время на ответ', 'Ответ', 'Правильный ответ']]
        self.experiment_number = 1
        self.test_start = None
        self.right_image = None
        self.delay = None
        self.picture_to_remember = None
        # self.attributes("-fullscreen", True)
        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)
        self.img = PhotoImage(file=temp_image_file)
        self.main_image = self.canvas.create_image(self.image_size // 2, self.image_size // 2, image=self.img)

        self.picture_to_remember = choice(files)

        self.img = [None, None]
        self.image = [None, None]

        self.load_settings()

        self.img1, self.img2 = None, None

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
        if not self.pressed:
            self.log.append([self.experiment_number, round(time.perf_counter() - settings.experiment_start, 3),
                            round(time.perf_counter() - self.test_start, 3),
                            number, self.right_image])
            if number == self.right_image:
                utils.play_right_answer_sound()
            else:
                utils.play_wrong_answer_sound()
        self.pressed = True

    def update(self):
        for i in range(self.session_number):
            for j in range(self.repeat_number):
                self.picture_to_remember = choice(files)
                self.img = PhotoImage(file=f'{directory}/{self.picture_to_remember}')
                self.main_image = self.canvas.create_image(self.image_size // 2, self.image_size // 2, image=self.img)

                time.sleep(self.delay[0])

                self.canvas.itemconfig(self.main_image, state='hidden')

                time.sleep(self.delay[1])

                self.pressed = False
                temp = files.copy()
                temp.remove(self.picture_to_remember)
                file = [self.picture_to_remember, choice(temp)]
                shuffle(file)
                self.right_image = file.index(self.picture_to_remember)

                self.img = [PhotoImage(file=f'{directory}/{file[i]}') for i in range(2)]
                self.image = [self.canvas.create_image((i + 0.5) * self.image_size, 0.5 * self.image_size, image=img)
                              for i, img in enumerate(self.img)]

                self.canvas.tag_bind(self.image[0], '<Button-1>', lambda event: self.image_pressed(0))
                self.canvas.tag_bind(self.image[1], '<Button-1>', lambda event: self.image_pressed(1))

                self.test_start = time.perf_counter()

                if not settings.restart_after_answer:
                    time.sleep(self.delay[2])
                else:
                    t = time.perf_counter()
                    while time.perf_counter() - t < self.delay[2]:
                        if self.pressed:
                            break
                        time.sleep(0.05)

                if not self.pressed:
                    self.log.append([self.experiment_number, round(time.perf_counter() - settings.experiment_start, 3),
                                     None, None, self.right_image])

                for k in range(2):
                    self.canvas.itemconfig(self.image[i], state='hidden')

                time.sleep(self.delay[3])

                self.experiment_number += 1

            time.sleep(self.delay[4])


if __name__ == '__main__':
    directory = '../images'
    temp_image_file = '../settings.png'
    files = os.listdir(directory)
    window = MonkeyWindow1()
    window.mainloop()
else:
    files = os.listdir(directory)

