import tkinter as tk
import threading
from time import sleep, perf_counter
from tkinter import *
import settings
from random import randint, randrange


class MonkeyWindow2(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.log = [['Номер', 'Абсолютное время', 'Время на ответ', 'Ответ', 'Правильный ответ']]

        self.title('Experiment window')
        self.geometry('800x800')

        self.image_speed = randint(settings.image_min_speed, settings.image_max_speed)
        self.canvas_size = [500, 500]
        self.image_size = 32
        t = (self.canvas_size[1] - settings.image_number * self.image_size) // (settings.image_number + 1)
        x_pos = (self.canvas_size[0] - settings.barrier_width) // 2 - self.image_size - settings.barrier_dist
        self.image_position = [[x_pos, t * (i + 1) + self.image_size * i] for i in range(settings.image_number)]
        self.final_image_position = [[x_pos, t * (i + 1) + self.image_size * i] for i in range(settings.image_number)]
        print(self.image_position)
        self.canvas = Canvas(self, bg="white", width=self.canvas_size[0], height=self.canvas_size[1])
        self.canvas.pack(anchor=CENTER, expand=1)

        self.python_image = PhotoImage(file="settings.png")

        self.image = [self.canvas.create_image(*self.image_position[i], image=self.python_image) for i in
                      range(settings.image_number)]
        self.right_image = randrange(settings.image_number)
        # self.draw = [i == self.right_image for i in range(image_number)]
        for i in range(settings.image_number):
            if i != self.right_image:
                self.canvas.itemconfig(self.image[i], state='hidden')

        self.experiment_number = 1
        self.test_start = perf_counter()
        self.pressed = False

        self.bind()

        self.barrier = self.canvas.create_rectangle((self.canvas_size[0] - settings.barrier_width) // 2, 0,
                                                    settings.barrier_width + (self.canvas_size[0] - settings.barrier_width) // 2,
                                                    self.canvas_size[1], fill=settings.barrier_color)

        self.time = []
        for i in range(settings.image_number):
            self.time.append(perf_counter())

        self.t1 = threading.Thread(target=self.update)
        self.t1.start()

    def object_click_event(self, x: int):
        self.log.append([self.experiment_number, round(perf_counter() - settings.experiment_start, 3),
                         round(perf_counter() - self.test_start, 3),
                         x, self.right_image])
        self.pressed = True

    def update(self):
        for i in range(settings.repeat_number2):
            next_experiment = False
            while not next_experiment:
                next_experiment = True
                for i in range(settings.image_number):
                    self.canvas.move(self.image[i], self.image_speed * (perf_counter() - self.time[i]), 0)
                    self.time[i] = perf_counter()

                    if self.is_image_behind_barrier(i):
                        self.canvas.itemconfig(self.image[i], state='normal')
                    if not self.canvas.coords(self.image[i])[0] - (self.image_size // 2) > self.canvas_size[0]:
                        next_experiment = False

                sleep(0.05)
            sleep(settings.session_delay2)
            self.right_image = randrange(settings.image_number)
            for i in range(settings.image_number):
                pos = self.canvas.coords(self.image[i])
                self.canvas.move(self.image[i], self.image_position[i][0] - pos[0], self.image_position[i][1] - pos[1])
                self.canvas.itemconfig(self.image[i], state='normal' if self.right_image == i else 'hidden')
            self.test_start = perf_counter()
            if not self.pressed:
                self.log.append([self.experiment_number, round(perf_counter() - settings.experiment_start, 3),
                                 None, None, self.right_image])
            self.experiment_number += 1
            self.pressed = False
        self.destroy()

    def is_image_behind_barrier(self, n: int):
        img_pos = [self.canvas.coords(self.image[n])[0] - self.image_size // 2,
                   self.canvas.coords(self.image[n])[1] + self.image_size // 2]
        barrier_pos = ((self.canvas_size[0] - settings.barrier_width) // 2, 0,
                       settings.barrier_width + (self.canvas_size[0] - settings.barrier_width) // 2,
                       self.canvas_size[1])
        t = [img_pos, [img_pos[0] + self.image_size, img_pos[1]], [img_pos[0], img_pos[1] + self.image_size],
             [img_pos[0] + self.image_size, img_pos[1] + self.image_size]]
        t2 = 0
        for i in t:
            t2 += (barrier_pos[0] < i[0] < barrier_pos[2] and barrier_pos[1] < i[1] < barrier_pos[3])
        return t2 == 4

    def bind(self):
        # for i in range(image_number):
        #        self.canvas.tag_bind(self.image[i], '<Button-1>', lambda event: self.object_click_event(i))
        # doesn't work somehow
        if settings.image_number > 0:
            self.canvas.tag_bind(self.image[0], '<Button-1>', lambda event: self.object_click_event(0))
        if settings.image_number > 1:
            self.canvas.tag_bind(self.image[1], '<Button-1>', lambda event: self.object_click_event(1))
        if settings.image_number > 2:
            self.canvas.tag_bind(self.image[2], '<Button-1>', lambda event: self.object_click_event(2))
        if settings.image_number > 3:
            self.canvas.tag_bind(self.image[3], '<Button-1>', lambda event: self.object_click_event(3))
        if settings.image_number > 4:
            self.canvas.tag_bind(self.image[4], '<Button-1>', lambda event: self.object_click_event(4))
        if settings.image_number > 5:
            self.canvas.tag_bind(self.image[5], '<Button-1>', lambda event: self.object_click_event(5))
        if settings.image_number > 6:
            self.canvas.tag_bind(self.image[6], '<Button-1>', lambda event: self.object_click_event(6))
        if settings.image_number > 7:
            self.canvas.tag_bind(self.image[7], '<Button-1>', lambda event: self.object_click_event(7))
        if settings.image_number > 8:
            self.canvas.tag_bind(self.image[8], '<Button-1>', lambda event: self.object_click_event(8))
        if settings.image_number > 9:
            self.canvas.tag_bind(self.image[9], '<Button-1>', lambda event: self.object_click_event(9))


if __name__ == '__main__':
    root = Tk()
    root.title('main window')
    window = MonkeyWindow2()
    window.mainloop()
