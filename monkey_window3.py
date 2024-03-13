import random
import tkinter as tk
import threading
from time import perf_counter, sleep
import os
import settings

directory = "images"
files = os.listdir(directory)  # images name list


class MonkeyWindow2(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Experiment window')
        self.canvas_size = [500, 500]
        self.canvas = tk.Canvas(self, height=self.canvas_size[1], width=self.canvas_size[0])
        self.canvas.pack()

        t1 = threading.Thread(target=self.update)
        t1.start()

    def update(self):
        self.image_numbers = random.sample(list(range(len(files))), settings.image_number3)
        self.right_image = random.choice(self.image_numbers)

        table_size_x = self.canvas_size[0] // (settings.image_size3 + 5)
        table_size_y = self.canvas_size[1] // (settings.image_size3 + 5)

        self.image_position = random.sample(list([(i, j) for i in range(table_size_x) for j in range(table_size_y)]),
                                            settings.image_number3)

        if settings.shuffle_images:
            self.image_position2 = random.sample(
                list([(i, j) for i in range(table_size_x) for j in range(table_size_y)]),
                settings.image_number3)
        else:
            self.image_position2 = self.image_position

        self.texture = [tk.PhotoImage(file=f'images/{files[self.image_numbers[i]]}') for i in
                        range(settings.image_number3)]
        self.image = [self.canvas.create_image(settings.image_size3 // 2 + self.image_position[i][0] * (settings.image_size3 + 5),
                                               settings.image_size3 // 2 + self.image_position[i][1] * (settings.image_size3 + 5),
                                               image=self.texture[i]) for i in range(settings.image_number3)]
        self.canvas.itemconfig(self.image[self.right_image], state='hidden')

        sleep(settings.delay3[0])

        for i in range(settings.image_number3):
            self.canvas.itemconfig(self.image[i], state='hidden')

        sleep(settings.delay[1])

        for i in range(settings.image_number3):
            self.canvas.itemconfig(self.image[i], state='normal')

        print('move images')

        for i in range(settings.image_number3):
            self.canvas.move(self.image[i],
                             (self.image_position2[i][0] - self.image_position[i][0]) * (settings.image_size3 + 5),
                             (self.image_position2[i][1] - self.image_position[i][1]) * (settings.image_size3 + 5))


if __name__ == '__main__':
    window = MonkeyWindow2()
    window.mainloop()
