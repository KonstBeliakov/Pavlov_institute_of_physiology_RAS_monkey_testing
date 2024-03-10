import tkinter as tk
import threading
from time import sleep, perf_counter
from tkinter import *
from settings import *
from random import randint, randrange


class MonkeyWindow2(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.title('Experiment window')
        self.geometry('800x800')

        self.image_speed = randint(image_min_speed, image_max_speed)
        self.canvas_size = [500, 500]
        self.image_size = 32
        t = (self.canvas_size[1] - image_number * self.image_size) // (image_number + 1)
        self.image_position = [[10, t * (i + 1) + self.image_size * i] for i in range(image_number)]
        print(self.image_position)
        self.canvas = Canvas(self, bg="white", width=self.canvas_size[0], height=self.canvas_size[1])
        self.canvas.pack(anchor=CENTER, expand=1)

        self.python_image = PhotoImage(file="settings.png")

        self.image = [self.canvas.create_image(*self.image_position[i], image=self.python_image) for i in
                      range(image_number)]
        self.right_image = randrange(image_number)
        self.draw = [i == self.right_image for i in range(image_number)]
        for i in range(image_number):
            if i != self.right_image:
                self.canvas.itemconfig(self.image[i], state='hidden')
        self.barrier = self.canvas.create_rectangle((self.canvas_size[0] - barrier_width) // 2, 0,
                                                    barrier_width + (self.canvas_size[0] - barrier_width) // 2,
                                                    self.canvas_size[1], fill=barrier_color)

        self.time = []
        for i in range(image_number):
            self.time.append(perf_counter())

        self.t1 = threading.Thread(target=self.update)
        self.t1.start()

    def update(self):
        while True:
            for i in range(image_number):
                self.canvas.move(self.image[i], self.image_speed * (perf_counter() - self.time[i]), 0)
                self.time[i] = perf_counter()

                if self.is_image_behind_barrier(i):
                    self.canvas.itemconfig(self.image[i], state='normal')
            sleep(0.05)

    def is_image_behind_barrier(self, n: int):
        img_pos = [self.canvas.coords(self.image[n])[0] - self.image_size // 2,
                   self.canvas.coords(self.image[n])[1] + self.image_size // 2]
        barrier_pos = ((self.canvas_size[0] - barrier_width) // 2, 0,
                       barrier_width + (self.canvas_size[0] - barrier_width) // 2, self.canvas_size[1])
        t = [img_pos, [img_pos[0] + self.image_size, img_pos[1]], [img_pos[0], img_pos[1] + self.image_size],
             [img_pos[0] + self.image_size, img_pos[1] + self.image_size]]
        t2 = 0
        for i in t:
            t2 += (barrier_pos[0] < i[0] < barrier_pos[2] and barrier_pos[1] < i[1] < barrier_pos[3])
        return t2 == 4


if __name__ == '__main__':
    root = Tk()
    root.title('main window')
    window = MonkeyWindow2(root)
    window.mainloop()
