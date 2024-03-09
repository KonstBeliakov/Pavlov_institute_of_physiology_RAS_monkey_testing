import tkinter as tk
import threading
from time import sleep, perf_counter
from tkinter import *
from settings import *
from random import randint


class MonkeyWindow2(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.title('Experiment window')
        self.geometry('800x800')
        self.image_position = [10, 50]
        self.image_speed = randint(image_min_speed, image_max_speed)
        self.canvas_size = [500, 500]
        self.canvas = Canvas(self, bg="white", width=self.canvas_size[0], height=self.canvas_size[1])
        self.canvas.pack(anchor=CENTER, expand=1)

        self.python_image = PhotoImage(file="settings.png")

        self.image = self.canvas.create_image(*self.image_position, image=self.python_image)

        self.t1 = threading.Thread(target=self.update)
        self.time = perf_counter()
        self.t1.start()

    def update(self):
        while True:
            self.canvas.move(self.image, self.image_speed * (perf_counter() - self.time), 0)
            self.time = perf_counter()
            sleep(0.01)


if __name__ == '__main__':
    root = Tk()
    root.title('main window')
    window = MonkeyWindow2(root)
    window.mainloop()
