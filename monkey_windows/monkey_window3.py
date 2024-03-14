import random
import tkinter as tk
import threading
from time import perf_counter, sleep
import os
import settings

directory = "images"
files = os.listdir(directory)  # images name list


class MonkeyWindow3(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.test_start = None
        self.title('Experiment window')
        self.log = [['Номер', 'Абсолютное время', 'Время на ответ', 'Ответ', 'Правильный ответ']]
        self.experiment_number = 1
        self.canvas_size = [500, 500]
        self.canvas = tk.Canvas(self, height=self.canvas_size[1], width=self.canvas_size[0])
        self.canvas.pack()

        self.stop = False

        t1 = threading.Thread(target=self.update)
        t1.start()

    def update(self):
        while True:
            table_size_x = self.canvas_size[0] // (settings.image_size3 + 5)
            table_size_y = self.canvas_size[1] // (settings.image_size3 + 5)

            self.image_numbers = random.sample(list(range(len(files))), settings.max_image_number)
            self.texture = [tk.PhotoImage(file=f'images/{files[self.image_numbers[i]]}') for i in range(settings.max_image_number)]
            self.stop = False
            for image_number in range(settings.min_image_number + 1, settings.max_image_number + 1):
                self.image_position = random.sample(list([(i, j) for i in range(table_size_x) for j in range(table_size_y)]),
                                                    image_number)

                if settings.shuffle_images:
                    self.image_position2 = random.sample(
                        list([(i, j) for i in range(table_size_x) for j in range(table_size_y)]),
                        image_number)
                else:
                    self.image_position2 = self.image_position


                self.image = [
                    self.canvas.create_image(settings.image_size3 // 2 + self.image_position[i][0] * (settings.image_size3 + 5),
                                             settings.image_size3 // 2 + self.image_position[i][1] * (settings.image_size3 + 5),
                                             image=self.texture[i]) for i in range(image_number)]
                self.canvas.itemconfig(self.image[-1], state='hidden')

                sleep(settings.delay3[0])

                for i in range(len(self.image)):
                    self.canvas.itemconfig(self.image[i], state='hidden')

                sleep(settings.delay3[1])

                for i in range(image_number):
                    self.canvas.itemconfig(self.image[i], state='normal')

                print('move images...', end='')
                self.pressed = False
                self.bind()

                for i in range(len(self.image)):
                    self.canvas.move(self.image[i],
                                     (self.image_position2[i][0] - self.image_position[i][0]) * (settings.image_size3 + 5),
                                     (self.image_position2[i][1] - self.image_position[i][1]) * (settings.image_size3 + 5))
                print('done')

                self.test_start = perf_counter()

                while (perf_counter() - self.test_start) < settings.delay3[2]:
                    sleep(0.1)
                    if self.stop:
                        print('stop')
                        break
                if self.stop:
                    break

                if not self.pressed:
                    self.log.append([self.experiment_number, round(perf_counter() - settings.experiment_start, 3),
                                     None, None, image_number])

                for i in range(len(self.image)):
                    self.canvas.itemconfig(self.image[i], state='hidden')

                sleep(settings.delay3[3])

            self.experiment_number += 1

    def bind(self):
        # doesn't work for some reason
        #self.f = [lambda event: self.image_pressed(i) for i in range(len(self.image))]

        #for i in range(len(self.image)):
        #    self.canvas.tag_bind(self.image[i], '<Button-1>', self.f[i])#lambda event: self.image_pressed(i))

        if len(self.image) > 0:
            self.canvas.tag_bind(self.image[0], '<Button-1>', lambda event: self.image_pressed(0))
        if len(self.image) > 1:
            self.canvas.tag_bind(self.image[1], '<Button-1>', lambda event: self.image_pressed(1))
        if len(self.image) > 2:
            self.canvas.tag_bind(self.image[2], '<Button-1>', lambda event: self.image_pressed(2))
        if len(self.image) > 3:
            self.canvas.tag_bind(self.image[3], '<Button-1>', lambda event: self.image_pressed(3))
        if len(self.image) > 4:
            self.canvas.tag_bind(self.image[4], '<Button-1>', lambda event: self.image_pressed(4))
        if len(self.image) > 5:
            self.canvas.tag_bind(self.image[5], '<Button-1>', lambda event: self.image_pressed(5))
        if len(self.image) > 6:
            self.canvas.tag_bind(self.image[6], '<Button-1>', lambda event: self.image_pressed(6))
        if len(self.image) > 7:
            self.canvas.tag_bind(self.image[7], '<Button-1>', lambda event: self.image_pressed(7))
        if len(self.image) > 8:
            self.canvas.tag_bind(self.image[8], '<Button-1>', lambda event: self.image_pressed(8))
        if len(self.image) > 9:
            self.canvas.tag_bind(self.image[9], '<Button-1>', lambda event: self.image_pressed(9))

    def image_pressed(self, number):
        self.log.append([self.experiment_number, round(perf_counter() - settings.experiment_start, 3),
                         round(perf_counter() - self.test_start, 3), number, len(self.image) - 1])
        self.pressed = True

        if settings.stop_after_error and (number != len(self.image) - 1):
            self.stop = True
            print(number, len(self.image) - 1, 'stopped')


if __name__ == '__main__':
    window = MonkeyWindow3()
    window.mainloop()
