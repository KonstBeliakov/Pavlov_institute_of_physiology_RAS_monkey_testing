import threading
from time import sleep, perf_counter
from tkinter import *
from settings import settings

from random import randint, randrange
import utils
from monkey_windows.monkey_window import MonkeyWindow
from widgets.canvas_object import CanvasObject


class MonkeyWindow2(MonkeyWindow):
    def __init__(self):
        super().__init__()

        self.log = [['Номер', 'Абсолютное время', 'Время на ответ', 'Ответ', 'Правильный ответ']]

        self.title('Experiment window')

        self.image_speed = randint(settings['image_min_speed'], settings['image_max_speed'])

        self.image_size = settings['image_size2']
        t = (self.canvas_size[1] - settings['image_number'] * self.image_size) // (settings['image_number'] + 1)
        x_pos = (self.canvas_size[0] - settings['barrier_width']) // 2 - self.image_size - settings['barrier_dist']
        self.image_position = [[x_pos, t * (i + 1) + self.image_size * i] for i in range(settings['image_number'])]

        filename = 'pictograms/yes.png'
        self.python_image = utils.open_image(filename, settings['image_size2'])

        self.objects = [CanvasObject(self.canvas, *self.image_position[i], self.image_size, filename,
                                     speedX=self.image_speed) for i in range(settings['image_number'])]

        self.right_image = randrange(settings['image_number'])

        for obj in self.objects:
            obj.hide()
        self.objects[self.right_image].show()

        self.experiment_number = 1
        self.test_start = perf_counter()
        self.pressed = False

        self.bind()

        self.barrier = self.canvas.create_rectangle((self.canvas_size[0] - settings['barrier_width']) // 2, 0,
                                                    settings['barrier_width'] + (
                                                                self.canvas_size[0] - settings['barrier_width']) // 2,
                                                    self.canvas_size[1], fill=settings['barrier_color'])

        self.t1 = threading.Thread(target=self.update)
        self.t1.start()

    def object_click_event(self, x: int):
        self.log.append([self.experiment_number, round(perf_counter() - settings['experiment_start'], 3),
                         round(perf_counter() - self.test_start, 3),
                         x, self.right_image])
        if x == self.right_image:
            utils.right_answer()
        else:
            utils.wrong_answer()
        self.pressed = True

    def update(self):
        for i in range(settings['repeat_number2']):
            next_experiment = False
            while not next_experiment:
                next_experiment = True
                for i, obj in enumerate(self.objects):
                    obj.update()

                    if self.is_image_behind_barrier(i):
                        obj.show()
                    if not obj.x - (self.image_size // 2) > self.canvas_size[0]:
                        next_experiment = False
                sleep(0.05)

            sleep(settings['session_delay2'])
            self.right_image = randrange(settings['image_number'])

            for i, obj in enumerate(self.objects):
                obj.set_pos(*self.image_position[i])
                obj.hide()

            self.objects[self.right_image].show()
            self.test_start = perf_counter()
            if not self.pressed:
                self.log.append([self.experiment_number, round(perf_counter() - settings['experiment_start'], 3),
                                 None, None, self.right_image])
            self.experiment_number += 1
            self.pressed = False
        self.destroy()

    def is_image_behind_barrier(self, n: int):
        img_pos = [self.objects[n].x - self.image_size // 2, self.objects[n].y + self.image_size // 2]
        barrier_pos = ((self.canvas_size[0] - settings['barrier_width']) // 2, 0,
                       settings['barrier_width'] + (self.canvas_size[0] - settings['barrier_width']) // 2,
                       self.canvas_size[1])
        t = [img_pos, [img_pos[0] + self.image_size, img_pos[1]], [img_pos[0], img_pos[1] + self.image_size],
             [img_pos[0] + self.image_size, img_pos[1] + self.image_size]]
        t2 = 0
        for i in t:
            t2 += (barrier_pos[0] < i[0] < barrier_pos[2] and barrier_pos[1] < i[1] < barrier_pos[3])
        return t2 == 4

    def bind_image(self, x):
        self.objects[x].bind('<Button-1>', lambda event: self.object_click_event(x))

    def bind(self):
        for i in range(settings['image_number']):
            self.bind_image(i)


if __name__ == '__main__':
    root = Tk()
    root.title('main window')
    window = MonkeyWindow2()
    window.mainloop()
