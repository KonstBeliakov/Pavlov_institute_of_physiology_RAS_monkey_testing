import threading

import mss
import mss.tools

from PIL import Image
from PIL import ImageTk
import tkinter as tk

from settings import settings


class SecondScreenCopy:
    def __init__(self, root, x, y):
        self.root = root
        self.canvas = tk.Canvas(self.root)
        self.canvas.grid(row=y, column=x)

        t1 = threading.Thread(target=lambda: self.second_screen_update(self.canvas))
        t1.start()

    def second_screen_update(self, canvas):
        python_image = tk.PhotoImage(file="pictograms/settings.png")
        monitor_number = 2
        with mss.mss() as sct:
            mon = sct.monitors[monitor_number]
            self.canvas_image = canvas.create_image(int(mon['width'] * settings['monitor_copy_size']),
                                                    int(mon['height'] * settings['monitor_copy_size']),
                                                    image=python_image)
            monitor = {
                "top": mon["top"],
                "left": mon["left"],
                "width": mon["width"],
                "height": mon["height"],
                "mon": monitor_number,
            }
        while True:
            with mss.mss() as sct:
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                img2 = img.resize((int(img.size[0] * 2 * settings['monitor_copy_size']),
                                   int(img.size[1] * 2 * settings['monitor_copy_size'])))
                img3 = ImageTk.PhotoImage(img2)

                canvas.itemconfigure(self.canvas_image, image=img3)
