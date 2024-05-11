import random
import tkinter as tk
import threading
from time import perf_counter, sleep
import os
import settings
import utils
from monkey_windows.monkey_window import MonkeyWindow

directory = "images"
files = os.listdir(directory)  # images name list


class MonkeyWindow3(MonkeyWindow):
    def __init__(self):
        super().__init__()
        self.test_start = None
        self.title('Experiment window')
        self.log = [['Номер', 'Абсолютное время', 'Время на ответ', 'Ответ', 'Правильный ответ']]
        self.experiment_number = 1

        self.stop = False

        t1 = threading.Thread(target=self.update)
        t1.start()

    def update(self):
        while True:
            table_size_x = int(self.canvas_size[0] // (settings.image_size3 + 5))
            table_size_y = int(self.canvas_size[1] // (settings.image_size3 + 5))

            self.image_numbers = random.sample(list(range(len(files))), settings.max_image_number)
            self.texture = [tk.PhotoImage(file=f'{directory}/{files[self.image_numbers[i]]}') for i in
                            range(settings.max_image_number)]
            self.stop = False
            for image_number in range(settings.min_image_number + 1, settings.max_image_number + 1):
                self.image_position = random.sample(
                    list([(i, j) for i in range(table_size_x) for j in range(table_size_y)]),
                    image_number)

                if settings.shuffle_images:
                    self.image_position2 = random.sample(
                        list([(i, j) for i in range(table_size_x) for j in range(table_size_y)]),
                        image_number)
                else:
                    self.image_position2 = self.image_position

                self.image = [
                    self.canvas.create_image(
                        settings.image_size3 // 2 + self.image_position[i][0] * (settings.image_size3 + 5),
                        settings.image_size3 // 2 + self.image_position[i][1] * (settings.image_size3 + 5),
                        image=self.texture[i]) for i in range(image_number)]
                self.canvas.itemconfig(self.image[-1], state='hidden')

                sleep(settings.delay3[0])

                for i in range(len(self.image)):
                    self.canvas.itemconfig(self.image[i], state='hidden')

                sleep(settings.delay3[1])

                for i in range(image_number):
                    self.canvas.itemconfig(self.image[i], state='normal')

                self.pressed = False
                self.bind()

                for i in range(len(self.image)):
                    self.canvas.move(self.image[i],
                                     (self.image_position2[i][0] - self.image_position[i][0]) * (
                                                 settings.image_size3 + 5),
                                     (self.image_position2[i][1] - self.image_position[i][1]) * (
                                                 settings.image_size3 + 5))

                self.test_start = perf_counter()

                while (perf_counter() - self.test_start) < settings.delay3[2]:
                    sleep(0.1)
                    if self.stop:
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

    def bind_image(self, x):
        self.canvas.tag_bind(self.image[x], '<Button-1>', lambda event: self.image_pressed(x))

    def bind(self):
        for i in range(len(self.image)):
            self.bind_image(i)

    def image_pressed(self, number):
        self.log.append([self.experiment_number, round(perf_counter() - settings.experiment_start, 3),
                         round(perf_counter() - self.test_start, 3), number, len(self.image) - 1])
        self.pressed = True

        if settings.stop_after_error and (number != len(self.image) - 1):
            self.stop = True
            print(number, len(self.image) - 1, 'stopped')

        if number == len(self.image) - 1:
            utils.right_answer()
        else:
            utils.wrong_answer()


if __name__ == '__main__':
    window = MonkeyWindow3()
    window.mainloop()
