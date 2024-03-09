import tkinter as tk
import threading
from time import sleep, perf_counter
from tkinter import *


class MonkeyWindow2(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.title('Experiment window')
        self.geometry('800x800')
        self.image_position = [10, 50]
        self.image_speed = 10

        self.canvas = Canvas(self, bg="white", width=500, height=500)
        self.canvas.pack(anchor=CENTER, expand=1)

        self.python_image = PhotoImage(file="settings.png")

        self.canvas.create_image(*self.image_position, image=self.python_image)

        self.t1 = threading.Thread(target=self.update)
        self.time = perf_counter()
        self.t1.start()

    def update(self):
        while True:
            self.image_position = [self.image_position[0] + self.image_speed * (perf_counter() - self.time),
                                   self.image_position[1]]
            self.canvas.delete("all")
            self.canvas.create_image(*self.image_position, image=self.python_image)
            self.time = perf_counter()
            sleep(0.1)


if __name__ == '__main__':
    root = Tk()
    root.title('main window')
    window = MonkeyWindow2(root)
    window.mainloop()
